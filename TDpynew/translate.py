#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import codecs
import re
import string
import sys
#---

#---
import urllib
import urllib.request
import urllib.parse
import requests
#---
import text_changes
import ref
# ref.fix_ref( first , alltext )
#---
import user_account_new
#---
lgname_enwiki   = user_account_new.lgname_enwiki
lgpass_enwiki   = user_account_new.lgpass_enwiki
#---
import mdapi
# mdapi.submitAPI( params )
#---
wholearticle = { 1 : False }
#---
SS = { "token" : '' }
session = {}
session[1] = requests.Session()
session["url"] = ""
#---
Url_To_login = { 1 : '' , 'not' : True }
#---
login_done = { 1 : False }
#---
def log_to_enwiki() :
    #---
    if login_done[1] : return ''
    #---
    api_urle = 'https://' + 'en.wikipedia.org/w/api.php' 
    #---
    Url_To_login[1] = api_urle
    #---
    session[1] = requests.Session()
    #---
    session["url"] = api_urle
    #---
    # get login token
    r1 = session[1].get(api_urle, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
    })
    r1.raise_for_status()
    # log in
    r2 = session[1].post(api_urle, data={
        'format': 'json',
        'action': 'login',
        'lgname': lgname_enwiki,
        'lgpassword': lgpass_enwiki,
        'lgtoken': r1.json()['query']['tokens']['logintoken'],
    })

    r3 = session[1].get(api_urle, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    })
    #---
    token = r3.json()['query']['tokens']['csrftoken']
    #---
    login_done[1] = True
    #---
    session["token"] = token
#---
def submit_to_enwiki( params ):
    #---
    log_to_enwiki()
    #---
    params['token'] = session.get("token","")
    #---
    json1 = {}
    #---    
    try:
        r4 = session[1].post(session["url"], data=params)
        json1 = json.loads( r4.text )
    except Exception as e:
        # pywikibot.output( "arAPI: post_ss error: %s" % e )
        return {}
    #---
    return json1
    #---
def put(title,text):
    #---
    text = text.replace("{{Sprotect|small=yes}}","")
    #---
    suus = 'from https://' + 'mdwiki.org/wiki/' + title.replace(' ' , '_')
    #---
    tit2 = 'User:Mr. Ibrahem/' + title
    #---
    dataa = {
        "format": "json",
        "utf8": 1,
        "action": "edit",
        "title": tit2,
        "text": text,
        "summary": suus,
        #"nocreate": 1,
    }
    #---
    js = submit_to_enwiki( dataa )
    #---
    if 'Success' in str(js):
        print('true')
    else:
        print(str(js))
#---
def work( title ):
    #---
    title = urllib.parse.unquote(title)
    #---
    if 'test' in sys.argv: print(title)
    #---
    params2 = {"action": "parse","format": "json","page": title ,"prop": "wikitext"}
    #---
    json2 = mdapi.submitAPI(params2)
    #---
    alltext = json2.get("parse", {}).get("wikitext", {}).get("*", '')
    #---
    first = ''
    #---
    if wholearticle[1]:
        first = alltext
    else:
        params = {"action": "parse","format": "json","page": title ,"prop": "wikitext","section": "0" }
        json1 = mdapi.submitAPI(params)
        first = json1.get("parse", {}).get("wikitext", {}).get("*", '')
    #---
    text = first
    #---
    if not wholearticle[1]:
        #text += '\n==References==\n<references />\n[[en:%s]]' % title
        text += '\n==References==\n<references />'
    #---
    text = ref.fix_ref( text, alltext )
    #---
    text = text_changes.work( text )
    #---
    text = text.replace('[[Category:','[[:Category:')
    #---
    if text == '' : return "no text"
    #---
    return put(title,text)
    #---
title = ''
#---
# python translate.py -title:Amoebiasis 
#---
for arg in sys.argv:
    arg, sep, value = arg.partition(':')
    #---
    if arg == "-title" : title = value
    #---
    if arg == "wholearticle" : wholearticle[1] = True
    #---
if title != '' :
    work( title )
    #print(a)
#---

#---
