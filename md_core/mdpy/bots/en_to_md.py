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
#---
'''

#---
from mdpy.bots import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---

'''
#---

#---
enwiki_to_mdwiki = {}
mdwiki_to_enwiki = {}
#---
# Etonogestrel موجودة في ويكي إنجليزية تحويلة إلى المقالة الهدف الموجودة في ويكي ميد
#---
other_qids_json = {}
#---
from mdpy.bots import sql_for_mdwiki
#---
mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
#---
lala = ''
#---
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
def make_mdwiki_list():
    #---
    ffile = project + '/public_html/Translation_Dashboard/Tables/medwiki_to_enwiki.json'
    #---
    # read the file without errors
    try:
        lala = open( ffile , encoding="utf-8-sig").read()
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
make_mdwiki_list()
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