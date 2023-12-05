'''

python3 core8/pwb.py WHOem/lists/find_views en

'''
import sys
import json
import os
from pathlib import Path
import codecs
import time
import datetime
from datetime import timedelta

# ---
from mdpy import printe
from mdpy.bots import wiki_api
from priorviews.bots import helps

# ---
TEST = False
# ---
Dir = Path(__file__).parent
# ---
with codecs.open(f'{Dir}/lang_links.json', 'r', encoding='utf-8') as f:
    lang_links = json.load(f)  # {'en': 'enwiki', 'redirect_to': '', 'langs': {'ar': 'arwiki'}}
# ---
file = f'{Dir}/views.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
with codecs.open(file, 'r', encoding='utf-8') as f:
    ViewsData = json.load(f)
# ---
N_g = 0


def log_views():
    printe.output(f'<<yellow>> log_views {len(ViewsData)} views')
    # dump ViewsData
    helps.dump_data(file, ViewsData)


def api_views(title, lang):
    # ---
    d_end = datetime.datetime.utcnow() - timedelta(days=1)
    d_start = d_end - timedelta()
    # ---
    d_end = d_end.strftime('%Y%m%d')
    # ---
    d_start = "20110101"
    # ---
    d_start = ""
    # ---
    enviews = wiki_api.get_views_with_rest_v1(lang, [title])
    # ---
    if 'sleep' in sys.argv:
        time.sleep(1)
    # ---
    if not enviews or enviews == {}:
        return 0
    # ---
    vs = enviews.get(title, {}).get('all', 0)
    # ---
    return vs


def get_v(mdtitle, langslinks):
    # ---
    global ViewsData, N_g
    # ---
    for lang, title in langslinks.items():
        # ---
        if lang != "en" and "en" in sys.argv:
            continue
        # ---
        viws_in = ViewsData[mdtitle].get(lang, {}).get('views', 0)
        # ---
        if 'new' in sys.argv and viws_in != 0:
            continue
        # ---
        viws = api_views(title, lang)
        # ---
        printe.output(f't: {title} - {lang} - views: {viws}')
        # ---
        if viws is None:
            continue
        # ---
        if viws_in != 0 and viws == 0:
            continue
        # ---
        ViewsData[mdtitle][lang] = {"title": title, "views": viws}
        # ---
        N_g += 1
        # ---
        if N_g % 100 == 0:
            log_views()


def start():
    # ---
    # len of tab in lang_links
    all_lenth = sum(len(tab['langs'].keys()) for tab in lang_links.values())
    # ---
    if 'en' in sys.argv:
        all_lenth = len(lang_links)
    # ---
    n = 0
    # ---
    for mdtitle, tab in lang_links.items():
        # ---
        n += 1
        # ---
        if mdtitle not in ViewsData:
            ViewsData[mdtitle] = {}
        # ---
        printe.output(f'<<blue>> p:{n}/{all_lenth} mdtitle: {mdtitle}')
        # ---
        langslinks = tab['langs']
        # printe.output(f'langslinks: {len(langslinks)}')
        # ---
        get_v(mdtitle, langslinks)
        # ---
    # ---
    log_views()


if __name__ == '__main__':
    start()
