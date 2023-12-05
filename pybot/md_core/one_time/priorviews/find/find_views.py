'''

python3 core8/pwb.py priorviews/find/find_views test

'''
from priorviews.lists.links_by_section import sects_links_langlinks
import sys
import json
import os
from pathlib import Path
import codecs
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
Dir2 = os.path.dirname(Dir)
# ---
file = f'{Dir2}/lists/views_mdwiki_langs.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
# ---
ViewsData = json.load(codecs.open(file, 'r', 'utf-8'))


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
    # d_start = d_start.strftime('%Y%m%d')
    d_start = "20110101"
    # ---
    enviews = wiki_api.get_views_with_rest_v1(lang, [title], date_start=d_start, date_end=d_end, printurl=TEST)
    # ---
    if not enviews or enviews == {}:
        return 0
    # ---
    vs = enviews.get(title, {}).get('all', 0)
    # ---
    # ---
    return vs


# ---
N_g = 0


def get_v(links):
    # ---
    global ViewsData, N_g
    # ---
    m = 0
    # ---
    lena = len(links.keys())
    # ---
    for mdtitle, langs in links.items():
        # ---
        m += 1
        # ---
        if mdtitle not in ViewsData:
            ViewsData[mdtitle] = {}
        # ---
        printe.output(f'<<yellow>> title: {m}/{lena} get_v {mdtitle}')
        # ---
        if "en" in sys.argv:
            langs['en'] = mdtitle
        # ---
        leno = len(langs.keys())
        # ---
        for lang, title in langs.items():
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
            print(f'title {N_g}/{leno}: {title} - {lang} - {viws}')
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
    n = 0
    # ---
    # make text for each section
    for section, links in sects_links_langlinks.items():
        # ---
        print(f'section: {section}')
        print(f'links: {len(links)}')
        # ---
        n += 1
        # ---
        get_v(links)
        # ---
    # ---
    log_views()


def test():
    # ---
    da = {
        "Pit latrine": {
            'ar': 'مرحاض ذو حفرة',
            'bn': 'খাটা পায়খানা',
            'ca': 'Latrina de fossa',
            'ee': 'Do nugododeƒe',
            'es': 'Letrina de hoyo',
            'fa': 'توالت گودالی',
            'ha': 'Shaddar gargajiya',
            'hi': 'खुड्डी शौचालय',
            'ig': 'Ụlọ mposi',
            'it': 'Latrina a fossa',
            'ln': 'Latrine ya libulu',
            'nso': 'Boithomelo bja mokoti',
            'or': 'ବରପାଲି ପାଇଖାନା',
            'pl': 'Latryna',
            'ru': 'Ямный туалет',
            'sw': 'Choo cha shimo',
            'ta': 'குழி கழிவறை',
            'tr': 'Köy tuvaleti',
            'ur': 'گڑھے والا بیت الخلا',
            'wo': 'Duus',
            'xh': 'Ithoyilethi yomngxuma',
            'yo': 'Ṣalanga oniho',
            'zh': '旱廁',
            'zu': 'Ithoyilethe lomgodi',
        }
    }
    # ---
    get_v(da)
    # ---
    log_views()

    # ---


# ---
if __name__ == '__main__':
    if "test1" in sys.argv:
        TEST = True
        test()
    else:
        start()
