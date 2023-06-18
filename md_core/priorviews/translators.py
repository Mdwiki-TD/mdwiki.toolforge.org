'''

#---
from priorviews import translators
# translators.tra_by_lang
# translators.counts_by_translator
#---
python3 ./core8/pwb.py priorviews/translators

'''
import sys
import pywikibot
import json
import os
import re
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
file = f'{Dir}/translators_mdwiki_langs.json'
#---
if not os.path.exists(file):
    with open(file, 'w') as f:  json.dump({}, f)
#---
tra_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))
#---
_data = { "ar" : { "artitle" : "بيت الحكمة"}}
#---
counts_by_translator  = {}
#---
# Iterate through each markdown file and language in `tra_by_lang`
for lang, titles in tra_by_lang.items():
    #---
    if not lang in counts_by_translator: counts_by_translator[lang] = {}
    #---
    for title, user in titles.items():
        if not user in counts_by_translator[lang] : counts_by_translator[lang][user] = 0
        counts_by_translator[lang][user] += 1
#---
if __name__ == '__main__':
    for x, wo in counts_by_translator.items():   print(x, wo)
    #---
    print(f'len of counts_by_translator: {len(counts_by_translator)}')
    #---
    print(f'len of tra_by_lang: {len(tra_by_lang)}')
    for lang, titles in tra_by_lang.items():
        for title, words in titles.items():
            print(lang, title, words)

#---