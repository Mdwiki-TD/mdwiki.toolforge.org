'''
# ---
from priorviews.lists import creators
# creators.Creators_by_lang_title
# creators.counts_creators_by_lang
# ---
python3 core8/pwb.py priorviews/lists/creators

'''
import sys
import json
import os
from pathlib import Path
import re
import codecs

# ---
from priorviews.bots import helps

# ---
Dir = Path(__file__).parent
# ---
file_cts = f'{Dir}/creators_as_translators.json'
# ---
if not os.path.exists(file_cts):
    with open(file_cts, 'w') as f:
        json.dump({}, f)
# ---
creators_as_translators = json.load(codecs.open(file_cts, 'r', 'utf-8'))
# ---
file = f'{Dir}/creators_by_lang.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
CreatorsData = json.load(codecs.open(file, 'r', 'utf-8'))
# ---
Creators_by_lang_title = {}
# ---
counts_creators_by_lang = {}
# ---
Dump_it = False
# ---
# Iterate through each markdown file and language in `CreatorsData`
for lang in CreatorsData.copy():
    # ---
    titles = CreatorsData[lang]
    # ---
    if lang not in counts_creators_by_lang:
        counts_creators_by_lang[lang] = {}
    if lang not in Creators_by_lang_title:
        Creators_by_lang_title[lang] = {}
    # ---
    for title, tab in titles.items():
        # ---
        actor = tab["actor"]
        _time_ = tab["time"]
        TD = tab["TD"]
        comment = tab["comment"]
        # ---
        if comment.find("|User:Mr. Ibrahem/") == -1 and TD:
            Dump_it = True
            print('false TD..')
            CreatorsData[lang][title]['TD'] = False
        # ---
        # if actor match IP address : skip
        if re.match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", actor):
            continue
        # ---
        if actor not in counts_creators_by_lang[lang]:
            counts_creators_by_lang[lang][actor] = 0
        counts_creators_by_lang[lang][actor] += 1
        # ---
        Creators_by_lang_title[lang][title] = tab
        # ---
# ---
if Dump_it:
    helps.dump_data(file, CreatorsData)
# ---
if __name__ == '__main__':
    if 'dd' not in sys.argv:
        print(f'len of Creators_by_lang_title: {len(Creators_by_lang_title)}')
        for lang, titles in Creators_by_lang_title.items():
            for title, words in titles.items():
                print(lang, title, words)

        for x, wo in counts_creators_by_lang.items():
            print(x)
            for x, z in wo.items():
                print(x, z)
        # ---
        print(f'len of counts_creators_by_lang: {len(counts_creators_by_lang)}')
        # ---

# ---
