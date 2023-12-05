#!/usr/bin/python3
"""


"""
# python3 core8/pwb.py mdpages/qids_others/make_list
# python3 core8/pwb.py mdpages/qids_others/make_list add_sql
import sys
import os

# ---
from mdpages.qids_others import sql_qids_others
from mdpy.bots import catdepth2
from mdpy.bots import wiki_api
from mdpy.bots import mdwiki_api
from mdpy import printe
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
project += '/public_html/Translation_Dashboard/Tables/'
# ---
medwiki_to_enwiki_conflic = {}
medwiki_to_enwiki = {}
# ---
# mdtitle_to_qid = sql_qids_others.get_others_qids()
# sql_qids_others.add_titles_to_qids(tab, add_empty_qid=False)
# sql_qids_others.set_title_where_qid(new_title, qid)


def add_sql(o_qids):
    printe.output('write to sql')
    # ---
    others_in = sql_qids_others.get_others_qids()
    # others_in = { x: y for x, y in others_in.items() if y != ''}
    # ---
    same = [x for x in o_qids if x in others_in and others_in[x] == o_qids[x]]
    # ---
    diff = [x for x in o_qids if x in others_in and others_in[x] != o_qids[x] and o_qids[x] != '']
    # ---
    printe.output(f'len of same: {len(same)}')
    printe.output(f'len of diff: {len(diff)}')
    # ---
    # del all same from o_qids
    o_qids_new = {x: y for x, y in o_qids.items() if x not in same and x not in diff}
    # ---
    for x in diff:
        printe.output(f'x: {x}, qid_in: {others_in[x]} != new qid: {o_qids[x]}')
    # ---
    printe.output(f'<<lightgreen>> new len of o_qids_new:{len(o_qids_new)}')
    # ---
    len_empty = [x for x in o_qids_new if o_qids_new[x] == '']
    printe.output(f'<<lightgreen>> new len of len_empty:{len(len_empty)}')
    # ---
    if 'add' in sys.argv:
        sql_qids_others.add_titles_to_qids(o_qids_new, add_empty_qid=True)


def check():
    # ---
    all_pages = []
    sames = []
    missing_in_enwiki = []
    # ---
    o_qids = {}
    # ---
    printe.output('Get all pages...')
    # ---
    Listo = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    all_pages = mdwiki_api.Get_All_pages('!', namespace='0', apfilterredir='nonredirects')
    listo2 = [x for x in all_pages if x not in Listo]
    Listo = listo2
    # ---
    printe.output(f'len of cat pages: {len(Listo)}')
    # ---
    Listo = [x for x in Listo if valid_title(x)]
    # ---
    for i in range(0, len(Listo), 100):
        # ---
        newlist = Listo[i : i + 100]
        # ---
        line = "|".join(newlist)
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageprops",
            "ppprop": "wikibase_item",
            "titles": line,
            # "redirects": 1,
            "converttitles": 1,
            "utf8": 1,
        }
        # ---
        if 'redirects' in sys.argv:
            params["redirects"] = 1
        # ---
        jsone = wiki_api.submitAPI(params, apiurl='https://' + 'en.wikipedia.org/w/api.php', returnjson=False)
        # ---
        if jsone and 'batchcomplete' in jsone:
            # ---
            query = jsone.get("query", {})
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get("redirects", [])
            for red in Redirects:
                if red["to"] not in all_pages:
                    medwiki_to_enwiki[red["from"]] = red["to"]
                else:
                    medwiki_to_enwiki_conflic[red["from"]] = red["to"]
            # ---
            redirects_x = {x['to']: x['from'] for x in Redirects}
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            # { "-1": { "ns": 0, "title": "Fsdfdsf", "missing": "" }, "2767": { "pageid": 2767, "ns": 0, "title": "ACE inhibitor" } }
            # ---
            for page in pages:
                # ---
                tab = pages[page]
                title = tab['title']
                # ---
                if 'missing' in tab:
                    missing_in_enwiki.append(title)
                else:
                    title = redirects_x.get(title, title)
                    # printe.output('<<lightyellow>> title["%s"] sames' % title )
                    qid = tab.get("pageprops", {}).get("wikibase_item", "")
                    o_qids[title] = qid
                    sames.append(title)
            # ---
        else:
            printe.output("<<lightred>> check.py no jsone")
            printe.output(jsone)
        # ---
    # ---
    numb = 0
    for fromm, to in medwiki_to_enwiki.items():
        numb += 1
        faf = f'["{fromm}"]'
        printe.output(f'en titles {numb} from_to{faf.ljust(30)} = "{to}"')
    # ---
    numb = 0
    # ---
    printe.output('<<lightred>> pages both in mdwiki cat:::')
    for md, en in medwiki_to_enwiki_conflic.items():
        numb += 1
        faf = f'["{md}"]'
        fen = f'["{en}"]'
        printe.output(f'<<lightred>> {numb} page{faf.ljust(40)} to enwiki{fen}')
    # ---
    sames = list(set(sames))
    missing_in_enwiki = list(set(missing_in_enwiki))
    # ---
    printe.output(f'<<lightgreen>> len of medwiki_to_enwiki:{len(medwiki_to_enwiki)}')
    printe.output(f'<<lightgreen>> len of missing_in_enwiki:{len(missing_in_enwiki)}')
    printe.output(f'<<lightgreen>> len of medwiki_to_enwiki_conflic:{len(medwiki_to_enwiki_conflic)}')
    printe.output(f'<<lightgreen>> len of sames:{len(sames)}')
    # ---
    printe.output(f'<<lightgreen>> len of o_qids:{len(o_qids)}')
    # --
    o_qids_n = {x: q for x, q in o_qids.items() if q != ''}
    printe.output(f'<<lightgreen>> len of o_qids (qid != ""):{len(o_qids_n)}')
    # ---
    for x in missing_in_enwiki:
        if not x in o_qids:
            o_qids[x] = ''
    # ---
    o_qids = {x: v for x, v in o_qids.items() if x in all_pages}
    # ---
    # write to sql
    add_sql(o_qids)
    # ---


if __name__ == '__main__':
    check()
