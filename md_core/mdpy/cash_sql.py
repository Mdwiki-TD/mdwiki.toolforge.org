#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
""" 
إيجاد معرف ويكيداتا للعناصر بدون معرف

python3 pwb.py mdpy/cash_sql


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
import sys
sys.dont_write_bytecode = True
#---
from mdpy import sql_for_mdwiki
#---
from mdpy import py_tools

#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
if not os.path.isdir(project): project = '/mdwiki'
#---
noqids1 = []
#---
with open(project + '/public_html/Translation_Dashboard/Tables/noqids.json', 'r') as f:
    noqids1 = json.load(f)
#---
from mdpy import wiki_api

#---
noqids = []
#---
title_to_qid_in_sql = {}
#---
sq = sql_for_mdwiki.mdwiki_sql(' select DISTINCT title, qid from qids;')
#---
for ta in sq: 
    title = py_tools.Decode_bytes(ta[0])
    qqid = py_tools.Decode_bytes(ta[1])
    if qqid != '':
        title_to_qid_in_sql[title] = qqid
    else:
        noqids.append(title)
#---
for x in noqids1:
    if not x in title_to_qid_in_sql and not x in noqids :
        noqids.append(x)
#---
qids_list_already = list(title_to_qid_in_sql.values())
#---
def add_them(table):
    #---
    all_texts = ''
    #---
    texts = ''
    #---
    for title, qid in table.items():
        #---
        title2 = py_tools.make_cod(title)
        #---
        qid_in = title_to_qid_in_sql.get(title,'')
        #---
        # qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}' WHERE NOT EXISTS ( SELECT 1 FROM qids q2 WHERE q2.title = {title});""".format(qid=qid, title = title2)
        qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}';""".format(qid=qid, title = title2)
        #---
        if title in title_to_qid_in_sql:
            qua = """UPDATE qids set qid = '{qid}' where title = {title};""".format(qid=qid, title = title2)
            if qid == qid_in:
                qua = ''
        #---
        if qua != '' : 
            num += 1
            #---
            # print(qua)
            #---
            all_texts += f'\n{qua}'
            texts += f'\n{qua}'
        #---
        if texts != '':
            if num % 300 == 0:
                print(texts)
                vfg = sql_for_mdwiki.mdwiki_sql(texts, update = True, Prints = False)
                texts = ''        
                #---
                # if 'break' in sys.argv: break
    #---
#---
def add_them_new(table):
    #---
    all_texts = ''
    #---
    texts = ''
    #---
    UPDATE = []
    INSERT = []
    #---
    for title, qid in table.items():
        #---
        qid_in = title_to_qid_in_sql.get(title,'')
        #---
        title2 = py_tools.make_cod(title)
        #---
        qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}';""".format(qid=qid, title = title2)
        #---
        if title in title_to_qid_in_sql:
            qua = """UPDATE qids set qid = '{qid}' where title = {title};""".format(qid=qid, title = title2)
            if qid == qid_in:
                qua = ''
            else:
                UPDATE.append(qua)
        else:
            INSERT.append("""({title}, '{qid}')""".format(qid=qid, title = title2))
        #---
        if qua != '' : 
            num += 1
    #---
    # update_line = ',\n'.join(UPDATE)
    #---
    insert_line = ',\n'.join(INSERT)
    #---
    if insert_line != '':
        qu = 'INSERT INTO qids (title, qid) values\n' + insert_line
        print(qu)
        vfg = sql_for_mdwiki.mdwiki_sql(qu, update = True, Prints = False)
    #---
    if UPDATE != []:
        for up in UPDATE:
            print(up)
            vfg = sql_for_mdwiki.mdwiki_sql(up, update = True, Prints = False)
#---
new_title_qid = {}
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
            
            if not q in qids_list_already:
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
        add_them_new(to_add)
#---
if __name__ == '__main__':
    get_qids()
#---