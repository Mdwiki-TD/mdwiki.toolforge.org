#!/usr/bin/python
"""

python3 core8/pwb.py mdpy/get_md_to_en nodump

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json

# ---
# ---

import sys
import os

# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
project += '/public_html/Translation_Dashboard/Tables/'
# ---
from mdpy.bots import catdepth2
from mdpy.bots import wiki_api
from mdpy import printe

# ---
medwiki_to_enwiki_conflic = {}
medwiki_to_enwiki = {}
missing_in_enwiki = []
sames = []
# ---


def check():
    # ---
    printe.output('Get cat pages from cat : RTT')
    # ---
    # Listo = mdwiki_api.subcatquery( 'RTT', depth = '1', ns = '0' )
    Listo = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    printe.output(f'len of cat pages: {len(Listo)}')
    # ---
    number = 0
    # ---
    Listo = [x for x in Listo if not (x.startswith('Category:') or x.startswith('File:') or x.startswith('Template:') or x.startswith('User:') or x.endswith("(disambiguation)"))]
    # ---
    for i in range(0, len(Listo), 100):
        # ---
        newlist = Listo[i:i + 100]
        # ---
        line = "|".join(newlist)
        # ---
        params = {
            "action": "query",
            "format": "json",
            # "prop": "redirects",
            # "rdlimit": "max"
            "titles": line,
            "redirects": 1,
            "converttitles": 1,
            "utf8": 1,
        }
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
                if red["to"] not in Listo:
                    medwiki_to_enwiki[red["from"]] = red["to"]
                else:
                    medwiki_to_enwiki_conflic[red["from"]] = red["to"]
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            pages_example = {
                "-1": {
                    "ns": 0,
                    "title": "Fsdfdsf",
                    "missing": ""
                },
                "2767": {
                    "pageid": 2767,
                    "ns": 0,
                    "title": "ACE inhibitor"
                }
            }
            # ---
            for page in pages:
                # ---
                tab = pages[page]
                title = tab['title']
                # ---
                if 'missing' in tab:
                    missing_in_enwiki.append(title)
                else:
                    # printe.output('<<lightyellow>> title["%s"] sames' % title )
                    sames.append(title)
            # ---
        else:
            printe.output("<<lightred>> check.py no jsone")
            printe.output(jsone)
        # ---
        # break
        # ---
    # ---
    numb = 0
    for fromm, to in medwiki_to_enwiki.items():
        numb += 1
        faf = f'["{fromm}"]'
        printe.output('en titles %d from_to%s = "%s"' % (numb, faf.ljust(30), to))
    # ---
    numb = 0
    for mis in missing_in_enwiki:
        numb += 1
        printe.output('<<lightyellow>> %d title:%s missing_in_enwiki' % (numb, mis.ljust(25)))
    # ---
    numb = 0
    # ---
    for md, en in medwiki_to_enwiki_conflic.items():
        numb += 1
        faf = f'["{md}"]'
        fen = f'["{en}"]'
        printe.output('<<lightred>> %d page%s redirect to enwiki%s, and they both in mdwiki cat.' % (numb, faf.ljust(30), fen.ljust(30)))
    # ---
    printe.output(f'<<lightgreen>> len of medwiki_to_enwiki:{len(medwiki_to_enwiki)}')
    printe.output(f'<<lightgreen>> len of missing_in_enwiki:{len(missing_in_enwiki)}')
    printe.output(f'<<lightgreen>> len of medwiki_to_enwiki_conflic:{len(medwiki_to_enwiki_conflic)}')
    printe.output(f'<<lightgreen>> len of sames:{len(sames)}')
    # ---
    if 'nodump' not in sys.argv:
        # الكتابة إلى الملفات
        json.dump(medwiki_to_enwiki, open(project + 'medwiki_to_enwiki.json', 'w'))
        # ---
        json.dump(missing_in_enwiki, open(project + 'missing_in_enwiki.json', 'w'))
        # ---
        json.dump(sames, open(project + 'sames.json', 'w'))


# ---
if __name__ == '__main__':
    check()
# ---
