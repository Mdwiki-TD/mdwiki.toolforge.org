#!/usr/bin/env python
#   himo
"""
إيجاد معرف ويكيداتا للعناصر بدون معرف
The script checks if the project directory exists and changes the path if it doesn't. This is a good practice for handling file paths.

The script retrieves all Wikidata identifiers (QIDs) and filters them based on whether they are empty or not.

Usage:
python3 core8/pwb.py mdpy/find_qids

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import os
import sys

# ---
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import wiki_api
from mdpy.bots import wikidataapi
from mdpy import printe
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
project = '/data/project/mdwiki/'
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
qids = sql_for_mdwiki.get_all_qids()
# ---
# qids_already = [q for title, q in qids.items() if q != '']
qids_already = {q: title for title, q in qids.items() if q != ''}
# ---
noqids = [title for title, q in qids.items() if q == '' and valid_title(title)]


def create_qids(no_qids):
    """create wikidata item for qids
    creates new Wikidata items for those without QIDs. It uses a for loop to iterate over the list of items without QIDs and makes a POST request to the Wikidata API for each item. The function also prints the response from the API, which can be useful for debugging.
    """
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


def get_qids(noqids_list):
    """
    function retrieves QIDs for a list of items. It uses the MediaWiki API to query for page properties and extracts the Wikidata item property. The function handles redirects and normalizes the titles. It also groups the items into batches of 50 to avoid exceeding the API's limit for the number of titles in a single request. This is a good practice for working with APIs.
    """
    # ---
    new_title_qids = {}
    # ---
    params = {
        "action": "query",
        # "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        # "normalize": 1,
        "utf8": 1,
    }
    # ---
    if 'redirects' in sys.argv:
        params["redirects"] = 1
    # ---
    num = 0
    # ---
    for i in range(0, len(noqids_list), 50):
        group = noqids_list[i : i + 50]
        # ---
        params["titles"] = '|'.join(group)
        # ---
        json1 = wiki_api.submitAPI(params, apiurl='https://en.wikipedia.org/w/api.php')
        # ---
        if json1:
            redirects = json1.get("query", {}).get("redirects", [])
            redirects = {x['to']: x['from'] for x in redirects}
            # ---
            pages = json1.get("query", {}).get("pages", {})
            # ---
            for _, kk in pages.items():
                # ---
                num += 1
                # ---
                title = kk.get("title", "")
                qid = kk.get("pageprops", {}).get("wikibase_item", "")
                # ---
                title = redirects.get(title, title)
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
    no = ''
    # ---
    false_qids = {}
    # ---
    to_add = {}
    empty_qids = []
    # ---
    for x, q in new_title_qid.items():
        ll = f'"{q}":"{x}",\n'
        # ---
        if q == '':
            no += ll
            empty_qids.append(x)
            continue
        # ---
        if q not in list(qids_already.keys()):
            to_add[x] = q
        else:
            false_qids[x] = q
    # ---
    printe.output('===================')
    if false_qids:
        printe.output('<<lightred>> flase qids:')
        for xz, q in false_qids.items():
            title_in = qids_already.get(q, '')
            # ---
            printe.output(f'q: {q}\t new title: ({xz})\t: title_in: ({title_in})..')
    # ---
    printe.output('===================')
    printe.output(f'<<lightred>>no qids: {len(empty_qids)}')
    if empty_qids:
        printe.output(no)
        # ---
        printe.output('<<purple>> add "createq" to sys.argv to create new items for them?')
        # ---
        if 'createq' in sys.argv:
            create_qids(empty_qids)
    # ---
    printe.output('===================')
    printe.output(f'find qid to {len(to_add)} from {len(noqids)} pages.')
    # ---
    if len(to_add) > 0:
        printe.output('<<lightyellow>>\n'.join([f'{k}\t:\t{v}' for k, v in to_add.items()]))
        # ---
        printe.output('<<purple>> add "addthem" to sys.argv to add them?')
        # ---
        if 'addthem' in sys.argv:
            sql_for_mdwiki.add_titles_to_qids(to_add)


if __name__ == '__main__':
    start()
