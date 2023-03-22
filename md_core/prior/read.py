'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]
'''
import sys
from collections import namedtuple
import os
import re
import json
import urllib.parse
import requests
import wikitextparser
import codecs
from mdpy import printe
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior/'
#---
all = json.loads(codecs.open(project + 'allen.json', 'r', encoding='utf-8').read())
#--
# _all_ = { "Abacavir": { "refs": 23, "langs": { "ar": { "title": "title", "refs": 5, "same": 4 } } } }
#---
text = ''
#---
# create wikitext from json
for en, ta in all.items():
    refs = ta['refs']
    langs = ta['langs']
    #---
    if refs < 1: continue
    #---
    langs1 = [ (v["same"], k) for k, v in langs.items() ]
    langs = { k: v for k, v in sorted(langs.items(), key=lambda item: item[1]['same'], reverse=True) }
    # sort lang by same
    langs1.sort(reverse=True)
    #---
    printe.output(len(langs1))
    #---
    same_text = '''{| class="wikitable sortable"
|-
! lang !! count'''
    #---
    # printe.output(langs)
    #---
    # for vs, lang in langs1:
        # lang_ta = langs[lang]
        #---
    for lang, lang_ta in langs.items():
        #---
        title = lang_ta['title']
        same = lang_ta['same']
        #---
        if same < 1: continue
        if 11 > same < ((refs/2)-1): continue
        #---
        ll = f'[[:{lang}:{title}|{lang}]]'
        #---
        line = f'''|-\n|{ll} || {same}'''
        #---
        # print(line)
        #---
        same_text += f'''\n{line}'''
    #---
    if same_text.find('[[') == -1: continue
    #---
    same_text = same_text.strip()
    #---
    text += f'''
    
=={en}==
* en: [[:en:{en}|{en}]], refs: {refs}
* same refrences:
{same_text}'''
    #---
    text += '\n|}'
    #---
#---
# write text to file
codecs.open(project + 'en.txt', 'w', encoding='utf-8').write(text)
#---
