#!/usr/bin/python3
"""

python3 core8/pwb.py mdpages/P11143

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import sys

# ---
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import catdepth2
from mdpy.bots import wikidataapi
from mdpy import printe

# ---
sys.argv.append('workhimo')
# ---
wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php")
# ---
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
# ---
qids_di = sql_for_mdwiki.get_all_qids()
# ---
qids = {q: title for title, q in qids_di.items() if q != ''}
# ---
mdwiki_in_qids = list(qids.values())
# ---
query = '''select distinct ?item ?prop where { ?item wdt:P11143 ?prop .}'''
# ---
in_wd = {}
# ---
new_qids = {}
# ---
wdlist = wikidataapi.sparql_generator_url(query, printq=False, add_date=True)
# ---
for wd in wdlist:
    prop = wd['prop']
    # ---
    qid = wd['item'].split('/entity/')[1]
    # ---
    in_wd[qid] = prop
    # ---
    if qid not in qids and prop not in mdwiki_in_qids:
        new_qids[qid] = prop


def add_missing(newlist):
    # ---
    print('len of newlist: ' + str(len(newlist)))
    # ---
    if len(newlist) > 0:
        # ---
        printe.output(f'<<yellow>>claims to add_missing: {len(newlist.items())}')
        if len(newlist.items()) < 100:
            print("\n".join([f'{k}\t:\t{v}' for k, v in newlist.items()]))
        # ---
        if 'add' not in sys.argv:
            printe.output('<<puruple>> add "add" to sys.argv to add them?')
            return
        # ---
        n = 0
        # ---
        for q, value in newlist.items():
            n += 1
            printe.output(f'<<yellow>> q {n} from {len(newlist)}')
            wikidataapi.Claim_API_str(q, 'P11143', value)


def fix(merge_qids):
    # mdwiki != P11143
    # تصحيح قيم الخاصية التي لا تساوي اسم المقالة
    # ---
    for q, wd_value in merge_qids.copy().items():
        md_title = qids.get(q)
        if md_title == wd_value:
            continue
        # ---
        print(f'wd_value:{wd_value} != md_title:{md_title}, qid:{q}')
        # ---
        merge_qids[q] = md_title
        # ---
        # delete the old
        ae = wikidataapi.Get_claim(q, 'P11143', get_claim_id=True)
        if ae:
            for x in ae:
                value = x['value']
                claimid = x['id']
                if value == wd_value:
                    uxx = wikidataapi.Delete_claim(claimid)
                    if uxx:
                        print(f'True.. Deleted {claimid}')
                    else:
                        print(f'Failed to delete {claimid}')
        # ---
        # add the correct claim
        ase = wikidataapi.Claim_API_str(q, 'P11143', md_title)
        if ase:
            print(f'True.. Added P11143:{md_title}')
        else:
            print(f'Failed to add P11143:{md_title}')


def duplicate(merge_qids):
    # ايجاد عناصر ويكي بيانات بها قيمة الخاصية في أكثر من عنصر
    va_tab = {}
    # ---
    for q, va in merge_qids.items():
        # ---
        if va not in va_tab:
            va_tab[va] = []
        # ---
        if q not in va_tab[va]:
            va_tab[va].append(q)
    # ---
    va_tab_x = {k: v for k, v in va_tab.items() if len(v) > 1}
    # ---
    if va_tab_x:
        printe.output(f'<<lightyellow>> len of va_tab_x: {len(va_tab_x)}')
        # ---
        for va, qs in va_tab_x.items():
            print(f'va:{va}, qs:{qs}')
    # ---
    printe.output('<<lightyellow>> duplicate() end...')


def add_q(new_qids):
    # ---
    TD_list = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    print('len of new_qids: ' + str(len(new_qids)))
    # ---
    if len(new_qids) < 10:
        print("\n".join([f'{k}:{v}' for k, v in new_qids.items()]))
    # ---
    newtitles = {title: qid for qid, title in new_qids.items()}
    # ---
    titles_not_td = [x for x in newtitles if x not in TD_list]
    # ---
    delets = []
    # ---
    for title in titles_not_td:
        # printe.output(f'del {title}:{newtitles[title]} not in TD_list')
        del newtitles[title]
        delets.append(title)
    # ---
    print(f'len of newtitles: {len(newtitles)}, len of delets: {len(delets)}')
    # ---
    if len(newtitles) > 0:
        printe.output('<<puruple>> add "addq" to sys.argv to add them to qids')
        # ---
        if 'addq' not in sys.argv:
            return
        # ---
        sql_for_mdwiki.add_titles_to_qids(newtitles)
        # ---


def start():
    # ---
    print(f'len of in_wd: {len(in_wd)}')
    # ---
    newlist = {q: tt for q, tt in qids.items() if q not in in_wd.keys()}
    # ---
    add_missing(newlist)
    # ---
    # merge_qids = {**newlist, **in_wd}
    merge_qids = {**newlist, **in_wd}
    # ---
    if 'fix' in sys.argv:
        fix(merge_qids)
    # ---
    duplicate(merge_qids)
    # ---
    add_q(new_qids)


if __name__ == '__main__':
    start()
