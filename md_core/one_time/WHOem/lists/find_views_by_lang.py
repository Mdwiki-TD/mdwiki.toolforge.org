'''

python3 core8/pwb.py WHOem/lists/find_views_by_lang

'''
import sys
import json
import os
from pathlib import Path
import codecs

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
with codecs.open(f'{Dir}/lang_links_mdtitles.json', 'r', encoding='utf-8') as f:
    lang_links_mdtitles = json.load(f)
# ---
file = f'{Dir}/views.json'
# ---
if not os.path.exists(file):
    with open(file, 'w', encoding='utf-8') as f:
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


def get_v(lang, links):
    # ---
    global ViewsData, N_g
    # ---
    len_p = len(links)
    # -- -
    if 'new' in sys.argv:
        links = {x: t for x, t in links.items() if ViewsData[t].get(lang, {}).get('views', 0) == 0}
        de = len_p - len(links)
        printe.output(f'de: {de}')
    # ---
    # split links to groups by 10 titles
    for i in range(0, len(links), 10):
        group = dict(list(links.items())[i : i + 10])
        # ---
        views_tab = wiki_api.get_views_with_rest_v1(lang, group.keys())
        # ---
        for title, views in views_tab.items():
            # ---
            # _views_ = {"all": 14351,"2021": {"all": 907,"202108": 186},"2022": {"all": 5750,"202201": 158}}
            # ---
            mdtitle = lang_links_mdtitles.get(lang, {}).get(title, None)
            if mdtitle is None:
                continue
            # ---
            views = views['all']
            # ---
            viws_in = ViewsData[mdtitle].get(lang, {}).get('views', 0)
            # ---
            printe.output(f't: {title} - {lang} - views: {views}')
            # ---
            # ViewsData.setdefault(mdtitle, {})[lang] = ViewsData[mdtitle].setdefault(lang, {})
            # ---
            # ViewsData.setdefault(mdtitle, {})
            if mdtitle not in ViewsData.keys():
                ViewsData[mdtitle] = {}
            # ---
            # ViewsData[mdtitle].setdefault(lang, {})
            if lang not in ViewsData[mdtitle].keys():
                ViewsData[mdtitle][lang] = {}
            # ---
            if viws_in > 0 and views == 0:
                continue
            # ---
            ViewsData[mdtitle][lang] = {"title": title, "views": views}
            # ---
            N_g += 1
            # ---
            if N_g % 100 == 0:
                log_views()


def start():
    # ---
    # len of tab in lang_links
    all_lenth = sum(len(tab.keys()) for tab in lang_links_mdtitles.values())
    # ---
    to_work = lang_links_mdtitles
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        if arg == 'lang' and value in lang_links_mdtitles.keys():
            all_lenth = len(lang_links_mdtitles.get(value, {}))
            to_work = {value: lang_links_mdtitles[value]}
            printe.output(f'<<purple>> work in lang: {value}')
    # ---
    n = 0
    # ---
    for lang, tab in to_work.items():
        # ---
        n += 1
        # ---
        ViewsData.update({x: {} for x in tab.values() if x not in ViewsData})
        # ---
        printe.output(f'<<blue>> p:{n}/{all_lenth} lang: {lang}, titles: {len(tab)}')
        # ---
        get_v(lang, tab)
        # ---
    # ---
    log_views()


if __name__ == '__main__':
    if 'fix' in sys.argv:
        ViewsData = {x: z for x, z in ViewsData.items() if x in lang_links.keys()}
        with codecs.open(file, 'w', encoding='utf-8') as f:
            json.dump(ViewsData, f, ensure_ascii=False, indent=4)
        print(f'len ViewsData: {len(ViewsData)}')
    else:
        start()
