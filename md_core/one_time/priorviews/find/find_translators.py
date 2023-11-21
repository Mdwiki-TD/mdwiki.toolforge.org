'''

python3 core8/pwb.py priorviews/find/find_translators new
python3 core8/pwb.py priorviews/find/find_translators removeip

'''
from priorviews.lists.links_by_section import links_by_lang
import sys
import json
import os
from pathlib import Path
import codecs

# ---
from mdpy import printe

# ---
from priorviews.bots import get_translator

# ---
from priorviews.bots import helps

# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# helps.dump_data(file, data)
# ---
TEST = False
# ---
Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file = f'{Dir2}/lists/translators_mdwiki_langs.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
tra_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))


def logem():
    printe.output(f'<<yellow>> logem {len(tra_by_lang)} words')
    # dump tra_by_lang
    helps.dump_data(file, tra_by_lang)


# ---
N_g = 0


def get_t(links, lang):
    # ---
    global tra_by_lang, N_g
    # ---
    if lang not in tra_by_lang:
        tra_by_lang[lang] = {}
    # ---
    m = 0

    def valid(x, tab, empty=''):
        i = tab.get(x) or tab.get(x.lower())
        if not i or i == empty:
            return True
        return False

    # ---
    if 'onlynew' in sys.argv:
        links = [x for x in links if valid(x, tra_by_lang[lang])]
    # ---
    lena = len(links)
    # ---
    for title in links:
        # ---
        title_lower = title.lower()
        # ---
        m += 1
        # ---
        value_in = tra_by_lang[lang].get(title_lower) or tra_by_lang[lang].get(title) or ''
        # ---
        if 'new' in sys.argv and value_in != "":
            continue
        # ---
        printe.output(f'<<yellow>> title: {m}/{lena} get_t {title}, value_in:{value_in}')
        # ---
        _value = get_translator.get_au(title, lang)
        # ---
        if _value is None:
            _value = 0
        # ---
        if value_in != 0 and _value == 0:
            continue
        # ---
        if helps.is_ip(_value):
            continue
        # ---
        tra_by_lang[lang][title_lower] = _value
        # ---
        N_g += 1
        # ---
        if N_g % 100 == 0:
            logem()


def start():
    # ---
    langkeys = links_by_lang.keys()
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langkeys = [value]
    # ---
    n = 0
    # ---
    for lang in langkeys:
        # ---
        links = links_by_lang[lang]
        # ---
        print(f'lang: {lang}')
        print(f'links: {len(links)}')
        # ---
        n += 1
        # ---
        get_t(links, lang)
        # ---
    # ---
    logem()


def test():
    # ---
    da = ['مرحاض ذو حفرة']
    # ---
    get_t(da, "ar")
    # ---
    logem()
    # ---
    n = 0
    # ---
    if "print" in sys.argv:
        for lang, titles in tra_by_lang.items():
            for title, tra in titles.items():
                if tra != '':
                    n += 1
                    print(n, lang, title, tra)


def removeip():
    # ---
    for lang in tra_by_lang.copy():
        titles = tra_by_lang[lang]
        for title, user in titles.items():
            if user == '':
                continue
            # ---
            # skip user match ip address
            if helps.is_ip(user):
                tra_by_lang[lang][title] = ''
                print(f' <<yellow>> skip user match ip address: {user}')
                continue
    # ---
    logem()

    # ---


# ---
if __name__ == '__main__':
    if 'removeip' in sys.argv:
        removeip()
    elif "test1" in sys.argv:
        TEST = True
        test()
    else:
        start()
