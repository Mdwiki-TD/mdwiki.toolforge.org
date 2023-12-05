"""

python3 core8/pwb.py priorviews/langs -lang:ar write ask

"""
import sys
import json
from pathlib import Path
import datetime
import codecs

# ---
from mdpy import printe

# ---
from priorviews.lists.links_by_section import sects_links_langlinks, links_by_lang
from priorviews.lists import views

# ---
from priorviews.bots import helps

# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# helps.talk_url(lang, user, labl)
# ---
from priorviews.bots import w_all

# ---
from new_api.mdwiki_page import MainPage as md_MainPage

# ---
Dir = Path(__file__).parent
# ---
translators_all = {}
# ---
tab_new = {}
# ---
tab_new['links'] = {}
# ---
for section, links in sects_links_langlinks.items():
    # ---
    for x in links:
        tab_new['links'][x] = {
            'section': section,
            'views': 0
        }
    # ---
# ---
sql_file = f'{Dir}/lists/tab_new.json'
# ---
tab_new['translates'] = []  # ['mdtitle', 'target', 'lang', 'views', 'type']


def make_lang_textso(lang):
    # ---
    secs_texts = '==by section=='
    lang_views = 0
    lang_words = 0
    # ---
    all_links = 0
    all_links_with_ar = 0
    # ---
    for section, links in sects_links_langlinks.items():
        # ---
        tab = {
            x: v[lang]
            for x, v in links.items() if lang in v
        }
        # ---
        all_links += len(links)
        all_links_with_ar += len(tab)
        # ---
        # diff = len(links) - len(tab)
        # ---
        secs_texts += f'\n==={section}===\n'
        secs_texts += f'* section links: {len(links)}\n'
        secs_texts += f'* with ({lang}) translations: {len(tab)}'
        # ---
        if len(tab) > 0:
            secs_texts += '\n\n'
            # ---
            head_table = '{| class="wikitable sortable mw-collapsible mw-collapsed plainrowheaders"\n|-\n'
            # ---
            if len(tab) < 20:
                head_table = '{| class="wikitable sortable"\n|-\n'
            # ---
            secs_texts += head_table
            secs_texts += f'! # !! title !! {lang} !! views !! time\n|-\n'
            # ---
            n = 0
            # ---
            for x, ar in tab.items():
                n += 1
                secs_texts += "|-\n"
                # ---
                arviews = views.views_by_lang.get(lang, {}).get(ar.lower(), 0)
                # ---
                lang_views += arviews
                # ---
                view_u = helps.views_url(ar, lang, arviews)
                # ---
                _creat = {}
                # ---
                _time_x = _creat.get("time", "")
                # ---
                if _time_x != '':
                    # Convert _time_x to a datetime object
                    datetime_obj = datetime.datetime.strptime(str(_time_x), '%Y%m%d%H%M%S')
                    _time_x = datetime_obj.strftime('%Y-%m-%d')
                # ---
                _cr_ = ''
                # ---
                fafo = {
                    'mdtitle': x,
                    'target': ar,
                    'lang': lang,
                    'views': arviews,
                }
                # ---
                tab_new['translates'].append(fafo)
                # ---
                secs_texts += f"| {n} || [[{x}]] || [[w:{lang}:{ar}|{ar}]] || {view_u} || {_cr_} || {_time_x}\n"
            # ---
            secs_texts += "|}\n"
    # ---
    newtext = '[https://:' + f'{lang}.wikipedia.org {lang}.wikipedia.org] statistics:\n'
    newtext += f'* All links: {all_links:,}\n'
    newtext += f'** With ({lang}) translations: {all_links_with_ar:,}\n'
    newtext += f'* Views: {lang_views:,} (from July 2015 to June 2023)\n'
    newtext += f'* Words: {lang_words:,}\n'
    newtext += '\n'
    # ----
    print(newtext)
    # ----
    newtext += "\n\n"
    newtext += secs_texts
    # ---
    return newtext


def work(lang):
    # ---
    newtext = make_lang_textso(lang)
    # ---
    if 'write' not in sys.argv:
        return
    # ---
    page = md_MainPage(f'User:Mr. Ibrahem/priorviews/bylang/{lang}', 'www', family='mdwiki')
    exists = page.exists()
    text = page.get_text()
    if not exists:
        create = page.Create(text=newtext, summary='update')
    elif text != newtext:
        # ---
        save_page = page.save(newtext=newtext, summary='update', nocreate=1, minor='')
    else:
        print('no change')

    # ---


# ---
if __name__ == "__main__":
    langs = links_by_lang.keys()
    # ---
    wrtire = True
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langs = [value]
            wrtire = False
    # ---
    lenn = len(langs)
    # ---
    n = 0
    # ---
    for lang in langs:
        n += 1
        printe.output(f'<<yellow>> {n}/{lenn} langs.py lang: {lang}')
        # ---
        work(lang)
    # ---
    if wrtire:
        w_all.work_all(translators_all)
    # ---
    json.dump(tab_new, codecs.open(sql_file, 'w', 'utf-8'), indent=4)
    # ---
