#!/usr/bin/python

"""

إيجاد الصفحات القديمة
تحديث صفحة User:Mr. Ibrahem/pages

python3 mdpy/io.py test 

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
#---
print_pywikibot = { 1 : False }
try:
    import pywikibot
    print_pywikibot[1] = True
except:
    print_pywikibot[1] = False
#---
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
import os
import urllib
import urllib.request
import urllib.parse
#---
#---
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = 'I:/mdwiki'
#---
#---
from mdpy import mdwiki_api

















#---
#import requests
#Session = requests.Session()
#---
def outbotnew( s ):
    if s == '' : return '' 
        #pywikibot.output( s )
    if print_pywikibot[1] :
        pywikibot.output( s )
    else:
        print( s )
#---
NewList = {}
#---
fska = codecs.open( project + '/md_core/mdpy/date_before_20200701.txt' , "r", encoding="utf-8") .read()
fakalist = fska.split('\n')
fakalist = [ x.strip().split(']]')[0].replace('[[','').strip() for x in fakalist ]
#---
listo = mdwiki_api.Get_All_pages( '!' , namespace = '0' )
listo = [  x for x in listo  if not  x in fakalist ]
num = 0
if 'test' in sys_argv: listo = listo[:100]
#---
if '200' in sys_argv: listo = listo[:200]
#---
outbotnew('len of listo: %d' % len(listo) )
#---
for page in listo:
    num += 1
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": page,
        "rvprop": "timestamp",
        "rvlimit": "1",
        "rvdir": "newer"
    }
    hh = mdwiki_api.post(params)
    #---
    #{"continue":{"rvcontinue":"20041026150441|715742","continue":"||"}, "query":{"pages" :{"5089": {"pageid":5089,"ns":0,"title":"Zopiclone","revisions":[{"timestamp":"2004-10-25T15:57:14Z"}]}}}}
    #date = ''
    #---
    kk = hh.get("query",{}).get("pages",{})
    for key, vav in kk.items():
        # {'pageid': 55693, 'ns': 0, 'title': '1-Docosanol', 'revisions': [{'timestamp': '2021-03-26T21:04:02Z'}]}
        # key = list(kk.keys())[0]
        timestamp = vav.get("revisions",[{'timestamp': ''}])[0].get("timestamp",'')
        NewList[page] = timestamp
        break
    #---
    # print(sddd)
    #---
    if str(num).endswith('00') : outbotnew( 'page:%d:%s,timestamp:%s' % (num,page,timestamp) )
    #---
# 2004-07-18T21:51:19Z
#---
laly = [ [int( io.split('T')[0].replace('-','') ) , x ] for x  , io in NewList.items() ] 
laly.sort( reverse = True )
#---
outbotnew( 'has %d pages. ' % len(laly) )
#---
new = [ [ z , g ] for z,g in laly if z > 20200701 ] 
new.sort( reverse = True )
#---
old = [ [ z , g ] for z,g in laly if z < 20200701 ] 
old.sort( reverse = True )
#---
outbotnew( 'we have %d pages with date > 20200701. ' % len(new) )
outbotnew( 'we have %d pages with date < 20200701. ' % len(old) )
#---
#masha = '\n'.join( [ "[[%s]]\t%d" % (s,d) for d,s in new ] )
masha = '\n'.join( [ "%s" % s for d,s in new ] )
#---
with codecs.open( project + '/md_core/mdpy/date_after_20200701.txt' , "w", encoding="utf-8") as logfil3e:
    logfil3e.write( masha )
logfil3e.close()
#---
masha3 = '\n'.join( [ "%s" % ss for ds,ss in old ] )
#---
with codecs.open( project + '/md_core/mdpy/date_before_20200701.txt' , "w", encoding="utf-8") as ooo:
    ooo.write( masha3 )
ooo.close()
#---
text = '''
--~~~~
{| class="wikitable sortable"
|-
! #
! Title
! Creation date
! Import history
'''
numb = 0
for Date , pag in new : 
    numb += 1
    url = 'https://' + 'yemen.toolforge.org/med/import-history.php?code=James%2399&title={{urlencode:' + pag + '}}'
    text += '|-\n| %d || [[%s]] || %s || [%s ] \n' % ( numb , pag , Date , url )

text += '''|-
|}
'''
if 'test' in sys_argv:
    outbotnew( text )
else:
    mdwiki_api.page_put( newtext=text , summary='update' , title='User:Mr. Ibrahem/pages' )
#---
