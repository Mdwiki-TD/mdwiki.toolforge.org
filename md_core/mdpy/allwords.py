#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بعدد الكلمات

python3 pwb.py mdpy/allwords less100
# python3 pwb.py /data/project/mdwiki/mdpy/words
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
#---
#import pywikibot
#---
import re
import string
#import datetime 
#import dateutil.parser
import time
#from datetime import datetime, date
#menet = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
import sys
#---
sys_argv = sys.argv or []
#---
import pywikibot
#---
# start of mdwiki_api.py file
import mdwiki_api


















#---
all_words = {}
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
import catdepth2
#---
vaild_links = { 1 : {} }
#---
allword_file = project + '/public_html/Translation_Dashboard/Tables/allwords.json'
#---
all_words = json.loads(codecs.open(allword_file, "r", encoding="utf-8").read())
#---
def Decode_bytes(x):
    if type(x) == bytes:
        x = x.decode("utf-8")
    return x
#---
def logaa():
    with open( allword_file , 'w') as outfile:
        json.dump( all_words, outfile, sort_keys = True )
    outfile.close()
    #---
    pywikibot.output('<<lightgreen>> %d lines to %s' % ( len(all_words) , allword_file ) )
#---
def get_valid_Links():
    #---
    tabe = catdepth2.subcatquery2( 'RTT' , depth = '3' , ns = '0' )
    #---
    vav = tabe['list']
    #---
    if 'newpages' in sys_argv:
        dada = [ t for t in vav if ( not t in all_words or all_words[t] == 0 ) ]
        vav = dada
    #---
    for x in vav:
        if x.startswith('Category:') :
            vav.remove(x)
    #---
    pywikibot.output( 'Get words for :%d titles.' % len(vav) )
    return vav
#---
def from_sql():
    #---
    que = '''select title, word from pages;'''
    #---
    sq = sql_for_mdwiki.mdwiki_sql(que)
    #---
    titles = []
    #---
    for tab in sq :
        title  = Decode_bytes(tab[0])
        word  = Decode_bytes(tab[1])
        #---
        titles.append(title)
        #---
    #---
    pywikibot.output( '<<lightyellow>> find %d to work from sql. ' % len(titles) )
    return titles
#---
def mmain():
    #---
    n = 0
    #---
    limit = 10000
    if 'limit100' in sys.argv : limit = 100
    #---
    #---
    if 'sql' in sys.argv:
        vai2 = from_sql()
        vaild_links[1] = [ t for t in vai2 if (not t in all_words or all_words[t] < 50) ]
        pywikibot.output('ALL SQL LINKS:%d, to work:%d' % (len(vai2), len(vaild_links[1]) ) )
    #---
    else:
        vaild_links[1] = get_valid_Links()
    #---
    for x in vaild_links[1]:
        #---
        n += 1
        #---
        pywikibot.output(' p %d from %d: wordcount for %s' % (n, len(vaild_links[1]), x) )
        #---
        if x.startswith('Category:') : continue
        #---
        if n >= limit : 
            break
        #---
        aword = mdwiki_api.wordcount(x)
        #---
        if aword == 0 :
            aword = mdwiki_api.wordcount( x, srlimit = "500")
        #---
        pywikibot.output('\t\tword:%d' % aword )
        #---
        all_words[x] = aword
        #---
        if n == 10 or str(n).endswith('00'):
            logaa()
        #---
    #---
    logaa()
#---
if __name__ == '__main__':
    mmain()
#---
