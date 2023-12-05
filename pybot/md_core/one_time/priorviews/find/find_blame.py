'''

python3 core8/pwb.py priorviews/find/find_blame -lang:ar

'''

import sys
import os
from pathlib import Path
import json
import sys
import codecs

# ---
from mdpy import printe
from priorviews.bots import gt_blame
from priorviews.lists.links_by_section import links_by_lang
from priorviews.lists.translators import tra_by_lang
from priorviews.lists import creators
from prior.json_langs.lists import json_langs_by_langs

# tab = json_langs_by_langs.get(lang, {}).get(title, {})# {'extlinks': extlinks, 'refsname': refsname}
# ---
from priorviews.bots import helps

# ---
from wikiblame.bot import get_blame  # first, result = get_blame({"lang": "es", "article": "Letrina " ,"needle": "Till2014"})

# ---
links_without_translator = {}
# ---
for lla, titles in links_by_lang.items():
    links_without_translator[lla] = [x for x in titles if tra_by_lang.get(lla, {}).get(x, '') == '' and tra_by_lang.get(lla, {}).get(x.lower(), '') == '']
# ---
COUNTS_ALL = 0
# ---
Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file = f'{Dir2}/lists/blames.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
new_data = json.load(codecs.open(file, 'r', 'utf-8'))


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
    en = infos.get('en', '')
    # ---
    if 'history' in sys.argv:
        ne = gt_blame.search_history(title, lang, en=en, refname=refname, extlinks=extlinks)
        if ne:
            return ne
    else:
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
    return ''


def logem():
    printe.output(f'<<yellow>> logem {len(new_data)} words')
    # dump new_data
    helps.dump_data(file, new_data)


def get_b(links, lang):
    # ---
    global new_data, COUNTS_ALL
    # ---
    if lang not in new_data:
        new_data[lang] = {}

    def valid(x, tab, empty=''):
        i = tab.get(x) or tab.get(x.lower())
        if not i or i == empty:
            return True
        return False

    # ---
    if 'new' in sys.argv:
        # links = [ x for x in links if not x in new_data[lang] or v[lang][x] == '']
        links = [x for x in links if valid(x, new_data[lang], empty='')]
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
        COUNTS_ALL += 1
        # ---
        if COUNTS_ALL % 200 == 0:
            logem()
        # ---
        value_in = new_data[lang].get(title_lower) or new_data[lang].get(title) or ''
        # ---
        if 'new' in sys.argv and (title_lower in new_data[lang] or title in new_data[lang]):
            continue
        # ---
        new_data[lang][title_lower] = value_in
        # ---
        printe.output(f'<<yellow>> title: {m}/{lena} get_t {title}, value_in:{value_in}')
        # ---
        # {"time": 20140721110644, "actor": "CFCF", "comment": "Translated from [[:en:African trypanosomiasis|English]] by Somil.Mishra at [[:en:Translators Without Borders|Translators Without Borders]]", "TD": false}
        crate = lang_creators.get(title, {})
        page_time = crate.get("time")
        # ---
        if page_time:
            printe.output(f'<<yellow>> page_time: {page_time}')
            year = int(str(page_time)[0:4])
            if year < 2012 and 'all' not in sys.argv:
                printe.output('<<red>> skip....')
                continue
        # ---
        _value = gtblame_value(title, lang)
        # ---
        if _value is None:
            _value = 0
        # ---
        if _value == 'creator':
            _value = crate.get("actor", '')
            printe.output(f'<<green>> creator _value: {_value}')
        # ---
        if value_in != 0 and _value == 0:
            continue
        # ---
        new_data[lang][title_lower] = _value
        # ---
    # ---
    # logem()


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
        print('=============================' * 2)
        print(f'lang: {la}, links: {len(links)}')
        # ---
        n += 1
        # ---
        get_b(links, la)
    # ---
    logem()

    # ---


# ---
if __name__ == '__main__':
    start()
