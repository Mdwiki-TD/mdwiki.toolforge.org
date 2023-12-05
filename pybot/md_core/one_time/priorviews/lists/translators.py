'''
# ---
from priorviews.lists import translators
# translators.tra_by_lang
# translators.counts_by_translator
# translators.counts_by_lang
# ---
python3 core8/pwb.py priorviews/lists/translators

'''
from priorviews.bots import helps
import json
import os
from pathlib import Path
import codecs

# ---
Dir = Path(__file__).parent
# ---
file = f'{Dir}/translators_mdwiki_langs.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
tra_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))
# ---
_data = {"ar": {"artitle": "بيت الحكمة"}}
# ---
# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# ---
counts_by_translator = {}
counts_by_lang = {}
# ---
# Iterate through each markdown file and language in `tra_by_lang`
for lang, titles in tra_by_lang.items():
    # ---
    if lang not in counts_by_translator:
        counts_by_translator[lang] = {}
    if lang not in counts_by_lang:
        counts_by_lang[lang] = 0
    # ---
    for title, user in titles.items():
        # ---
        if user == '':
            continue
        # ---
        # skip user match ip address
        if helps.is_ip(user):
            continue
        # ---
        if user not in counts_by_translator[lang]:
            counts_by_translator[lang][user] = 0
        counts_by_translator[lang][user] += 1
        # ---
        counts_by_lang[lang] += 1
# ---
if __name__ == '__main__':
    # for x, wo in counts_by_translator.items():   print(x, wo)
    # ---
    print(f'len of counts_by_translator: {len(counts_by_translator)}')
    # ---
    print(f'len of tra_by_lang: {len(tra_by_lang)}')
    for lang, titles in tra_by_lang.items():
        for title, user in titles.items():
            if user != '':
                print(f'{lang=}, {title=}, {user=}')
# ---
