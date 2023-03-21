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
import datetime
from datetime import datetime
Day_History = datetime.now().strftime("%Y-%m-%d")
#---
sys_argv = sys.argv or []
#---
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
if not os.path.isdir(project): project = '/mdwiki'
#---
#---
json_file = project + '/public_html/Translation_Dashboard/Tables/noqids.json'
# load json file
#---
noqids1 = json.load(open(json_file, 'r'))
#---
import py_tools
# py_tools.split_lists_to_numbers( lise, maxnumber = 100 )
#---
import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---
import wdapi
# wdapi.submitAPI( params, apiurl = 'https://' + 'en.wikipedia.org/w/api.php' )
#---
noqids = [ x for x in noqids1 if not x in en_to_md.mdtitle_to_qid ]
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
new_title_qid = {}
#---
qids_already = list(en_to_md.mdtitle_to_qid.values())
#---
def add_them(to_add):
    #---
    sql_for_mdwiki.add_titles_to_qids(to_add)
#---
def get_qids():
    #---
    splits = py_tools.split_lists_to_numbers( noqids )
    #---
    table = {}
    #---
    num = 0
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
    for lis in splits:
        #---
        ggg = splits[lis]
        params["titles"] = '|'.join( ggg )
        #---
        json1 = wdapi.submitAPI( params, apiurl = 'https://en.wikipedia.org/w/api.php' )
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
    #---
    tat = ''
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
                tat += ll
        else:
            no += ll
    #---
    pywikibot.output('===================' )
    if tat != '':
        pywikibot.output('<<lightred>> flase qids: ' )
        pywikibot.output(tat)
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