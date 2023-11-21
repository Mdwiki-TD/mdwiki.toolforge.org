#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بعدد الكلمات

python3 pwb.py TDpy/allwords less100
# python3 pwb.py /data/project/mdwiki/TDpy/words
python3 pwb.py TDpy/allwords newpages


"""
#
# (C) Ibrahem Qasim, 2021
#
#
from __future__ import absolute_import, unicode_literals
import json
import urllib
import codecs
import os

# ------
# import pywikibot
# from pywikibot import textlib
# ------
import re
import string

# import datetime
# import dateutil.parser
import time

# from datetime import datetime, date
# menet = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
import sys

# ------
sys_argv = sys.argv or []
# ------
# ======
print_pywikibot = {1: False}
try:
    import pywikibot

    print_pywikibot[1] = True
except:
    print_pywikibot[1] = False
# ======
# ------
import mdapi

# mdapi.submitAPI( params )
# mdapi.GetPageText( title )
# mdapi.wordcount( title, ns = '', srlimit ="100" )
# mdapi.
# ------
# ======
all_words = {}
# ======
# ------
# ------
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
# ------
if not os.path.isdir(project):
    project = '/mdwiki'
# ------
# ------
file = project + '/public_html/Translation_Dashboard/Tables/allwords.json'
# ------
with codecs.open(file, "r", encoding="utf-8") as haha:
    all_words = json.load(haha)
haha.close()


# ======
def logaa():
    with open(file, 'w') as outfile:
        json.dump(all_words, outfile, sort_keys=True)
    outfile.close()
    # ------
    pywikibot.output('<<lightgreen>> %d lines to %s' % (len(all_words), file))
    # pywikibot.output('<<lightgreen>> len old all_words %d' % len_old )


# ======
import catdepth2

tabe = catdepth2.subcatquery2('RTT', depth='3', ns='0')
# ======
vaild_links = {1: tabe['list']}
# ======
if 'newpages' in sys_argv:  # vaild_links
    dada = [t for t in vaild_links[1] if (not t in all_words or all_words[t] == 0)]
    vaild_links[1] = dada
# ======
for x in vaild_links[1]:
    if x.startswith('Category:'):
        vaild_links[1].remove(x)
# ======
pywikibot.output('Get words for :%d titles.' % len(vaild_links[1]))


# ======
def mmain():
    # ======
    n = 0
    # ======
    limit = 10000
    if 'limit100' in sys.argv:
        limit = 100
    # ======
    for x in vaild_links[1]:
        # ------
        n += 1
        # ------
        pywikibot.output(' p %d from %d: wordcount for %s' % (n, len(vaild_links[1]), x))
        # ------
        if x.startswith('Category:'):
            continue
        # ------
        if n >= limit:
            break
        # ------
        aword = mdapi.wordcount(x)
        # ------
        if aword == 0:
            aword = mdapi.wordcount(x, srlimit="500")
        # ------
        pywikibot.output('\t\tword:%d' % aword)
        # ------
        all_words[x] = aword
        # ------
        if n == 10 or str(n).endswith('00'):
            logaa()
        # ------
    # ======
    logaa()
    # ======


# ======
if __name__ == '__main__':
    mmain()
# ======
