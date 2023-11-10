#!/usr/bin/env python
"""
python3 core8/pwb.py newupdater/medask -page:Haemophilus_influenzae
python3 core8/pwb.py newupdater/medask -page:Crohn's_disease
python3 core8/pwb.py newupdater/medask -newpages:1000
python3 core8/pwb.py newupdater/medask -newpages:20000
python3 core8/pwb.py newupdater/medask -ns:0 search:drug
python3 core8/pwb.py newupdater/medask -start:!
python3 core8/pwb.py newupdater/medask -ns:0 -usercontribs:Edoderoobot
python3 core8/pwb.py newupdater/medask -ns:0 -usercontribs:Ghuron
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import sys
import urllib
import urllib.parse

# ---
from pathlib import Path

Dir = Path(__file__).parent
# ---
sys.path.append(str(Dir))
# ---
from newupdater import med
from mdpy import printe
from mdpy.bots import mdwiki_api
from new_api.mdwiki_page import NEW_API

# ---
api_new = NEW_API('www', family='mdwiki')
api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# pages   = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)


def work_on_title(title, returntext=False, text_O=""):
    # ---
    med.login()
    # ---
    title = urllib.parse.unquote(title)
    # ---
    text, new_text = med.get_new_text(title, text=text_O)
    # ---
    if text == "" or new_text == "":
        printe.output("<<red>> notext")
        return
    # ---
    if text == new_text:
        printe.output("no changes")
        return
    # ---
    printe.showDiff(text, new_text)
    # ---
    ask = input(f"<<yellow>> save title:{title}? ")
    # ---
    if ask in ['y', '', 'a']:
        return med.page_put(new_text, title)
    else:
        print("not saved")
        return


def main1():
    # ---
    if sys.argv and sys.argv[1]:
        # ---
        title = sys.argv[1]
        # ---
        work_on_title(title)


def main():
    printe.output('*<<lightred>> > main:')
    # ---
    user = ''
    user_limit = '3000'
    # ---
    searchlist = {
        "drug": "insource:/https\\:\\/\\/druginfo\\.nlm\\.nih\\.gov\\/drugportal\\/name\\/lactulose/",
    }
    # ---
    limite = 'max'
    starts = ''
    # ---
    pages = []
    # ---
    namespaces = '0'
    newpages = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if not value:
            print(f"Value required for argument {arg}")
            continue
        # ---
        arg = arg.lower()
        # ---
        if arg == "-limit" or arg == "limit":
            limite = value
        # ---
        if arg == "-userlimit" or arg == "userlimit":
            user_limit = value
        # ---
        if arg == "-page" or arg == "page":
            pages.append(value)
        # ---
        if arg == 'newpages' or arg == '-newpages':
            newpages = value
        # ---
        if arg == "-user" or arg == "-usercontribs":
            user = value
        # ---
        if arg == 'start' or arg == '-start':
            starts = value
        # ---
        if arg == "-ns":
            namespaces = value
        # ---
        if arg == 'search':
            if value in searchlist:
                value = searchlist[value]
            # ---
            ccc = NEW_API.Search(value=value, ns="0", srlimit="max")
            for x in ccc:
                pages.append(x)
    # ---
    if starts != '':
        # ---
        if starts == 'all':
            starts = ''
        # ---
        listen = api_new.Get_All_pages(start=starts, namespace=namespaces, limit=limite)
        # ---
        for n, page in enumerate(listen):
            printe.output(f'<<green>> n:{n}, title:{page}')
            work_on_title(page)
            # ---
    # ---
    lista = []
    # ---
    if newpages != "":
        lista = api_new.Get_Newpages(limit=newpages, namespace=namespaces)
    elif user != "":
        lista = mdwiki_api.Get_UserContribs(user, limit=user_limit, namespace=namespaces, ucshow="new")
    elif pages != []:
        lista = pages
    # ---
    for n, page in enumerate(lista):
        printe.output(f'<<green>> n:{n}, title:{page}')
        work_on_title(page)
    # ---


if __name__ == "__main__":
    main()
