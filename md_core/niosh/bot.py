'''
python pwb.py niosh/bot
python3 core8/pwb.py niosh/bot
'''
import sys
import os
import re
import json
import urllib.parse
import pywikibot
import wikitextparser
import codecs
# ---
from mdpy import printe
from new_api.wiki_page import MainPage, NEW_API
# ---
Dir = os.path.dirname(os.path.abspath(__file__))
# ---
file_json = f"{Dir}/jsons/extlinks.json"
if not os.path.isfile(file_json):
    json.dump({}, codecs.open(file_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
# ---
api_new = NEW_API('en', family='wikipedia')
# ---
value = 'insource:"cdc.gov/niosh/"'
search = api_new.Search(value, ns="0", offset='', srlimit="max", RETURN_dict=False, addparams={})
# ---
toto = {}
# ---
for x in search:
    page = MainPage(x, 'en', family='wikipedia')
    extlinks = page.get_extlinks()
    toto[x] = extlinks
# ---
json.dump(toto, codecs.open(file_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
# ---
ns = len(toto.keys())
n = 0
# ---
for x, exts in toto.items():
    n += 1
    print(f'n:{n}/{ns}, title:{x} lenth:{len(exts)}')
# ---
