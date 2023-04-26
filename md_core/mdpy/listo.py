#!/usr/bin/python

"""

Pages in WikiProjectMed:List missing Category:RTT

تحديث صفحة User:Mr. Ibrahem/List

python mdwiki/mdpy/listo.py save

python3 /data/project/mdwiki/md_core/mdpy/listo.py save

python3 /data/project/mdwiki/core/pwb.py mdpy/listo save

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
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

#---
import urllib
import urllib.request
import urllib.parse
#---
#---
from mdpy import mdwiki_api

















#---
#import requests
#Session = requests.Session()
#---#---
#---
limit_m = { 1 : 0 }
#---
for arg in sys_argv:
    arg, sep, value = arg.partition(':')
    #---
    if arg.lower() == 'li' or arg.lower() == '-li' and value.isdigit():
        limit_m[1] = int(value)
#---
redirects_pages = []
#---
if not 'nored' in sys.argv:
    redirects_pages = mdwiki_api.Get_All_pages( '!' , namespace = '0', apfilterredir = 'redirects', limit_all = limit_m[1] )
#---
dones = []
links = []
re_links = []
#---
ptext = mdwiki_api.GetPageText( 'WikiProjectMed:List' )
link_regex = re.compile(r'\[\[(.*?)\]\]')
#---
vaild_links = []
#---
for m2 in link_regex.finditer(ptext):
    sa = re.compile('\[\[(\:|)(\w{2}|\w{3}|w|en|image|file|category|template)\:', flags=re.IGNORECASE )
    sal = sa.findall(m2.group(0))
    if not sal:
        itemu = m2.group(1).split('|')[0].strip()
        vaild_links.append( itemu )
#---
print('len of vaild_links: %d' % len(vaild_links) )
#---
for x in vaild_links:
    x1 = x
    x2 = x#.replace(x[0], x[0].upper() , 1)
    if x1 != x2 : print('x1:%s,x2:%s' % (x1,x2) )
    if not x2 in dones: 
        dones.append( x2 )
        if x2 in redirects_pages or x1 in redirects_pages:
            re_links.append( x2 )
        else:
            links.append( x2 )
#---
print('len of re_links: %d' % len(re_links) )
print('len of links: %d' % len(links) )
#print(str(links))
#---
catpages = mdwiki_api.subcatquery( 'Category:RTT' , depth = '0' , ns = "0" )
catpages = [ x.replace('_',' ') for x in catpages ]
#catpages = mdwiki_api.Get_cat( 'RTT', '0' )
#---
print('len of catpages: %d' % len(catpages) )
if 'Biceps tendon rupture' in catpages:
    print('Biceps tendon rupture in catpages')
# print(str(catpages))
#---
listo = [ x for x in links if not x in catpages ]
#---
re_listo = [ d for d in re_links if not d in catpages ]
num = 0
#---
print('len of listo: %d' % len(listo) )
#---
lines = "\n".join( [ '# [[%s]]' % x for x in listo ] )
text = '''Pages in [[WikiProjectMed:List]] missing [[:Category:RTT]]:
--~~~~
__TOC__

== Articles ==
'''
text += lines
#---
text += "\n\n== Redirects ==\n\n"
#---
text += "\n".join( [ '# [[%s]]' % dx for dx in re_listo ] )
#---
print(text)
#---
mdwiki_api.page_put( newtext=text , summary='update' , title='User:Mr. Ibrahem/List' , nocreate = 0 )
#---
