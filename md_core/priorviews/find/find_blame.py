'''

python3 core8/pwb.py priorviews/find/find_blame -lang:ar

'''

import sys
import os
import re
import json
import sys
import pywikibot
import codecs
import datetime
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import urlencode
import requests
import wikitextparser
# ---
from mdpy import printe
from priorviews.bots import gt_blame
from priorviews.lists.links_by_section import links_by_lang
from priorviews.lists.translators import tra_by_lang
from priorviews.lists import creators
from prior.json_langs.lists import json_langs_by_langs
# tab = json_langs_by_langs.get(lang, {}).get(title, {})# {'extlinks': extlinks, 'refsname': refsname}
# ---
from wikiblame.bot import get_blame  # first, result = get_blame({"lang": "es", "article": "Letrina " ,"needle": "Till2014"})
# ---
links_without_translator = {}
# ---
for lla, titles in links_by_lang.items():
    links_without_translator[lla] = [x for x in titles if tra_by_lang.get(lla, {}).get(x, 0) == 0]
# ---
counts_all = 0
# ---
Dir = os.path.dirname(os.path.abspath(__file__))
Dir2 = os.path.dirname(Dir)
# ---
file = f'{Dir2}/lists/blames.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
new_data = json.load(codecs.open(file, 'r', 'utf-8'))
# ---


def gtblame_value(title, lang):
    # ---
    tab = {"lang": lang, "article": title, "needle": ""}
    # ---
    infos = json_langs_by_langs.get(lang, {}).get(title)  # {'extlinks': extlinks, 'refsname': refsname}
    # ---
    if not infos:
        return ''
    # ---
    refname = infos.get('refsname', [])
    extlinks = infos.get('extlinks', [])
    # ---
    for ref in refname:
        # ---
        printe.output(f'search for: ref: ({ref}), page: [[{lang}:{title}]]')
        # ---
        tab['needle'] = ref
        # ---
        first, result = get_blame(tab)
        # ---
        if first:
            return 'creator'
    # ---
    # ne = gt_blame.search_history(title, lang, refname=refname, extlinks=extlinks)
    # ---
    return ''
# ---


def logem():
    printe.output(f'<<yellow>> logem {len(new_data)} words')
    # dump new_data
    with codecs.open(file, 'w', 'utf-8') as foo:
        json.dump(new_data, foo, ensure_ascii=False)
    # ---


def get_b(links, lang):
    # ---
    global new_data, counts_all
    # ---
    if not lang in new_data:
        new_data[lang] = {}
    # ---
    m = 0
    # ---
    lang_creators = creators.Creators_by_lang_title.get(lang, {})
    # ---
    lena = len(links)
    # ---
    for title in links:
        # ---
        title_lower = title.lower()
        # ---
        m += 1
        # ---
        value_in = new_data[lang].get(title_lower, "")
        # ---
        counts_all += 1
        # ---
        if 'new' in sys.argv and value_in != "":
            continue
        # ---
        printe.output(f'<<yellow>> title: {m}/{lena} get_t {title}, value_in:{value_in}')
        # ---
        # {"time": 20140721110644, "actor": "CFCF", "comment": "Translated from [[:en:African trypanosomiasis|English]] by Somil.Mishra at [[:en:Translators Without Borders|Translators Without Borders]]", "TD": false}
        crate = lang_creators.get(title, {})
        # ---
        page_time = crate.get("time")
        # ---
        if page_time:
            printe.output(f'<<yellow>> page_time: {page_time}')
            year = int(str(page_time)[0:4])
            if year < 2012:
                printe.output('<<red>> skip....')
                continue
        # ---
        _value = gtblame_value(title, lang)
        # ---
        if _value is None:
            _value = 0
        # ---
        if _value == 'creator':
            _value = crate["actor"]
            printe.output(f'<<green>> creator _value: {_value}')
        # ---
        if value_in != 0 and _value == 0:
            continue
        # ---
        new_data[lang][title_lower] = _value
        # ---
        if counts_all % 100 == 0:
            logem()
    # ---
    logem()
    # ---


def start():
    # ---
    langkeys = links_without_translator.keys()
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langkeys = [value]
    # ---
    n = 0
    # ---
    for la in langkeys:
        # ---
        links = links_without_translator[la]
        # ---
        print(f'lang: {la}')
        print(f'links: {len(links)}')
        # ---
        n += 1
        # ---
        get_b(links, la)
        # ---
        if n % 20 == 0:
            logem()
    # ---
    logem()

    # ---
# ---
if __name__ == '__main__':
    start()
