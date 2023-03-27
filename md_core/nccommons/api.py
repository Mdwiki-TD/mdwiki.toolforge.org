#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
#
# (C) Ibrahem Qasim, 2023
#
#---
import re
import sys
import json
import time
import urllib
import urllib.parse
import os
import codecs
import configparser
import requests
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project):  project = "I:/mdwiki/md_core/nccommons"
#---
config = configparser.ConfigParser()
config.read(project + "/nccommons_user.ini")
#---
username = config["DEFAULT"]["username"].strip()
password = config["DEFAULT"]["password"].strip()
#---
print(f"username: {username}")
#---
yes_answer = ["y", "a", "", "Y", "A", "all"]
#---
SS = {}
r1_params = {"format": "json", "action": "query", "meta": "tokens", "type": "login"}
r2_params = {"format": "json", "action": "login", "lgname": username, "lgpassword": password}
#---
SS["ss"] = requests.Session()
#---
def py_input(s):
    print(s)
    sa = input()
    #---
    return sa
#---
def post(params):
    #---
    jj = {}
    #---
    if 'printurl' in sys.argv: 
        url = SS["url"] + '?' + urllib.parse.urlencode(params)
        print(url.replace('&format=json', ''))
    #---
    try:
        r4 = SS["ss"].post(SS["url"], data=params)
    except Exception as e:
        print(f"nccommons/com.py: {e}")
        return False
    #---
    try:
        jj = r4.json()
    except:
        print("error r4.json()")
        print(f"r4.text: {r4.text}")
    #---
    return jj
#---
def Log_to_wiki(family="nccommons", lang="www"):
    #---
    user = r2_params["lgname"]
    #---
    print(f"nccommons/com.py: log to {lang}.{family}.org user:{user}")
    #---
    SS["family"] = family
    SS["lang"] = lang
    SS["url"] = "https://" + f"{lang}.{family}.org/w/api.php"
    SS["ss"] = requests.Session()
    #---
    r11 = SS["ss"].get(SS["url"], params=r1_params)
    r11.raise_for_status()
    #---
    r2_params["lgtoken"] = r11.json()["query"]["tokens"]["logintoken"]
    r22 = SS["ss"].post(SS["url"], data=r2_params)
    #---
    if r22.json()["login"]["result"] != "Success":
        print("nccommons/com.py: login failed, reason: %s" % r22.json()["login"]["reason"])
        sys.exit(1)
    else:
        print("com.py login Success")
    #---
    SS["r33"] = SS["ss"].get( SS["url"], params={"format": "json", "action": "query", "meta": "tokens"})
    #---
    SS["r3_token"] = SS["r33"].json()["query"]["tokens"]["csrftoken"]
#---
Log_to_wiki()
#---
def Get_All_pages_A(start, namespace="0", limit="max", apfilterredir="", apcontinue=""):
    #---
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "apnamespace": namespace,
        "aplimit": limit,
        "apfilterredir": "nonredirects",
        "utf8": 1,
        "token": SS["r3_token"],
        "bot": 1,
    }
    #---
    if apfilterredir in ["redirects", "all", "nonredirects"]:
        params["apfilterredir"] = apfilterredir
    #---
    if start != "":
        params["apfrom"] = start
    #---
    if apcontinue != "":
        params["apcontinue"] = apcontinue
    #---
    json1 = post(params)
    #---
    # if json1:   newss = json1.get("query", {}).get("allpages", {})
    #---
    return json1
#---
def Get_All_pages(start, namespace="0", limit="max", apfilterredir="", limit_all=0):
    #---
    print('Get_All_pages for start:"%s", limit:"%s",namespace:"%s",apfilterredir:"%s"'% (start, limit, namespace, apfilterredir))
    #---
    json1 = Get_All_pages_A(start, namespace=namespace, limit=limit, apfilterredir=apfilterredir)
    #---
    Main_table = []
    #---
    Apcontinue = ""
    #---
    if json1:
        Apcontinue = json1.get("continue", {}).get("apcontinue", "")
        newp = json1.get("query", {}).get("allpages", {})
        #---
        Main_table = [x["title"] for x in newp]
    else:
        print("com.py no json1")
    #---
    Apcontinue2 = {1: Apcontinue}
    numb = 0
    #---
    while Apcontinue2[1] != "":
        #---
        numb += 1
        #---
        print(f'\tGet_All_pages_A {numb}, Apcontinue2[1]..')
        #---
        try:
            json2 = Get_All_pages_A(
                start,
                namespace=namespace,
                limit=limit,
                apfilterredir=apfilterredir,
                apcontinue=Apcontinue2[1],
            )
        except KeyboardInterrupt:
            print("nccommons/com.py: KeyboardInterrupt")
            Apcontinue2[1] = ''
            json2 = False
            break
        #---
        if json2:
            Apcontinue2[1] = json2.get("continue", {}).get("apcontinue", "")
            #---
            newp = json2.get("query", {}).get("allpages", {})
            #---
            for x in newp:
                if not x["title"] in Main_table:
                    Main_table.append(x["title"])
            #---
            print("len of Main_table %d." % len(Main_table))
            #---
        else:
            print("com.py no json1")
        #---
        if limit_all > 0 and len(Main_table) > limit_all:
            Apcontinue2[1] = ""
            print("limit_all > len(Main_table) ")
            break
        #---
    #---
    # if numb > 0 and Apcontinue2[1] == "":   print("Apcontinue2[1] == '' ")
    #---
    print("com.py Get_All_pages : find %d pages." % len(Main_table))
    #---
    return Main_table
#---
Save_all = {1: False}
#---
def create_Page(text, title):
    print(" create Page %s:" % title)
    time_sleep = 0
    #---
    params = {
        "action": "edit",
        "format": "json",
        "title": title,
        "text": text,
        "summary": "create page",
        "notminor": 1,
        "createonly": 1,
        "token": SS["r3_token"],
        "utf8": 1,
    }
    #---
    if not Save_all[1] and ("ask" in sys.argv and not "save" in sys.argv):
        print(text)
        sa = py_input( 'nccommons/com.py: create:"%s" page ? ([y]es, [N]o):user:%s' % (title, r2_params["lgname"]) )
        #---
        if not sa.strip() in yes_answer:
            print("wrong answer")
            return False
        #---
        if sa.strip() == "a":
            print("---------------------------------------------")
            print("nccommons.py create_Page save all without asking.")
            print("---------------------------------------------")
            Save_all[1] = True
        #---
    #---
    result = post(params)
    #---
    success = result.get("success") or result.get("Success")
    error = result.get("error")
    #---
    if success:
        print("** true ..  %s : [[%s]] " % (SS["family"], title))
        print("تم بنجاح... time.sleep(%d) " % time_sleep)
        time.sleep(time_sleep)
        return True
    elif error:
        if "code" in error:
            if error["code"] == "articleexists":
                print("error when create_Page")
    else:
        return False
    #---
    print("end of create_Page def return False title:(%s)" % title)
    #---
    return False
#---
'''
#---
from nccommons import api
# newpages = api.Get_All_pages(start="", namespace="0", limit="max", apfilterredir="", limit_all="")
# new = api.create_Page(text=, title)
#---
'''