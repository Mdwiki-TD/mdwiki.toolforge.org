#!/usr/bin/python

"""

نسخ التاريخ من الإنجليزية إلى mdwiki


python3 pwb.py mdpy/imp -page:Infertility

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import urllib
import codecs
#---
import pywikibot
#---
import re
import string
#import datetime 
#import dateutil.parser
#import time
import sys
#---
sys_argv = sys.argv or []
#---
import urllib
import urllib.request
import urllib.parse
#---
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
#---
#---
import mdwiki_api

















#---
import requests
Session = requests.Session()
#---
offset = { 1 : 0 }
#---
to_make = {}
#---
#from export import * # export_en_history( title )
#---
def work( title , num , lenth  , From = '' ):
    #---
    pywikibot.output( '-------------------------------------------\n*<<lightyellow>> >%d/%d title:"%s".' % ( num , lenth , title ) )
    #---
    if num < offset[1]:
       return ""
    #---
    exists = mdwiki_api.Find_pages_exists_or_not( [title] )
    #---
    for tit , o in exists.items() :
        if o == False and tit == title :
            pywikibot.output( " page:%s not exists in mdwiki." % title )
            return ""
    #---
    text = mdwiki_api.GetPageText( title )
    #---
    #if '2021' in sys_argv:
        #---
        #FILE_PATH = export_en_history( title )
        #---
        #ing = mdwiki_api.import_history( FILE_PATH , title )
        #---ing = mdwiki_api.import_page( title )
    #else:
    ing = mdwiki_api.import_page( title )
    #---
    if text and text != "":
       # {"import":[{"ns":0,"title":"Kerion","revisions":74}]}
       pywikibot.output( ing )
    #---
    ing_js = {}
    try:
        ing_js = json.loads(ing)
    except:
        print("")
    #---
    done = ing_js.get("import",[])[0].get("revisions",0)
    #---
    pywikibot.output( "<<lightgreen>> imported %d revisions" % done )
    #---
    #uuu = mdwiki_api.page_put_new( text , '' , title , returntrue = True )
    if done > 0 : 
        uuu = mdwiki_api.page_put_new( text , '' , title , returntrue = True )
        #---
        if uuu != True:
            title2 = 'User:Mr._Ibrahem/' + title
            paramse = {
                "action": "edit",
                "format": "json",
                "title": title2,
                "text": text,
                "summary": 'Returns the article text after importing the history',
                #"createonly": 1,
                "utf8": 1
                }
            #---
            mdwiki_api.post( paramse )
            #fd = mdwiki_api.create_Page( text , '' , title2 , False )
               #fd = mdwiki_api.create_Page( text , '' , title2 , False , sleep = 0 )
            #---
for arg in sys_argv:
    arg, sep, value = arg.partition(':')
    #---
    if arg.lower() == 'offset' or arg.lower() == '-offset' and value.isdigit():
        offset[1] = int(value)
#---
def main():
    pywikibot.output( '*<<lightred>> > main:')
    #---
    # python3 imp.py -page:Crohn's_disease
    # python imp.py -newpages:1000
    # python imp.py -newpages:20000
    options = {}
    #---
    page2 = ''
    From = '0'
    #---
    for arg in sys_argv:
        arg, sep, value = arg.partition(':')
        #---
        arg = arg.lower()
        #---
        if arg == "-from": 
            From = py_tools.ec_de_code( value , 'decode' )
        #---
        if arg == "-page2" or arg == "page2" : 
            page2 = py_tools.ec_de_code( value , 'decode' )
        #---
        
    #---
    if page2 != '' and From != '' :
        work( page2 , 0 , 1 , From = From ) 
    #---
    user = ''
    user_limit = '3000'
    #---
    searchlist = {
        "drug" : "insource:/https\\:\\/\\/druginfo\\.nlm\\.nih\\.gov\\/drugportal\\/name\\/lactulose/" ,
        }
    #---
    limite = 'max'
    starts = ''
    #---
    pages = []
    #---
    namespaces = '0'
    newpages = ''
    #---
        
    #---
    for arg in sys_argv:
        arg, sep, value = arg.partition(':')
        #---
        arg = arg.lower()
        #---
        if arg == "-limit" or arg == "limit" : 
            limite = value
        #---
        if arg == "-userlimit" or arg == "userlimit" : 
            user_limit = value
        #---
        if arg == "-page" or arg == "page" : 
            pages.append( value )
        #---
        if arg == 'newpages' or arg == '-newpages':
            newpages = value
        #---
        # python imp.py -ns:0 -usercontribs:Edoderoobot
        # python imp.py -ns:0 -usercontribs:Ghuron
        if arg == "-user" or arg == "-usercontribs" : 
            user = value
        #---
        # python imp.py -start:!
        if arg == 'start' or arg == '-start':
            starts = value
        #---
        if arg == "-ns" : 
            namespaces = value
        #---
        # python imp.py -file:mdwiki/list.txt
        # python3 imp.py -file:mdwiki/list.txt
        if arg == "-file" : 
            text2 = codecs.open(value, 'r', 'utf8')
            text = text2.read()
            for x in text.split("\n") : 
                pages.append( x.strip() )
        #---
        # python imp.py -ns:0 search:drug
        if arg == 'search' :
            if value in searchlist :
                value = searchlist[value]
            #---
            ccc = mdwiki_api.Search( value , ns = "0" , offset='', srlimit ="max" , RETURN_dict = False , addparams = {} )
            for x in ccc : 
                pages.append( x )
        #---
        #---
    #---
    starts = starts
    start_done = starts
    okay = True
    #---
    if starts == 'all' :
        while okay == True :
            #---
            if starts == start_done :
                okay = False
            #---
            # python imp.py -start:all
            # 
            #---
            list = mdwiki_api.Get_All_pages( '' , namespace = namespaces, limit = limite )
            start_done = starts
            num = 0
            for page in list:
                num += 1
                work( page , num , len(list) ) 
                #---
                starts = page
    #---
    if starts != '' :
        listen = mdwiki_api.Get_All_pages( starts , namespace = namespaces, limit = limite )
        num = 0
        for page in listen:
            num += 1
            work( page , num , len(listen) ) 
            #---
    #---
    list = []
    #---
    if newpages != "":
        list = mdwiki_api.Get_Newpages( limit = newpages , namespace = namespaces )
    elif user != "":
        list = mdwiki_api.Get_UserContribs( user , limit = user_limit , namespace = namespaces , ucshow = "new" )
    elif pages != []:
        list = pages
    #---
    num = 0
    for page in list:
        num += 1
        work( page , num , len(list) ) 
    #---
    #'''
    #---
    if starts == 'all' :
        while okay == True :
            #---
            if starts == start_done :
                okay = False
            #---
            # python imp.py -start:all
            # 
            #---
            list = mdwiki_api.Get_All_pages( '' , namespace = namespaces, limit = limite )
            start_done = starts
            num = 0
            for page in list:
                num += 1
                work( page , num , len(list) ) 
                #---
                starts = page
    #---
    elif starts != '' :
        #while start_done != starts :
        while okay == True :
            #---
            if starts == start_done :
                okay = False
            #---
            # python3 imp.py -start:! -limit:3
            # 
            #---
            list = mdwiki_api.Get_All_pages( starts , namespace = namespaces, limit = limite )
            start_done = starts
            num = 0
            for page in list:
                num += 1
                work( page , num , len(list) ) 
                #---
                starts = page
#---
# python imp.py
#---
if __name__ == "__main__":
    main()
#---
