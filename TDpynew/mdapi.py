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
#---
from warnings import warn
#import pywikibot
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
import requests
#---
import user_account_new
#---
username = user_account_new.my_username      #user_account_new.bot_username
passe    = user_account_new.mdwiki_pass         #user_account_new.bot_password     #user_account_new.my_password
#---
#---
SS = {}
#---
print_pywikibot = { 1 : False }
try:
    import pywikibot
    print_pywikibot[1] = True
except:
    print_pywikibot[1] = False
#---
def printt(s):
    if print_pywikibot[1]:
        pywikibot.output(s)
    #else:
        #print(s)
#---
def start_sea():
    global SS
    SS["ss"] = requests.Session()
    SS["url"] = 'https://' + 'mdwiki.org/w/api.php'
    SS["ss"] = requests.Session()
    #---
    r11 = SS["ss"].get(SS["url"], params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        })
    r11.raise_for_status()
    # log in
    r22 = SS["ss"].post(SS["url"], data= {
        #'assert': 'user',
        'format': 'json',
        'action': 'login',
        'lgname': username,
        'lgpassword': passe,
        'lgtoken': r11.json()['query']['tokens']['logintoken'],
        } )
    #---
    # printt( f'__file__:{__file__}' )
    #---
    if r22.json()['login']['result'] != 'Success':
        ress = r22.json()['login']['result']
        if print_pywikibot[1]:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(ress), UserWarning)
            pywikibot.output( r22.json() )
            pywikibot.output( 'CRITICAL:' )
    else:
        printt( "<<lightgreen>> mdwiki/TDpy/mdapi.py: log to %s user:%s Success... " % (SS["url"], username ) )
    #---
    # get edit token
    SS["r33"] = SS["ss"].get(SS["url"], params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    })
    #---
    SS["r3_token"] = SS["r33"].json()['query']['tokens']['csrftoken']
    #---
#---
start_sea()
#---
# mdapi.submitAPI( params, type ="get" )
#---
def submitAPI( params, type = 'get'):
    #---
    json1 = {}
    #---    
    try:
        r4 = SS["ss"].post(SS["url"], data=params)
        json1 = json.loads( r4.text )
    except Exception as e:
        if print_pywikibot[1]:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
        return {}
    #---
    return json1
#---