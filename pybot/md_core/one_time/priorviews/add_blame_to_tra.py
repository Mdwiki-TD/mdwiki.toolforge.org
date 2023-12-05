'''

python3 core8/pwb.py priorviews/add_blame_to_tra

'''

import sys
from pathlib import Path
import json

# ---
from mdpy import printe

# ---
from priorviews.find.find_blame import new_data
from priorviews.lists.translators import tra_by_lang
from priorviews.bots import helps

# ---
Dir = Path(__file__).parent
# ---
skip_users = ["doc james"]


def add_to_translators():
    sk = 0
    new = 1
    dd = 1
    for lang, titles in new_data.items():
        # ---
        if lang not in tra_by_lang:
            tra_by_lang[lang] = {}
        # ---
        titles = {title: user for title, user in titles.items() if user != ''}
        # ---
        if not titles:
            continue
        # ---
        # titles no bots
        titles_bots = [user for title, user in titles.items() if user != '' and user.lower().endswith('bot')]

        titles_no_bots = {title: user for title, user in titles.items() if user != '' and not user.lower().endswith('bot')}

        # printe.output(f'<<blue>> lang:{lang} found {len(titles_bots)} bots, {len(titles_no_bots)} no bots')

        # ---
        for title, user in titles_no_bots.items():
            # ---
            if user.lower().endswith('bot'):
                sk += 1
                # printe.output(f'<<red>> {sk} skip bots: {lang=}, {title=}, {user=}')
                continue
            # ---
            in_ = tra_by_lang[lang].get(title, "")
            # ---
            if in_ == user or user.lower() in skip_users:
                continue
            # ---
            if in_ == '' or in_.lower() in skip_users or helps.is_ip(in_):
                new += 1
                tra_by_lang[lang][title] = user
                printe.output(f'<<green>> {new=} {lang=}, {title=}, {user=}, old: {in_}')
            elif in_ != user:
                dd += 1
                printe.output(f'<<purple>> {dd=} skip, userin: {in_=}, new: {user}')
        # ---
    # ---
    file = f'{Dir}/lists/translators_mdwiki_langs.json'
    # ---
    helps.dump_data(file, tra_by_lang)
    # with codecs.open(file, 'w', 'utf-8') as zf: json.dump(tra_by_lang, zf, ensure_ascii=False)


def sea55():
    data = json.load(open(f'{Dir}/sea55.json', encoding='utf-8'))
    # ---
    n = 0
    # ---
    for lang, titls in data.items():
        if lang not in new_data:
            new_data[lang] = {}
        # ---
        for title in titls:
            if title.lower() not in new_data[lang] and title not in new_data[lang]:
                n += 1
                printe.output(f'<<red>>{n=}/{len(titls)} {lang=}, {title=}')
                new_data[lang][title.lower()] = ""
        # ---
    # ---
    file = f'{Dir}/lists/blames.json'
    # ---
    # with open(file, 'w', encoding='utf-8') as zf:   json.dump(new_data, zf, ensure_ascii=False)
    helps.dump_data(file, new_data)

    # ---


# ---
if __name__ == '__main__':
    # ---
    if 'sea55' in sys.argv:
        sea55()
    else:
        add_to_translators()
