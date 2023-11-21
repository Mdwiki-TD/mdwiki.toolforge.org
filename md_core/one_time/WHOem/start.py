'''

python3 core8/pwb.py WHOem/start enonly

'''
from WHOem import get_them
from new_api.wiki_page import change_codes
from mdpy import printe
import sys
import os
import json
import codecs
from pathlib import Path

# ---
Dir = Path(__file__).parent
# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
with codecs.open(f'{Dir}/lists/md_links.json', 'r', encoding='utf-8') as f:
    md_links = json.load(f)
# ---
with codecs.open(f'{Dir}/lists/lang_links.json', 'r', encoding='utf-8') as f:
    lang_links = json.load(f)  # {'en': 'enwiki', 'redirect_to': '', 'langs': {'ar': 'arwiki'}}
# ---
with codecs.open(f'{Dir}/lists/links_not_found.json', 'r', encoding='utf-8') as f:
    links_not_found = json.load(f)  # ["error"]
# ---
allen = {}


def work_lang_links(x, langs):
    # --
    n = 0
    # --
    for lang, tit in langs.items():
        # ---
        n += 1
        # ---
        lang = change_codes.get(lang) or lang
        # ---
        if lang == 'simple':
            continue
        # ---
        tata = {'title': tit, 'extlinks': [], 'refsname': []}
        # ---
        allen[title]['langs'][lang] = tata
        # ---
        if 'enonly' in sys.argv:
            continue
        # ---
        tatnn = get_them.work_in_one_lang_link(lang, tit)
        # ---
        # text1 = tatnn.text
        extlinks1 = tatnn.extlinks
        refsname1 = tatnn.refsname
        # ---
        tata['extlinks'] = extlinks1
        tata['refsname'] = refsname1
        # ---
        lenex = str(len(tata["extlinks"])).ljust(4)
        lenre = str(len(tata["refsname"])).ljust(4)
        # ---
        printe.output(f'\tp{n}/{len(langlinks)}:\t{lang.ljust(20)}\t{lenex} extlinks, {lenre} refsname..')
        # ---
        allen[title]['langs'][lang] = tata


def start_all():
    # ---
    # start work in allens
    # ---
    printe.output(f'len of lang_links: {len(lang_linkss)}')
    # ---
    no = 0
    # ---
    for x, va in lang_links.items():
        no += 1
        # ---
        pap = f'p {n}/{len(lang_links)}: {x}'
        # ---
        printe.output(pap)
        # ---
        work_lang_links(x, va['langs'])
        # ---
    with codecs.open(f'{Dir}/lists/start.json', 'w', encoding='utf-8') as f:
        json.dump(allen, f, ensure_ascii=False, indent=4)


# ---
if __name__ == '__main__':
    start_all()
