#!/usr/bin/env python

"""

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import json
import codecs
import sys
import os
#---
import requests
import urllib
import urllib.parse
#---
import MedWork
#---
from_toolforge = True
#---
def print_new(s):
    if not from_toolforge:
        printe.output(s)
#---
if not "from_toolforge" in sys.argv and not "ch" in sys.argv:
    from_toolforge = False
    import printe
#---
MedWork.printn = print_new
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project): project = "/mdwiki"
#---
import user_account_new
#---
username = user_account_new.my_username
password = user_account_new.mdwiki_pass
#---
SS = {}
#---
def login():
    #---
    SS["ss"] = requests.Session()
    SS["url"] = "https://" + "mdwiki.org/w/api.php"
    SS["ss"] = requests.Session()
    #---
    r11 = SS["ss"].get(SS["url"], params={
        "format": "json",
        "action": "query",
        "meta": "tokens",
        "type": "login",
        })
    r11.raise_for_status()
    # log in
    r22 = SS["ss"].post(SS["url"], data= {
        #fz"assert": "user",
        "format": "json",
        "action": "login",
        "lgname": username,
        "lgtoken": r11.json()["query"]["tokens"]["logintoken"],
        "lgpassword": password,
        } )
    #---
    # get edit token
    SS["r33"] = SS["ss"].get(SS["url"], params={
        "format": "json",
        "action": "query",
        "meta": "tokens",
    })
    #---
    SS["r3_token"] = SS["r33"].json()["query"]["tokens"]["csrftoken"]
#---
login()
#---
def GetPageText(title):
    #---
    print_new(f'get text for {title}')
    #---
    params = { "action": "parse", "format": "json", "prop": "wikitext", "page": title, "utf8": 1}
    #---
    url = "https://" + "mdwiki.org/w/api.php?action=parse&prop=wikitext&utf8=1&format=json&page=" + title
    #---
    r4 = {}
    #---
    try:
        r4 = SS["ss"].post(SS["url"], data=params).json()
    except Exception as e:
        print_new(e)
        r4 = {}
    #---
    # print_new(r4)
    #---{'parse': {'title': 'Semaglutide', 'pageid': 55901, 'wikitext': {'*': '
    text = r4.get("parse", {}).get("wikitext", {}).get("*", "")
    #---
    return text
#---
def page_put(NewText, title):
    #---
    pparams = {
        "action": "edit",
        "format": "json",
        "title": title,
        "text": NewText,
        "summary": "mdwiki changes.",
        "bot": 1,
        "nocreate": 1,
        "token": SS["r3_token"],
    }
    #---
    r4 = {}
    #---
    try:
        r4 = SS["ss"].post(SS["url"], data=pparams).json()
    except Exception as e:
        print("save error: " + str(e))
        return
    #---
    if "success" in str(r4).lower():
        print( "True" )
    else:
        print( r4.get("error", {}).get("info", ""))
        print( "False" )
#---
def get_new_text(title, text=''):
    #---
    if text == "" :     text = GetPageText( title )
    #---
    newtext = ""
    #---
    if text != "":
        newtext = MedWork.work_on_text(title, text)
    #---
    return text, newtext
#---
def work_on_title(title, returntext=False, text_O=""):
    #---
    title = title
    title = urllib.parse.unquote(title)
    #---
    text, new_text = get_new_text(title, text=text_O)
    #---
    if not "ch" in sys.argv :
        print(new_text)
        return
    #---
    if text.strip() == "" or new_text.strip() == "":
        print("notext")
        return
    elif text == new_text :
        print("no changes")
        return
    elif "save" in sys.argv:
        return page_put(new_text, title)
    #---
    title2 = title
    title2 = title2.replace(":","-").replace("/","-")
    #---
    try:
        filename = project + "/public_html/updatercash/" + title2 + ".txt"
        #---
        codecs.open( filename, "w", encoding="utf-8").write( new_text ) 
        #---
        print(filename)
        #---
    except Exception as e:
        filename = project + "/public_html/updatercash/title2.txt"
        #---
        codecs.open(filename, "w", encoding="utf-8").write( new_text ) 
        #---
        print(filename)
#---
def main():
    #---
    if sys.argv and sys.argv[1] :
        #---
        title = sys.argv[1]
        #---
        work_on_title(title)
#---
if __name__ == "__main__":
    main()
#---