#!/usr/bin/python

"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import codecs
import json
import re
import string
import sys
sys_argv = sys.argv or []
#---
from mdpy import mdwiki_api

















#---
numbers = { 1 : 20000 , 'done' : 0 }
#---
import os
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
public_html = project + '/public_html'
#---
def work( title ):
    #---
    
    #---
    text = mdwiki_api.GetPageText( title )
    #---
    # <templatestyles src="Owid/styles.css"/><ourworldindatamirror>cumulative-covid-cases-region</ourworldindatamirror>
    #---
    regref = re.compile( r'<templatestyles\s*src="Owid/styles.css"\s*/\s*>\s*<ourworldindatamirror>(?P<content>.*?)</ourworldindatamirror>' , re.IGNORECASE | re.DOTALL)
    #---
    newtext = text
    #---
    for match in regref.finditer(text):
        #---
        aaa = match.group()
        #---
        content = match.group('content')
        if not content.strip():
            continue
        #---
        content = content.strip()
        #---
        if newtext.find(content) != -1 :
            newtext = newtext.replace( aaa, '{{ourworldindatamirror|%s}}' % content )
    #---
    sus = 'fix ourworldindatamirror'
    #---
    if newtext != text :
        numbers['done'] += 1
        #---
        vav = mdwiki_api.page_put_new( newtext, sus, title )
#---
def main():
    nn = ''
    #---
    list = mdwiki_api.Get_All_pages( 'COVID' )
    #---
    num = 0
    #---
    for page in list:
        num += 1
        #---
        if numbers['done'] >= numbers[1] :  break
        #---
        work( page ) 
    #---
# python py/replace1.py 
#---
if __name__ == "__main__":
    main()
#---
