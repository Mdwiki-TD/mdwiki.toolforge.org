#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
""" 
إيجاد معرف ويكيداتا للعناصر بدون معرف

python3 pwb.py mdpy/cash


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
import stat
import sys
sys.dont_write_bytecode = True
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
if not os.path.isdir(project): project = '/mdwiki'
#---
from mdpy import wiki_api
#---
from mdpy import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
qids = sql_for_mdwiki.get_all_qids()
#---
qids_already = [ q for title, q in qids.items() if q != '']
#---
noqids = [ title for title, q in qids.items() if q == '']
#---
def add_them(to_add):
    #---
    sql_for_mdwiki.add_titles_to_qids(to_add)
#---
new_title_qid = {}
#---
def get_qids():
    #---
    params = {
        "action": "query",
        # "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "normalize": 1,
        "utf8": 1
        }
    #---
    num = 0
    #---
    for i in range(0, len(noqids), 50):
        #---
        group = noqids[i:i+50]
        params["titles"] = '|'.join( group )
        #---
        json1 = wiki_api.submitAPI( params, apiurl = 'https://en.wikipedia.org/w/api.php' )
        #---
        if json1:
            pages = json1.get("query",{}).get("pages",{})
            #---
            for p, kk in pages.items():
                #---
                num += 1
                #---
                title = kk.get("title","")
                qid   = kk.get("pageprops", {}).get("wikibase_item", "")
                #---
                new_title_qid[title] = qid
    #---
    to_add_text = ''
    no = ''
    #---
    toadd = 0
    #---
    to_add = {}
    #---
    for x, q in new_title_qid.items():
        ll = f'"{q}":"{x}",\n'
        if q != '':
            if not q in qids_already:
                toadd += 1
                pywikibot.output('<<lightyellow>>' + ll.strip() )
                to_add[x] = q
            else:
                to_add_text += ll
        else:
            no += ll
    #---
    pywikibot.output('===================' )
    if to_add_text != '':
        pywikibot.output('<<lightred>> flase qids: ' )
        pywikibot.output(to_add_text)
        pywikibot.output('===================' )
    #---
    pywikibot.output('===================' )
    pywikibot.output('<<lightred>>no qids:' )
    pywikibot.output( no )
    #---
    pywikibot.output('find qid to %d from %d pages. ' % ( toadd, len(noqids)))
    #---
    if 'addthem' in sys.argv and toadd > 0:
        add_them(to_add)
#---
if __name__ == '__main__':
    get_qids()
#---