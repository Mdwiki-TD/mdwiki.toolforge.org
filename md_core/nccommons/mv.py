#!/usr/bin/python3
"""
python3 core8/pwb.py nccommons/mv
"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
from new_api.ncc_page import MainPage as ncc_MainPage
from new_api.mdwiki_page import NEW_API
from nccommons import api
from mdpy.bots import mdwiki_api
import sys
import json
import os
import codecs
import pywikibot

# ---
project = "/data/project/mdwiki/"
# ---
if not os.path.isdir(project):
    project = "I:/mdwiki"
# ---
# ---
cats = json.load(codecs.open(f'{project}/md_core/nccommons/mv.json', 'r', 'utf-8'))
# ---
pywikibot.output(f'len of cats: {len(cats)}')
# ---
# ---
api_new = NEW_API('www', family='mdwiki')
# login   = api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# ---
exists = {}
# exists = api_new.Find_pages_exists_or_not(cats)
# ---
to_create = [x for x, t in exists.items() if t == False]
# ---
pywikibot.output(f'len of to_create: {len(to_create)}')
# ---
n = 0
# ---
for cat in to_create:
    n += 1
    pywikibot.output(f'cat: {n}/{len(to_create)}:')
    text = mdwiki_api.GetPageText(cat)
    new = api.create_Page(text, cat, summary='Copy categories from mdwiki')
# ---
to_update = [x for x, t in exists.items() if t == True]
to_update = cats
# ---
# ---
n = 0


def delete_it(cat):
    # ---
    pywikibot.output(f'cat: {n}/{len(to_update)}:')
    # ---
    params = {"action": "delete", "format": "json", "title": cat, "reason": "cat moved to nccommons.org"}  # , "deletetalk": 1}
    # ---
    doit = mdwiki_api.post(params, addtoken=True)
    # ---
    pywikibot.output(f'doit: {doit}')


# ---
for cat in to_update:
    # ---
    n += 1
    # ---
    pywikibot.output(f'cat: {n}/{len(to_update)}:')
    # ---
    nspage = ncc_MainPage(cat, 'www', family='nccommons')
    # ---
    pywikibot.output(f'GetPageText for page:{cat}')
    # ---
    md_text = mdwiki_api.GetPageText(cat)
    # ---
    if md_text == '':
        continue
    # ---
    nc_text = nspage.get_text()
    # ---
    if md_text == nc_text:
        pywikibot.output(f'{cat} is up to date')
    else:
        save_page = nspage.save(newtext=md_text, summary='Copy from mdwiki', nocreate=1)
    # ---
    delete_it(cat)
    # ---
    if 'break' in sys.argv:
        break
    # ---
