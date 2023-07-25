"""

python3 core8/pwb.py priorviews/langs -lang:ar write ask

"""
import sys
import pywikibot
import json
import os
import urllib.parse
import re
import datetime
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
from mdpy import printe
#---
from priorviews.lists.links_by_section import sects_links_langlinks, links_by_lang
from priorviews.lists import views 
from priorviews.lists import translators 
from priorviews.lists import words 
from priorviews.bots import helps
from priorviews.bots import w_all
#---
from new_api.mdwiki_page import MainPage as md_MainPage
#---
#---
from priorviews.lists import creators 
# creators.Creators_by_lang_title
# creators.counts_creators_by_lang
#---
translators_all = {}
#---
def talk_url(lang, user, labl):
    old = f'[[w:{lang}:User talk:{user}|{user}]]'
    # --
    pas = {'title': f'User_talk:{user}', 'action': 'edit', 'section': 'new'}
    url = f"//{lang}.wikipedia.org/w/index.php?" + urllib.parse.urlencode(pas)
    # ---
    return f'[{url} {labl}]'
#---
def authors_table(authors, lang):
    # authors_text += "\n*".join( [ f"{x}: {v}" for x, v in authors.items()])
    #----
    tab2 = {}
    for user, cunts in authors.items():
        if not cunts in tab2:
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
        usrs_line = ', '.join([talk_url(lang, x, x) for x in users])
        # ---
        authors_text += f'\n! {cunts} \n| {usrs_line}\n|-'
        # ---
    # ---
    authors_text += '\n|}'
    # ---
    return authors_text
