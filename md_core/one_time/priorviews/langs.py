"""

python3 core8/pwb.py priorviews/langs -lang:ar write ask

"""
from priorviews.lists import creators
from priorviews.lists.creators_to_translators import creators_as_translators
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
from priorviews.lists import translators
from priorviews.lists import words

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
# ---
# creators.Creators_by_lang_title
# creators.counts_creators_by_lang
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
        tab_new['links'][x] = {'section': section, 'words': 0, 'views': 0}
    # ---
# ---
sql_file = f'{Dir}/lists/tab_new.json'
# ---
tab_new['translates'] = []  # ['mdtitle', 'target', 'lang', 'views', 'words', 'translator', 'type']


def authors_table(authors, lang):
    # authors_text += "\n*".join( [ f"{x}: {v}" for x, v in authors.items()])
    # ----
    tab2 = {}
    for user, cunts in authors.items():
        if cunts not in tab2:
            tab2[cunts] = []
        tab2[cunts].append(user)
    # ---
    # sort tab2 by keys
    tab2 = dict(sorted(tab2.items(), key=lambda item: item[0], reverse=True))
    # ---
    authors_text = '{| class=wikitable sortable\n|-\n!count!!users\n|-\n'
    # ---
    lang_cunt = 0
    # ---
    for cunts, users in tab2.items():
        # ---
        for u in users:
            lang_cunt += cunts
        # ---
        users.sort()
        # ---
        usrs_line = ', '.join([helps.talk_url(lang, x, x) for x in users])
        # ---
        authors_text += f'\n! {cunts} \n| {usrs_line}\n|-'
        # ---
    # ---
    authors_text += '\n|}'
    # ---
    return authors_text


def make_lang_textso(lang):
    # ---
    authors = {}
    authors_2 = {}
    # ---
    secs_texts = '==by section=='
    lang_views = 0
    lang_words = 0
    # ---
    TD_all = 0
    tr_all = 0
    # ---
    all_links = 0
    all_links_with_ar = 0
    # ---
    for section, links in sects_links_langlinks.items():
        # ---
        tab = {x: v[lang] for x, v in links.items() if lang in v}
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
            secs_texts += f'! # !! title !! {lang} !! views !! words !! translator !! creator !! time\n|-\n'
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
                arwords = words.words_by_lang.get(lang, {}).get(ar.lower(), 0)
                # ---
                lang_words += arwords
                # ---
                ar_tra = translators.tra_by_lang.get(lang, {}).get(ar.lower(), '')
                # ---
                _creat = creators.Creators_by_lang_title.get(lang, {}).get(ar, {})
                _creat_user = _creat.get("actor", "")
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
                tr_type = ''
                # ---
                if ar_tra == '':
                    ar_tra = creators_as_translators.get(lang, {}).get(ar, '')
                    if ar_tra != '':
                        tr_type = 'creator'
                else:
                    tr_type = 'translator'
                # ---
                if _creat_user != '' and ar_tra == '':
                    _cr_ = f"[[w:{lang}:User:{_creat_user}|{_creat_user}]]"
                # ---
                wi_tra = ar_tra
                # ---
                if ar_tra != '':
                    tr_all += 1
                    # ---
                    wi_tra = f"[[w:{lang}:User:{ar_tra}|{ar_tra}]]"
                    # ---
                    if wi_tra not in authors:
                        authors[wi_tra] = 0
                    authors[wi_tra] += 1
                    # ---
                    if ar_tra not in authors_2:
                        authors_2[ar_tra] = 0
                    authors_2[ar_tra] += 1
                    # ---
                    if ar_tra not in translators_all:
                        translators_all[ar_tra] = {'all': 0, 'by_lang': {}}
                    # ---
                    if lang not in translators_all[ar_tra]['by_lang']:
                        translators_all[ar_tra]['by_lang'][lang] = 0
                    translators_all[ar_tra]['by_lang'][lang] += 1
                    # ---
                    translators_all[ar_tra]['all'] += 1
                # ---
                fafo = {'mdtitle': x, 'target': ar, 'lang': lang, 'views': arviews, 'words': arwords, 'translator': ar_tra, 'tr_type': tr_type}
                # ---
                tab_new['translates'].append(fafo)
                # ---
                secs_texts += f"| {n} || [[{x}]] || [[w:{lang}:{ar}|{ar}]] || {view_u} || {arwords} || {wi_tra} || {_cr_} || {_time_x}\n"
            # ---
            secs_texts += "|}\n"
    # ---
    newtext = '[https://:' + f'{lang}.wikipedia.org {lang}.wikipedia.org] statistics:\n'
    newtext += f'* All links: {all_links:,}\n'
    newtext += f'** With ({lang}) translations: {all_links_with_ar:,}\n'
    newtext += f"*** With translators: {tr_all:,}\n"
    # if TD_all > 0:
    # newtext += f"*** Articles translated by Translation Dashboard: {TD_all:,}\n"
    newtext += f'* Views: {lang_views:,} (from July 2015 to June 2023)\n'
    newtext += f'* Words: {lang_words:,}\n'
    newtext += '\n'
    # ----
    print(newtext)
    # ----
    # authors = sorted(authors.items(), key=lambda x: x[1])
    authors_2 = {x: v for x, v in sorted(authors_2.items(), key=lambda item: item[1], reverse=True)}
    authors_text = "\n==Translators==\n"
    # ----
    authors_text += authors_table(authors_2, lang)
    # ----
    newtext += authors_text
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
