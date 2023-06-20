'''

python3 ./core8/pwb.py priorviews/find_translators

'''
import sys
import pywikibot
import json
import os
import re
import codecs
import datetime
from datetime import timedelta
#---
from mdpy import printe
from mdpy.bots import wiki_api
#---
from priorviews.bots import get_author
#---
TEST = False
#---
Dir = os.path.dirname(os.path.abspath(__file__))
Dir2 = os.path.dirname(Dir)
#---
file = f'{Dir2}/lists/translators_mdwiki_langs.json'
#---
if not os.path.exists(file):
    with open(file, 'w') as f:  json.dump({}, f)
#---
from priorviews.lists.links_by_section import links_by_lang
#---
tra_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))
#---
def logem():
    printe.output(f'<<yellow>> logem {len(tra_by_lang)} words')
    # dump tra_by_lang
    with codecs.open(file, 'w', 'utf-8') as f:  json.dump(tra_by_lang, f, ensure_ascii=False)
    #---
#---
N_g = 0
#---
def get_t(links, lang):
    #---
    global tra_by_lang, N_g
    #---
    if not lang in tra_by_lang: tra_by_lang[lang] = {}
    #---
    m = 0
    #---
    lena = len(links)
    #---
    for title in links:
        #---
        title_lower = title.lower()
        #---
        m += 1
        #---
        value_in = tra_by_lang[lang].get(title_lower, "")
        #---
        N_g += 1
        #---
        if 'new' in sys.argv and value_in != "" : continue
        #---
        printe.output(f'<<yellow>> title: {m}/{lena} get_t {title}, value_in:{value_in}')
        #---
        _value = get_author.get_au(title, lang)
        #---
        if _value is None: _value = 0
        #---
        if value_in != 0 and _value == 0: continue
        #---
        tra_by_lang[lang][title_lower] = _value
        #---
        if N_g % 100 == 0:
            logem()
    #---
    logem()
    #---
#---
def start():
    #---
    langkeys = links_by_lang.keys()
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langkeys = [value]
    #---
    n = 0
    #---
    for lang in langkeys:
        #---
        links = links_by_lang[lang]
        #---
        print(f'lang: {lang}')
        print(f'links: {len(links)}')
        #---
        n += 1
        #---
        get_t(links, lang)
        #---
        if n % 20 == 0:
            logem()
    #---
    logem()
    #---
#---
def test():
    #---
    da = [
        'مرحاض ذو حفرة'
    ]
    #---
    get_t(da, "ar")
    #---
    logem()
    #---
    n = 0
    #---
    if "print" in sys.argv:
        for lang, titles in tra_by_lang.items():
            for title, tra in titles.items():
                if tra != '':
                    n += 1
                    print(n, lang, title, tra)
    #---
#---
if __name__ == '__main__':
    if "test1" in sys.argv: 
        TEST = True
        test()
    else: 
        start()
