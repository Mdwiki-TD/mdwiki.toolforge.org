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
import mdwiki_api
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
def log( text,nn ):
    #---
    with codecs.open( public_html + '/find/log/%s.txt' % nn , 'a' , encoding="utf-8") as fff: 
        fff.write( text )
    fff.close()
    #---
def work( title, Find, Replace, nn ):
    #---
    title = title
    #---
    text = mdwiki_api.GetPageText( title )
    new_text = text
    #---
    if Replace.strip() == "empty" :
        Replace = ""
    #---
    if new_text.strip() != '' :
        new_text = new_text.replace( Find , Replace )
    #---
    sus = 'replace %s [[toolforge:mdwiki/qdel.php?job=replace%s|(stop)]] ' % (nn,nn)
    #---
    if new_text != text :
        numbers['done'] += 1
        #---
        vava = {
        "edit": {
            "result": "Success",
            "pageid": 5013,
            "title": "User:Mr. Ibrahem/sandbox",
            "contentmodel": "wikitext",
            "oldrevid": 1272700,
            "newrevid": 1272701,
            "newtimestamp": "2021-12-02T22:46:23Z",
            "watched": ""
        }}
        #---
        vav = mdwiki_api.page_put_new( new_text, sus, title, return_table=True)
        if type(vav) == dict:
            #---
            newrevid = vav.get('edit',{}).get('newrevid',0)
            #---
            line = '"%s":%d,\n' % ( title.replace('"','\\"') , newrevid )
            #---
            with codecs.open( public_html + '/find/log/%s.txt' % nn , 'a' , encoding="utf-8") as fff: 
                fff.write( line )
            fff.close()
            #---
        else:
            print("err type(vav) != dict ")
    else:
        line = '"%s":"no changes",\n' % title.replace('"','\\"')
        log( line, nn )
    #---
def main():
    #pywikibot.output( '*<<lightred>> > main:')
    #---
    nn = ''
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        #---
        if arg == "-rand" : 
            nn = value
        #---
        if arg == "-number" and value.isdigit():
            # if re.match( '^(\d|\d+)$' , value.strip() ) :
            numbers[1] = int(value)
        #---
    print(nn)
    #---
    find = codecs.open(public_html + '/find/%s_find.txt' % nn , 'r', 'utf8').read()
    #---
    replace = codecs.open(public_html + '/find/%s_replace.txt' % nn , 'r', 'utf8').read()
    #---
    with codecs.open( public_html + '/find/log/%s.txt' % nn , 'w' , encoding="utf-8") as fff: 
        fff.write( '' )
    fff.close()
    #---
    with codecs.open( public_html + '/find/log/%s-text.txt' % nn , 'w' , encoding="utf-8") as fff: 
        fff.write( '' )
    fff.close()
    #---
    if 'newlist' in sys_argv:
        Add_pa = {"srsort": "just_match" , "srwhat": "text"}
        #---
        list = mdwiki_api.Search( find, ns="0", srlimit ="max", RETURN_dict=False, addparams = Add_pa )
    else:
        list = mdwiki_api.Get_All_pages( '' )
        #---
    #---
    text = "start work in %d pages." % len(list)
    log( "<span style='font-size:12px'>" + text + "</span>", '%s-text' % str(nn) )
    #---
    num = 0
    #---
    for page in list:
        num += 1
        #---
        if numbers['done'] >= numbers[1] : 
            break
        #---
        work( page , find , replace , nn ) 
    #---
# python py/replace1.py 
#---
if __name__ == "__main__":
    main()
#---
