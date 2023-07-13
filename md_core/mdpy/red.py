#!/usr/bin/python

"""

نسخ التحويلات من الإنجليزية إلى mdwiki

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
#import dateutil.parser
import time
#import datetime
#from datetime import datetime, date
#menet = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
import sys
#---

#---
import urllib
import urllib.request
import urllib.parse
#---
#---
from mdpy.bots import py_tools


#---
#---
from mdpy.bots import mdwiki_api
from mdpy import printe
import requests
Session = requests.Session()
#---
offset = { 1 : 0 }
#---
def get_red( title ):
    #---
    params = {
        "action": "query",
        "format": "json",
        "prop": "redirects",
        "titles": title,
        "utf8": 1,
        "rdprop": "title",
        #"rdprop": "pageid|title",
        "rdlimit": "max"
    }
    #---
    result = {
        "batchcomplete": "",
        "query": {
            "pages": {
                "1369": {
                    "pageid": 1369,
                    "ns": 0,
                    "title": "اليمن",
                    "redirects": [
                        {
                            "ns": 0,
                            "title": "جمهورية يمنية"
                        }
                    ]
                }
            }
        },
        "limits": {
            "redirects": 500
        }
        }
    #---
    list = []
    #---
    r22 = Session.post( 'https://' + 'en.wikipedia.org/w/api.php' , data = params )
    json1 = r22.json()
    #---
    pages = json1.get('query',{}).get('pages',{})
    #---szs
    for x in pages:
        title = pages[x].get('title','')
        redirectsn = pages[x].get('redirects',[])
        printe.output( redirectsn )
        if pages[x]["title"] == title : 
            for io in redirectsn:
                if io["ns"] != 0: continue
                #---
                if not io["title"] in list: list.append( io["title"] )
    #---
    return list
#---
to_make = {}
#---
def work( title , num , lenth ):
    #---
    printe.output( '-------------------------------------------\n*<<lightyellow>> >%d/%d title:"%s".' % ( num , lenth , title ) )
    #---
    exists = mdwiki_api.Find_pages_exists_or_not( [title] )
    #---
    for tit , o in exists.items() :
        if o == False and tit.lower() == title.lower() :
            printe.output( " page:%s not exists in mdwiki." % title )
            return ""
    #---
    if num < offset[1]:
       return ""
    #---
    redirects = get_red( title )
    printe.output( redirects )
    #---
    text = '#redirect [[%s]]' % title
    sus = 'Redirected page to [[%s]]' % title
    #---
    ing = mdwiki_api.Find_pages_exists_or_not( redirects )
    #---
    #for tit in redirects:
        #mdwiki_api.create_Page( text , sus , tit , False , family = "mdwiki" , sleep= 1)
    #---
    num = 0 
    for tit , o in ing.items() :
        num += 1
        if o == False :
            #---
            okay = True
            listr = [ 'user:' , 'category:' , 'template:' , 'wikipedia:' ]
            #---
            tit2 = tit.lower()
            #---
            for iof in listr :
                if tit2.startswith(iof) :
                    okay = False
                    printe.output( " tit2.startswith('%s') " % iof )
            #---
            if okay:
                mdwiki_api.create_Page( text , sus , tit , False , family = "mdwiki" , sleep = 1)
            #---
        else:
            printe.output( "page n:%d, title:'%s' already in mdwiki.org.." % (num,tit) )
    #---
 #   printe.output("sleep 5 s")
#    time.sleep(5)
    #---
#---
for arg in sys.argv:
    arg, sep, value = arg.partition(':')
    #---
    if arg.lower() == 'offset' or arg.lower() == '-offset' and value.isdigit():
        offset[1] = int(value)
#---
def main():
    printe.output( '*<<lightred>> > main:')
    #---
    # python3 red.py -page:Allopurinol
    # python3 red.py -page:Activated_charcoal_\(medication\)
    # python3 red.py -newpages:10
    # python red.py -newpages:1000
    # python red.py -newpages:20000
    options = {}
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
    for arg in sys.argv:
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
        if arg == "-page2" or arg == "page2" : 
            value = py_tools.ec_de_code( value , 'decode' )
            pages.append( value )
        #---
        if arg == 'newpages' or arg == '-newpages':
            newpages = value
        #---
        # python red.py -ns:0 -usercontribs:Edoderoobot
        # python red.py -ns:0 -usercontribs:Ghuron
        if arg == "-user" or arg == "-usercontribs" : 
            user = value
        #---
        # python red.py -start:!
        if arg == 'start' or arg == '-start':
            starts = value
        #---
        if arg == "-ns" : 
            namespaces = value
        #---
        # python red.py -file:mdwiki/list.txt
        # python3 red.py -file:mdwiki/list.txt
        if arg == "-file" : 
            #---
            #if value == 'redirectlist.txt' :
                #value = '/data/project/mdwiki/public_html/redirectlist.txt'
            #---
            text2 = codecs.open(value, 'r', 'utf8')
            text = text2.read()
            for x in text.split("\n") : 
                pages.append( x.strip() )
        #---
        # python red.py -ns:0 search:drug
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
            # python red.py -start:all
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
            # python red.py -start:all
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
            # python red.py -start:! -limit:3
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
# python red.py
#---
if __name__ == "__main__":
    main()
#---
