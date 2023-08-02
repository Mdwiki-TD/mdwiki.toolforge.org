#!/usr/bin/env python
#   himo
""" 
إيجاد معرف ويكيداتا للعناصر بدون معرف

python3 core8/pwb.py mdpy/find_qids

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import json
import pywikibot
import codecs
import os
from pymysql.converters import escape_string
import stat
import sys
# ---
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import wiki_api
from mdpy.bots import wikidataapi
from mdpy import printe
# ---
project = '/data/project/mdwiki/'
if not os.path.isdir(project):
    project = '/mdwiki'
# ---


def check_title(title):
    # ---
    title = title.lower().strip()
    # ---
    if title.find('(disambiguation)') != -1:
        return False
    if title.startswith('user:'):
        return False
    # ---
    return True


# ---
qids = sql_for_mdwiki.get_all_qids()
# ---
qids_already = [q for title, q in qids.items() if q != '']
# ---
noqidsnoqids = [title for title, q in qids.items() if q == '' and check_title(title)]
# ---


def create_qids(no_qids):
    # create wikidata item for qids
    # ---
    for x in no_qids:
        # ---
        CREATE = f'CREATE||LAST|Len|"{x}"||LAST|P11143|"{x}"'
        # ---
        new = wikidataapi.post_to_qs(CREATE)
        # ---
        print(new)
        # ---
        # break
# ---


def get_qids(noqids_list):
    # ---
    new_title_qids = {}
    # ---
    params = {
        "action": "query",
        # "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "normalize": 1,
        "utf8": 1
    }
    # ---
    num = 0
    # ---
    for i in range(0, len(noqids_list), 50):
        group = noqids_list[i:i+50]
        # ---
        params["titles"] = '|'.join(group)
        # ---
        json1 = wiki_api.submitAPI(params, apiurl='https://en.wikipedia.org/w/api.php')
        # ---
        if json1:
            pages = json1.get("query", {}).get("pages", {})
            # ---
            for p, kk in pages.items():
                # ---
                num += 1
                # ---
                title = kk.get("title", "")
                qid = kk.get("pageprops", {}).get("wikibase_item", "")
                # ---
                new_title_qids[title] = qid
    # ---
    return new_title_qids


def start():
    # ---
    if len(noqids) == 0:
        printe.output('<<green>> noqids list is empty. return "".')
        return
    # ---
    new_title_qid = get_qids(noqids)
    # ---
    to_add_text = ''
    no = ''
    # ---
    to_add = {}
    no_qids = []
    # ---
    for x, q in new_title_qid.items():
        ll = f'"{q}":"{x}",\n'
        # ---
        if q == '':
            no += ll
            no_qids.append(x)
            continue
        # ---
        if not q in qids_already:
            to_add[x] = q
        else:
            to_add_text += ll
    # ---
    printe.output('===================')
    if to_add_text != '':
        printe.output('<<lightred>> flase qids: ')
        printe.output(to_add_text)
        printe.output('===================')
    # ---
    printe.output('===================')
    printe.output('<<lightred>>no qids:')
    printe.output(no)
    # ---
    if 'createq' in sys.argv:
        create_qids(no_qids)
    # ---
    printe.output(f'find qid to {len(to_add)} from {len(noqids)} pages.')
    # ---
    if len(to_add) > 0:
        printe.output('<<lightyellow>>\n'.join([f'{k}\t:\t{v}' for k, v in to_add.items()]))
        # ---
        print('add "addthem" to sys.argv to add them?')
        # ---
        if 'addthem' in sys.argv:
            sql_for_mdwiki.add_titles_to_qids(to_add)


# ---
if __name__ == '__main__':
    start()
# ---
