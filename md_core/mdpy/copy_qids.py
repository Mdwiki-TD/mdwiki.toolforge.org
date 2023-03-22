#!/usr/bin/python

"""

python3 pwb.py mdpy/copy_qids

delete from qids q1 WHERE q1.qid = '' and EXISTS  (SELECT 1 FROM qids q2 WHERE q1.title = q2.title and q2.qid != '')

"""
#
# (C) Ibrahem Qasim, 2022
#
#
#---
import codecs
import os
import json
import sys
import pywikibot
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
# from sql import *
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
#---
in_qids = sql_for_mdwiki.get_all_qids()
#---
if 'rr' in sys.argv: sys.exit()
#---
len_qids_empty = len( [ x for x in in_qids if in_qids[x].find('Q') == -1 ] )
len_qids_not_empty = len( [ x for x in in_qids if in_qids[x] != '' ] )
#---
print(f'len_qids_empty = {len_qids_empty}')
print(f'len_qids_not_empty = {len_qids_not_empty}')
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
if not os.path.isdir(project): project = '/mdwiki'
#---
import en_to_md
# en_to_md.mdtitle_to_qid
qids_list = en_to_md.mdtitle_to_qid
#---
num = 0
#---
all_texts = ''
texts = ''
#---
print(f'len(qids_list) = {len(qids_list)}')
#---
for title, qid in qids_list.items():
    #---
    qid_in = in_qids.get(title,'')
    #---
    # qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}' WHERE NOT EXISTS ( SELECT 1 FROM qids q2 WHERE q2.title = {title});""".format(qid=qid, title = py_tools.make_cod(title))
    qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}';""".format(qid=qid, title = py_tools.make_cod(title))
    #---
    if title in in_qids:
        qua = """UPDATE qids set qid = '{qid}' where title = {title};""".format(qid=qid, title = py_tools.make_cod(title))
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
if texts != '':
    print(texts)
    vfg = sql_for_mdwiki.mdwiki_sql(texts, update = True, Prints = False)
#---
# log all_texts
with codecs.open(f'{project}/md_core/mdpy/copy_qids.txt', 'w', 'utf-8') as f:
    f.write(all_texts)
#---