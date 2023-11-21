#!/usr/bin/python3
"""
This script performs various operations related to MediaWiki pages and Wikibase QIDs.
It includes functions for filtering and processing page titles, checking page existence, 
retrieving and modifying page content, and adding tags based on QIDs.
"""
# python3 core8/pwb.py mdpages/qids_others/unlinkedwikibase
# ---
import sys
from mdpy.bots import sql_for_mdwiki
from mdpages.qids_others import sql_qids_others
from mdpy.bots import mdwiki_api
from mdpy import printe
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
from new_api.mdwiki_page import MainPage as md_MainPage

# ---
qids1 = sql_for_mdwiki.get_all_qids()
qids2 = sql_qids_others.get_others_qids()
# ---
qids1 = {x: v for x, v in qids1.items() if v != ''}
qids2 = {x: v for x, v in qids2.items() if v != ''}
# ---
vals_d = {}
# ---
for tab in [qids1, qids2]:
    for x, q in tab.items():
        if q not in vals_d:
            vals_d[q] = [x]
        elif x not in vals_d[q]:
            vals_d[q].append(x)
# ---
qids = {v[0]: q for q, v in vals_d.items() if len(v) == 1}
# ---
for q, v in vals_d.items():
    if len(v) > 1:
        printe.output(f'q:{q}, v:{v}')


def work_page(title, qid):
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        return
    # ---
    # if page.isRedirect() :  return
    # target = page.get_redirect_target()
    # ---
    text = page.get_text()
    # refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
    templates = page.get_templates()
    # ---
    if text.find('{{#unlinkedwikibase:id=') != -1:
        printe.output('page already tagged')
        return
    # ---
    tag = '{{#unlinkedwikibase:id=' + qid + '}}'
    # ---
    newtext = tag + text
    page.save(newtext=newtext, summary='add tag:' + tag, nocreate=1, minor='')


def add_tag():
    # ---
    printe.output('Get all pages...')
    # ---
    all_pages = mdwiki_api.Get_All_pages('!', namespace='0', apfilterredir='nonredirects')
    # ---
    all_pages = [x for x in all_pages if valid_title(x)]
    printe.output(f'len of all_pages: {len(all_pages)}')
    # ---
    for n, x in enumerate(all_pages):
        printe.output(f'p:{n}/{len(all_pages)}: t:{x}::')
        # ---
        # qid = qids1.get(x) or qids2.get(x)
        qid = qids.get(x)
        # ---
        if not qid:
            printe.output('no qid')
            continue
        # ---
        work_page(x, qid)


if __name__ == '__main__':
    if 'add' in sys.argv:
        add_tag()
