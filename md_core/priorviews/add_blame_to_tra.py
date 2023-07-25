'''

python3 core8/pwb.py priorviews/add_blame_to_tra

'''

import sys
import os
import re
import json
import sys
import codecs
# ---
from mdpy import printe
# ---
from priorviews.find.find_blame import new_data
from priorviews.lists.translators import tra_by_lang
# ---
Dir = os.path.dirname(os.path.abspath(__file__))
# ---
file = f'{Dir}/lists/blames.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
new_data = json.load(codecs.open(file, 'r', 'utf-8'))
# ---


def add_to_translators():
    for lang, titles in new_data.items():
        # ---
        if not lang in tra_by_lang:
            tra_by_lang[lang] = {}
        # ---
        for title, user in titles.items():
            if user == '':
                continue
            # ---
            in_ = tra_by_lang[lang].get(title, "")
            # ---
            if in_ == '':
                tra_by_lang[lang][title] = user
                printe.output(f'<<green>> {lang=}, {title=}, {user=}')
            elif in_ != user:
                printe.output(f'<<red>> userin: {in_}, new: {user}')
    # ---
    file = f'{Dir}/lists/translators_mdwiki_langs.json'
    # ---
    with codecs.open(file, 'w', 'utf-8') as zf:
        json.dump(tra_by_lang, zf, ensure_ascii=False)  # ---


# ---
if __name__ == '__main__':
    add_to_translators()
