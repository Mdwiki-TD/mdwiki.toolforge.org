#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بعدد الكلمات

python3 pwb.py mdpy/allwords less100
python3 pwb.py /data/project/mdwiki/mdpy/words
python3 pwb.py mdpy/allwords newpages


"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
import os
import re
import string
import time
import sys
#---
import pywikibot
#---
from mdpy import mdwiki_api
#---
from mdcount.links import get_valid_Links
#---
all_words_n = {}
json_file = {}
#---
def get_word_files():
    #---
    global all_words_n, json_file
    #---
    project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
    #---
    if not os.path.isdir(project): project = '/mdwiki'
    #---
    json_file[0] = project + '/public_html/Translation_Dashboard/Tables/allwords.json'
    #---
    all_words_n = json.loads(codecs.open(json_file[0], "r", encoding="utf-8").read())
    #---
#---
get_word_files()
#---
def log(file, table):
    json.dump(table, open(file, 'w'), sort_keys=True)
    #---
    pywikibot.output('<<lightgreen>> %d lines to %s' % ( len(table) , file ) )
#---
Nore = { 1 : False }
for arg in sys.argv:
    if arg in [ 'new', 'listnew', 'less100', 'more400' ] :
        Nore[1] = True
#---
from mdcount.lead import get_lead
#---
def mmain():
    #---
    n = 0
    #---
    limit = 10000
    if 'limit100' in sys.argv : limit = 100
    #---
    vaild_links = get_valid_Links(all_words_n)
    #---
    kkk = { 1 : vaild_links }
    #---
    for x in kkk[1]:
        #---
        n += 1
        #---
        pywikibot.output(' p %d from %d: wordcount for %s' % (n, len(kkk[1]), x) )
        #---
        if n >= limit :     break
        #---
        aword = mdwiki_api.wordcount(x)
        #---
        if aword == 0 :
            aword = mdwiki_api.wordcount( x, srlimit = "500")
        #---
        pywikibot.output('\t\tword:%d' % aword )
        #---
        all_words_n[x] = aword
        #---
        if n == 10 or str(n).endswith('00'):
            log(json_file[0], all_words_n)
        #---
    #---
    log(json_file[0], all_words_n)
#---
if __name__ == '__main__':
    mmain()
    #---
    sys.argv.append('sql')
    #---
    mmain()
#---
