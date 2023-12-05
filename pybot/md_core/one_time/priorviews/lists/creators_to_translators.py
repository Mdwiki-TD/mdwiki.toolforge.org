"""

python3 core8/pwb.py priorviews/lists/creators_to_translators
# ---
from priorviews.lists.creators_to_translators import creators_as_translators
# ---
"""
import json
import os
from pathlib import Path
import datetime
import codecs

# ---
from mdpy import printe

# ---
from priorviews.lists.links_by_section import links_by_lang
from priorviews.lists import translators
from priorviews.bots import helps
from priorviews.lists import creators  # creators.Creators_by_lang_title

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
n = 0
# ---
notadded = 0
added = 0
# ---
for lang, links in links_by_lang.items():
    n += 1
    # ---
    # printe.output(f'<<yellow>> {n}/{len(links_by_lang.keys())} lang: {lang}:')
    # ---
    if lang not in creators_as_translators:
        creators_as_translators[lang] = {}
    # ---
    lang_translations = translators.tra_by_lang.get(lang, {})
    # ---
    links = [x for x in links if lang_translations.get(x.lower(), '') == '']
    # ---
    for title in links:
        # ---
        _creator = creators.Creators_by_lang_title.get(lang, {}).get(title, {})
        # ---
        TD = _creator.get("TD")
        actor = _creator.get("actor", "")
        # ---
        _time_ = _creator.get("time", "")
        _time_x = ''
        # ---
        if actor == '':
            continue
        # ---
        year = '0'
        # ---
        if _time_ != '':
            # Convert _time_ to a datetime object
            datetime_obj = datetime.datetime.strptime(str(_time_), '%Y%m%d%H%M%S')
            _time_x = datetime_obj.strftime('%Y-%m-%d')
            year = datetime_obj.strftime('%Y')
        # ---
        if TD or int(year) > 2012:
            creators_as_translators[lang][title] = actor
            added += 1
            # ---
            # printe.output(f'<<blue>> {added}: {title}, actor: {actor}, TD: {TD}')
        else:
            notadded += 1
# ---
printe.output(f'<<blue>> added: {added}')
printe.output(f'<<blue>> notadded: {notadded}')
# ---
if __name__ == '__main__':
    # dump creators_as_translators
    helps.dump_data(file_cts, creators_as_translators)
    # ---
