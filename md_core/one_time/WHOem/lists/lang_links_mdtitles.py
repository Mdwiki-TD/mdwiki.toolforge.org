'''

python3 core8/pwb.py WHOem/lists/find_views_by_lang

'''
import json
from pathlib import Path
import codecs

# ---
# ---
Dir = Path(__file__).parent
# ---
with codecs.open(f'{Dir}/lang_links.json', 'r', encoding='utf-8') as f:
    lang_links = json.load(f)  # {'en': 'enwiki', 'redirect_to': '', 'langs': {'ar': 'arwiki'}}
# ---
lang_links_mdtitles = {lang: {} for mdtitle, tab in lang_links.items() for lang in tab['langs'].keys()}
# ---
for lang in lang_links_mdtitles.keys():
    lang_links_mdtitles[lang] = {tab['langs'][lang]: md for md, tab in lang_links.items() if lang in tab['langs']}
# ---
with codecs.open(f'{Dir}/lang_links_mdtitles.json', 'w', encoding='utf-8') as f:
    json.dump(lang_links_mdtitles, f, ensure_ascii=False, indent=4)
# ---
# sort lang_links_mdtitles by lenth
lang_links_mdtitles = dict(sorted(lang_links_mdtitles.items(), key=lambda x: len(x[1]), reverse=True))
# ---
# print first 10 of lang_links_mdtitles
to_p = dict(list(lang_links_mdtitles.items())[0:10])
# ---
for x, z in to_p.items():
    print(x, len(z))
# ---
