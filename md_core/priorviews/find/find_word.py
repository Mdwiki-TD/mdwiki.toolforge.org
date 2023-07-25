'''

python3 core8/pwb.py priorviews/find/find_word -lang:ar
python3 core8/pwb.py priorviews/find/find_word new

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
from priorviews.bots import count_words
#---
TEST = False
#---
Dir = os.path.dirname(os.path.abspath(__file__))
Dir2 = os.path.dirname(Dir)
#---
file = f'{Dir2}/lists/words_mdwiki_langs.json'
#---
if not os.path.exists(file):
    with open(file, 'w') as f:  json.dump({}, f)
#---
from priorviews.lists.links_by_section import links_by_lang
#---
words_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))
#---
def log_words():
    printe.output(f'<<yellow>> log_words {len(words_by_lang)} words')
    # dump words_by_lang
    with codecs.open(file, 'w', 'utf-8') as f:  json.dump(words_by_lang, f)
    #---
#---
N_g = 0
#---
def get_w(links, lang):
    #---
    global words_by_lang, N_g
    #---
    if not lang in words_by_lang: words_by_lang[lang] = {}
    #---
    m = 0
    #---
    if 'onlynew' in sys.argv:
        links = [ x for x in links if not x in words_by_lang[lang] or words_by_lang[lang][x] == 0]
    #---
    lena = len(links)
    #---
    for title in links:
        #---
        title_lower = title.lower()
        #---
        m += 1
        #---
        words_in = words_by_lang[lang].get(title_lower, 0)
        #---
        if 'new' in sys.argv and words_in > 40 : continue
        #---
        printe.output(f'<<yellow>> title: {m}/{lena} get_w {title}, words_in:{words_in}')
        #---
        _words = count_words.get_words(title, lang)
        #---
        if _words is None: _words = 0
        #---
        if words_in != 0 and _words == 0: continue
        #---
        words_by_lang[lang][title_lower] = _words
        #---
        N_g += 1
        #---
        if N_g % 100 == 0:
            log_words()
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
        get_w(links, lang)
        #---
    #---
    log_words()
    #---
#---
def test():
    #---
    da = [
        'مرحاض ذو حفرة'
    ]
    #---
    get_w(da, "ar")
    #---
    # log_words()
    #---
#---
if __name__ == '__main__':
    if "test1" in sys.argv: 
        TEST = True
        test()
    else: 
        start()
