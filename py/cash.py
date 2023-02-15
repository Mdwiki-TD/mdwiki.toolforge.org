#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
""" 
إيجاد معرف ويكيداتا للعناصر بدون معرف

python3 pwb.py py/cash


"""
#
# (C) Ibrahem Qasim, 2022
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
noqids1 = {}
#---
json_file = project + '/public_html/Translation_Dashboard/Tables/noqids.json'
# load json file
with open(json_file, 'r') as f:
    noqids1 = json.load(f)
f.close()
#---
import py_tools
# py_tools.split_lists_to_numbers( lise, maxnumber = 100 )
#---
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
new_title_qid = {}
#---
qids_already = list(en_to_md.mdtitle_to_qid.values())
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
        qids = json.load(open(project + '/public_html/Translation_Dashboard/Tables/mdwiki_to_qid.json'))
        #---
        qids_values = list(qids.values())
        #---
        for title, qid in to_add.items():
            if not qid in qids_values:
                qids[title] = qid
        #---
        with open( project + '/public_html/Translation_Dashboard/Tables/mdwiki_to_qid.json', 'w') as uuu:
            json.dump(qids, uuu)
        uuu.close()
#---

#---
if __name__ == '__main__':
    get_qids()
#---