'''
python pwb.py prior/niosh
'''
import sys
import os
import re
import json
import urllib.parse
import pywikibot
import wikitextparser
import codecs
#---
from mdpy import printe
#---
Dir = os.path.dirname(os.path.abspath(__file__))
Dir2 = os.path.dirname(Dir)
#---
project_js_newen = f'{Dir2}/json_en/'
#---
from new_api.mdwiki_page import MainPage as md_MainPage

allen = {}
#---
for filename in os.listdir(project_js_newen):
    if filename.endswith('.json'):
        filename2 = os.path.join(project_js_newen, filename)
        #---
        printe.output(f'filename: {filename2}..')
        #---
        data = json.load(open(filename2, 'r'))
        #---
        allen = {**allen, **data}
#---
toto = {}
#---
for a, tab in allen.items():
        lol = []
        ext = tab['extlinks']
        for x in ext:
            if x.find('cdc.gov/niosh/') != -1:
                lol.append(x)

        if len(lol) > 0:
            toto[a] = lol
    
#---
ns = len(toto.keys())
n = 0
#---
for x, exts in toto.items():
    n += 1
    print(f'n:{n}/{ns}, title:{x} lenth:{len(exts)}')
#---
    