#---
def make_lang_textso(lang):
    #---
    authors = {}
    authors_2 = {}
    #---
    secs_texts = '==by section=='
    lang_views = 0
    lang_words = 0
    #---
    creator_as_translator = 0
    #---
    TD_all = 0
    tr_all = 0
    #---
    all_links  = 0
    all_links_with_ar  = 0
    #---
    for section, links in sects_links_langlinks.items():
        #---
        tab = { x: v[lang] for x, v in links.items() if lang in v}
        #---
        all_links += len(links)
        all_links_with_ar += len(tab)
        #---
        # diff = len(links) - len(tab)
        #---
        secs_texts += f'\n==={section}===\n'
        secs_texts += f'* section links: {len(links)}\n'
        secs_texts += f'* with ({lang}) translations: {len(tab)}'
        #---
        if len(tab) > 0:
            secs_texts += '\n\n'
            #---
            head_table = '{| class="wikitable sortable mw-collapsible mw-collapsed plainrowheaders"\n|-\n'
            #---
            if len(tab) < 20:
                head_table = '{| class="wikitable sortable"\n|-\n'
            #---
            secs_texts += head_table
            secs_texts += f'! # !! title !! {lang} !! views !! words !! translator !! creator !! time\n|-\n'
            #---
            n = 0
            #---
            for x, ar in tab.items():
                n += 1
                secs_texts += "|-\n"
                #---
                arviews = views.views_by_lang.get(lang, {}).get(ar.lower(), 0)
                #---
                lang_views += arviews
                #---
                view_u = helps.views_url(ar, lang, arviews)
                #---
                arwords = words.words_by_lang.get(lang, {}).get(ar.lower(), 0)
                #---
                lang_words += arwords
                #---
                ar_tra  = translators.tra_by_lang.get(lang, {}).get(ar.lower(), '')
                #---
                _creator = creators.Creators_by_lang_title.get(lang, {}).get(ar, {})
                _cr_   = _creator.get("actor", "")
                _time_ = _creator.get("time", "")
                TD     = _creator.get("TD")
                #---
                _time_x = _time_
                #---
                tata = 0
                #---
                if _time_ != '':
                    # Convert _time_ to a datetime object
                    datetime_obj = datetime.datetime.strptime(str(_time_), '%Y%m%d%H%M%S')
                    # Format the datetime object as "YYYY-MM-DD"
                    year = datetime_obj.strftime('%Y')
                    if int(year) > 2012 and ar_tra == '':
                        ar_tra = _cr_
                        tata = 1
                    formatted_date = datetime_obj.strftime('%Y-%m-%d')
                    # Assign the formatted date to _time_
                    _time_x = formatted_date
                #---
                if TD:
                    TD_all += 1
                    #---
                    if ar_tra == '' or ar_tra == _cr_:
                        tata = 1
                        ar_tra = _cr_
                        _cr_   = 'TD'
                #---
                creator_as_translator += tata
                #---
                _cr_2 = _cr_
                #---
                if _cr_ not in ['TD', '']:
                    _cr_2 = f"[[w:{lang}:User:{_cr_}|{_cr_}]]"
                #---
                wi_tra = ar_tra
                #---
                if ar_tra != '':
                    tr_all += 1
                    #---
                    wi_tra = f"[[w:{lang}:User:{ar_tra}|{ar_tra}]]"
                    #---
                    if not wi_tra in authors: authors[wi_tra] = 0
                    authors[wi_tra] += 1
                    #---
                    if not ar_tra in authors_2: authors_2[ar_tra] = 0
                    authors_2[ar_tra] += 1
                    #---
                    if not ar_tra in translators_all: translators_all[ar_tra] = {'all': 0, 'by_lang': {}}
                    #---
                    if not lang in translators_all[ar_tra]['by_lang']: translators_all[ar_tra]['by_lang'][lang] = 0
                    translators_all[ar_tra]['by_lang'][lang] += 1
                    #---
                    if _cr_2 != 'TD':
                        _cr_2 = ''
                    #---
                    translators_all[ar_tra]['all'] += 1
                #---
                secs_texts += f"| {n} || [[{x}]] || [[w:{lang}:{ar}|{ar}]] || {view_u} || {arwords} || {wi_tra} || {_cr_2} || {_time_x}\n"
            #---
            secs_texts += "|}\n"
    #---
    newtext  = '[https://:' + f'{lang}.wikipedia.org {lang}.wikipedia.org] statistics:\n'
    newtext += f'* All links: {all_links:,}\n'
    newtext += f'** With ({lang}) translations: {all_links_with_ar:,}\n'
    newtext += f"*** With translators: {tr_all:,}\n"
    if TD_all > 0:
        newtext += f"*** Articles translated by Translation Dashboard: {TD_all:,}\n"
    newtext += f'* Views: {lang_views:,} (from July 2015 to June 2023)\n'
    newtext += f'* Words: {lang_words:,}\n'
    newtext += '\n'
    #----
    print(newtext)
    print(f'{creator_as_translator=:,}')
    #----
    # authors = sorted(authors.items(), key=lambda x: x[1])
    authors_2 = { x: v for x, v in sorted(authors_2.items(), key=lambda item: item[1], reverse=True)}
    authors_text = "\n==Translators==\n"
    #----
    authors_text += authors_table(authors_2, lang)
    #----
    newtext += authors_text
    newtext += "\n\n"
    newtext += secs_texts
    #---
    return newtext
#---
def work(lang):
    #---
    newtext = make_lang_textso(lang)
    #---
    if 'write' not in sys.argv: return
    #---
    page      = md_MainPage(f'User:Mr. Ibrahem/priorviews/bylang/{lang}', 'www', family='mdwiki')
    exists    = page.exists()
    text        = page.get_text()
    if not exists:
        create = page.Create(text=newtext, summary='update')
    elif text != newtext:
        #---
        save_page   = page.save(newtext=newtext, summary='update', nocreate=1, minor='')
    #---
    #---
#---
if __name__ == "__main__":
    langs = links_by_lang.keys()
    #---
    wrtire = True
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langs = [value]
            wrtire = False
    #---
    lenn = len(langs)
    #---
    n = 0
    #---
    for lang in langs:
        n += 1
        printe.output(f'<<yellow>> {n}/{lenn} langs.py lang: {lang}')
        #---
        work(lang)
    #---
    if wrtire:
        w_all.work_all(translators_all)
    #---