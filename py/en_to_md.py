#!/usr/bin/python

"""
11p deletion syndrome
Vulvar pain
Diabetic foot infection
Kidney agenesis
Orbital compartment syndrome
Pelvic floor disorders
Perianal itching
Genital itch
Lateral canthotomy
Prostate abscess

# Etonogestrel موجودة في ويكي إنجليزية تحويلة إلى المقالة الهدف الموجودة في ويكي ميد

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import codecs
import sys
import os
import json
import time
import py_tools
#---
'''

#---
import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---

'''
#---
sys_argv = sys.argv or []
#---
enwiki_to_mdwiki = {}
mdwiki_to_enwiki = {}
#---
# Etonogestrel موجودة في ويكي إنجليزية تحويلة إلى المقالة الهدف الموجودة في ويكي ميد
#---
other_qids_json = {}
#---
mdtitle_to_qid = {}
#---
import sql_for_mdwiki
#---
sq = sql_for_mdwiki.mdwiki_sql(' select DISTINCT title, qid from qids;')
#---
for ta in sq: 
    title = py_tools.Decode_bytes(ta[0])
    qqid = py_tools.Decode_bytes(ta[1])
    if qqid != '':
        mdtitle_to_qid[title] = qqid
#---
lala = ''
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
def make_mdwiki_list():
    #---
    ffile = project + '/public_html/Translation_Dashboard/Tables/medwiki_to_enwiki.json'
    #---
    # read the file without errors
    try:
        lala = open( ffile , "r", encoding="utf-8-sig").read()
    except Exception as e:
        print(e)
    #---
    fa = str(lala)
    #---
    if fa != '' : 
        From_json = json.loads(fa)
        #---
        for md,en in From_json.items():
            enwiki_to_mdwiki[en] = md
            #---
            mdwiki_to_enwiki[md] = en
#---
def make_qids_list():
    mdwiki_to_qid_file = project + '/public_html/Translation_Dashboard/Tables/mdwiki_to_qid.json'
    #---
    to_qids_text = ""
    #---
    try:
        to_qids_text = open( mdwiki_to_qid_file , "r", encoding="utf-8-sig").read()
        mdtitle_to_qid = json.loads(to_qids_text)
    except Exception as e:
        print("error when open mdwiki_to_qid.json: " + str(e))
        time.sleep(4)
    #---
    json_file = project + '/public_html/Translation_Dashboard/Tables/other_qids.json'
    # load json file
    #---
    try:
        with open(json_file) as f:
            other_qids_json = json.load(f)
        f.close()
    except Exception as e:
        print("error when open file: %s " % json_file)
        print(str(e))
        time.sleep(4)
    #---
    for ee, q in other_qids_json.items():
        if q != "":
            mdtitle_to_qid[ee] = q
#---
make_mdwiki_list()
# make_qids_list()
#---
if __name__ == "__main__":
    text = ''
    for x, q in mdtitle_to_qid.items():
        line = f'\n{q}\tP11143\t"{x}"'
        print(line.strip())
        text += line
    #---
    with open( project + '/uu.txt' , "w", encoding="utf-8-sig") as f:
        f.write(text)