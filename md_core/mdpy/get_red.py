#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
""" 

python3 core8/pwb.py mdpy/get_red

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

#---
#---
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = '/mdwiki'
from mdpy.bots import py_tools
from mdpy.bots import en_to_md
from mdpy import printe
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---
mdwiki_to_qid = en_to_md.mdtitle_to_qid
#---
from mdpy.bots import mdwiki_api
#---
def get_pages():
    #---
    splits = py_tools.split_lists_to_numbers( mdwiki_to_qid.keys() )
    #---
    table = {}
    #---
    num = 0
    #---
    for n, lis in splits.items():
        #---
        asa = mdwiki_api.get_redirect(lis)
        #---
        print('work on %d pagees.' % len(lis) )
        #---
        for red, target in asa.items():
            #---
            table[red] = target
            #---
    #---
    print('len of table %d ' % len(table))
    #---
    tat = ''
    #---
    rep = 0
    remo = 0
    #---
    to_add = {}
    to_del = []
    #---
    for old_title, new_title in table.items():
        ll = f'"old_title: {old_title}" to: "{new_title}",\n'
        #---
        t_q = mdwiki_to_qid.get(new_title, False)
        r_q = mdwiki_to_qid.get(old_title, False)
        #---
        if r_q: 
            if not t_q:
                # استبدال
                rep += 1
                #---
                printe.output('<<lightyellow>>' + ll.strip() )
                #---
                to_del.append(old_title)
                to_add[new_title] = r_q
                #---
                del mdwiki_to_qid[old_title]
                mdwiki_to_qid[new_title] = r_q
                #---
                tat += ll
                #---
            elif t_q == r_q:
                remo += 1
                to_del.append(old_title)
                del mdwiki_to_qid[old_title]
    #---
    printe.output('===================' )
    if tat != '':
        printe.output('<<lightred>> redirects: ' )
        printe.output(tat)
        printe.output('===================' )
    #---
    printe.output('replace %d pages. ' % rep)
    printe.output('remove %d pages. ' % remo)
    #---
    if len(to_del) > 0:
        printe.output('delete %d pages. ' % len(to_del))
        printe.output(to_del)
    #---
    if len(to_add) > 0:
        printe.output('add %d pages. ' % len(to_add))
        printe.output(to_add)
    #---
    if 'fix' in sys.argv:
        back_up = json.load(open(project + '/public_html/Translation_Dashboard/Tables/mdwiki_to_qid.json'))
        #---
        with open( project + '/public_html/Translation_Dashboard/Tables/mdwiki_to_qid_back_up.json', 'w') as uuu:
            json.dump(back_up, uuu)
        uuu.close()
        #---
        with open( project + '/public_html/Translation_Dashboard/Tables/mdwiki_to_qid.json', 'w') as uuu:
            json.dump(mdwiki_to_qid, uuu)
        uuu.close()
#---
if __name__ == '__main__':
    get_pages()
#---