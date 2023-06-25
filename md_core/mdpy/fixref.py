#!/usr/bin/python
"""
Change refs to newlines
python3 core8/pwb.py mdpy/fixref
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import json
import urllib
import codecs
import pywikibot
import re
import sys
import os
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
#---
from mdpy import printe
from mdpy.bots import mdwiki_api
from mdpy.bots import txtlib2
#---
thenumbers = { 1 : 20000 , 'done' : 0 }
#---
def add_new_Line( text ) :
    ingr = txtlib2.extract_templates_and_params(text)
    newtext = text
    #---
    for temp in ingr:
        name = temp['name']
        params = temp['params']
        template = temp['item']
        #---
        printe.output( "----------------------------------------------------------------" )
        printe.output( "template (%s) is :" % name )
        #---
        newtemp = template
        #---
        newtemp = re.sub(r'(\{\{\s*%s)\s*(\|)' % re.escape(name) , '\g<1>\n\g<2>' , newtemp )
        #---
        for x in params:
            #---
            value = params[x]
            #---
            if value.find( '%s' ) != -1 :
                printe.output('**<<lightred>> value(%s).find(%s) != -1 ' % ( value , '%s' ) )
                continue
            #---
            value = str(value)
            value = re.escape(value)
            x = re.escape(x)
            newtemp = re.sub(r"\|\s*(%s)\s*\=\s*(%s)\s*" % (x,value) , "| \g<1> = \g<2>" , newtemp, flags=re.IGNORECASE )
        #---
        if newtemp != template :
            newtext = newtext.replace( template , newtemp )
    #---
    return newtext
#---
def remove_new_Line( text ) :
    newtext = text
    #---
    ingr = txtlib2.extract_templates_and_params(text)
    #---
    for temp in ingr:
        #---
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        #---
        printe.output( "----------------------------------------------------------------" )
        printe.output( "template (%s) is :" % namestrip )
        #---
        newtemp = template
        #---
        newtemp = re.sub(r'(\{\{\s*%s\s*)\n*(\|)' % re.escape(namestrip) , '\g<1>\g<2>' , newtemp )
        newtemp = re.sub(r'\n\s*\|', '|' , newtemp, flags=re.DOTALL)
        #---
        for x in params:
            #---
            value = params[x]
            #---
            value = re.escape(value)
            x = re.escape(x)
            newtemp = re.sub(r"(\|\s*%s\s*\=\s*)(%s)\s*" % (x,value) , "\g<1>\g<2>" , newtemp, flags=re.DOTALL)
        #---
        newtemp = re.sub(r'\n\s*\}\}\s*$', '}}', newtemp)
        #---
        if newtemp != template :
            newtext = newtext.replace( template , newtemp )
    #---
    return newtext
#---
def fix_ref_template( text ) :
    regref = re.compile( r'(?i)(?P<params><ref[^>/]*>)(?P<content>.*?)</ref>' , re.IGNORECASE|re.DOTALL)
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
        if content.find('{{Cite') == -1 and content.find('{{cite') == -1 :
            continue
        #---
        if newtext.find(content) != -1 :
            content2 = remove_new_Line( content )
            if content2 != content :
                bbb = aaa.replace( content , content2 )
                newtext = newtext.replace( aaa , bbb )
    #---
    return newtext
#---
def work( title ):
    #---
    Ask = False
    if 'ask' in sys.argv: Ask = True
    #---
    text = mdwiki_api.GetPageText( title )
    #---
    new_text = fix_ref_template( text )
    #---
    summary = 'Normalize references'
    #---
    if new_text != text :
        thenumbers['done'] += 1
        #---
        mdwiki_api.page_put(oldtext=text, newtext=new_text, summary=summary, title=title, returntrue=False, diff=True)
    else:
        printe.output( 'no changes.')
    #---
def main():
    #---
    List = []
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        #---
        if arg == '-number' and value.isdigit():
            thenumbers[1] = int(value)
        #---
        if arg == '-file':
            text = codecs.open(project + '/public_html/find/%s' % value.strip() , 'r', 'utf8').read()
            List = [ x.strip() for x in text.split('\n') if x.strip() != '' ]
        #---
        if arg == 'allpages':
            List = mdwiki_api.Get_All_pages( '' )
        #---
        # python pwb.py mdwiki/mdpy/fixref -page:Histrelin ask
        if arg in ['-page', '-title']:
            List = [ value ]
        #---
    #---
    num = 0
    for title in List:
        num += 1
        #---
        if thenumbers['done'] >= thenumbers[1] and len(List) > 1:
            break
        work( title ) 
    #---
#---
if __name__ == "__main__":
    main()
#---
