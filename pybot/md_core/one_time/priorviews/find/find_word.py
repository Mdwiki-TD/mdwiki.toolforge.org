'''

python3 core8/pwb.py priorviews/find/find_word -lang:ar
python3 core8/pwb.py priorviews/find/find_word new

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
from priorviews.bots import helps
from priorviews.bots import count_words

# ---
TEST = False
# ---
Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file = f'{Dir2}/lists/words_mdwiki_langs.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
# ---
words_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))


def log_words():
    printe.output(f'<<yellow>> log_words {len(words_by_lang)} words')
    helps.dump_data(file, words_by_lang)


# ---
N_g = 0


def get_w(links, lang):
    # ---
    global words_by_lang, N_g
    # ---
    if lang not in words_by_lang:
        words_by_lang[lang] = {}
    # ---
    m = 0

    def valid(x, tab, empty=''):
        i = tab.get(x) or tab.get(x.lower())
        if not i or i == empty:
            return True
        return False

    # ---
    if 'onlynew' in sys.argv:
        # links = [ x for x in links if not x in words_by_lang[lang] or words_by_lang[lang][x] == 0]
        links = [x for x in links if valid(x, words_by_lang[lang], empty=0)]
    # ---
    lena = len(links)
    # ---
    for title in links:
        # ---
        title_lower = title.lower()
        # ---
        m += 1
        # ---
        words_in = words_by_lang[lang].get(title_lower, 0)
        # ---
        if 'new' in sys.argv and words_in > 40:
            continue
        # ---
        printe.output(f'<<yellow>> title: {m}/{lena} get_w {title}, words_in:{words_in}')
        # ---
        _words = count_words.get_words(title, lang)
        # ---
        if _words is None:
            _words = 0
        # ---
        if words_in != 0 and _words == 0:
            continue
        # ---
        words_by_lang[lang][title_lower] = _words
        # ---
        N_g += 1
        # ---
        if N_g % 100 == 0:
            log_words()


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
        get_w(links, lang)
        # ---
    # ---
    log_words()


def test():
    # ---
    da = ['مرحاض ذو حفرة']
    # ---
    get_w(da, "ar")

    # ---
    # log_words()
    # ---


# ---
if __name__ == '__main__':
    if "test1" in sys.argv:
        TEST = True
        test()
    else:
        start()
