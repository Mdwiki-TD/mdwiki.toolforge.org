#!/usr/bin/python

"""

python3 pwb.py py/copy_word_table

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
import sql_for_mdwiki 
# from sql import *
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
# py_tools.
# py_tools.
# py_tools.
#---
que = '''select DISTINCT w_title, w_lead_words, w_all_words from words;'''
#---
in_sql_lead = {}
in_sql_all = {}
#---
for q in sql_for_mdwiki.mdwiki_sql(que):
    #---
    w_title     = py_tools.Decode_bytes(q[0])
    w_lead_words= py_tools.Decode_bytes(q[1])
    w_all_words = py_tools.Decode_bytes(q[2])
    #---
    in_sql_lead[w_title] = w_lead_words
    in_sql_all[w_title] = w_all_words
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
if not os.path.isdir(project): project = '/mdwiki'
#---
lead_words = json.loads(codecs.open(project + '/public_html/Translation_Dashboard/Tables/words.json',    "r", encoding="utf-8").read())
all_words  = json.loads(codecs.open(project + '/public_html/Translation_Dashboard/Tables/allwords.json', "r", encoding="utf-8").read())
#---
new_words = {}
#---
# list for titles in both all_ref and lead_ref
# na_list = list( set(all_words.keys()) & set(lead_words.keys()) )
na_list = [ x for x in all_words.keys() ]
#---
for x in lead_words.keys():
    if not x in na_list : na_list.append(x)
#---
# remove duplicates from list
# na_list = list(set(na_list))
#---
len_all = len(na_list)
#---
UPDATE = []
INSERT = []
#---
num = 0
same = 0
#---
for tit in na_list:
    #---
    lead = lead_words.get(tit, 0)
    All  = all_words.get(tit, 0)
    #---
    sql_lead = in_sql_lead.get(tit)
    sql_all  = in_sql_all.get(tit)
    #---
    num += 1
    #---
    title2 = py_tools.make_cod(tit)
    #---
    qua = """INSERT INTO words (w_title, w_lead_words, w_all_words) SELECT {title}, {lead}, {All}
    WHERE NOT EXISTS ( SELECT 1 FROM words  WHERE w_title = {title} );
    
    UPDATE words SET w_lead_words = {lead}, w_all_words = {All} WHERE w_title = {title};
    """.format(title = title2, lead = lead, All = All)
    #---
    qua_update = """UPDATE words SET w_lead_words = {lead}, w_all_words = {All} WHERE w_title = {title};""".format(
        title = title2, lead = lead, All = All
    )
    #---
    # pywikibot.output( f'n:{num} / {len_all}\t:{title} \t:: lead:{lead}\t all: {All}' )
    #---
    if not tit in in_sql_lead:
        qua_new = """({title}, {lead}, {All})""".format(title = title2, lead = lead, All = All)
        INSERT.append(qua_new)
    else:
        if sql_lead != lead or sql_all != All:
            if lead > 10 and All > 10:
                UPDATE.append(qua_update)
        else:
            same += 1
#---
texts = []
#---
n = 0
#---
for qu in UPDATE:
    #---
    n += 1
    #---
    texts.append(qu)
    #---
    if len(texts) % 50 == 0 or n == len(UPDATE):
        tt = "\n".join(texts)
        #---
        print('====')
        print('%d run sql for %s lines.' % (n, len(texts) ) )
        #---
        print(tt)
        #---
        vfg = sql_for_mdwiki.mdwiki_sql(tt, update=True, Prints=True)
        #---
        texts = []
        #---
        if 'break' in sys.argv: break
#---
if INSERT != []:
    insert_line = ',\n'.join(INSERT)
    #---
    qu = 'INSERT INTO words (w_title, w_lead_words, w_all_words) values\n' + insert_line
    print(qu)
    vfg = sql_for_mdwiki.mdwiki_sql(qu, update=True, Prints=True)
#---
print(f'len lead_words from file: {len(lead_words)}')
print(f'len all_words from file: {len(all_words)}')
#---
print(f'len sql titles: {len(in_sql_lead)}')
print(f'pages with same values in sql and file: {same}')
#---