"""

python3 pwb.py priorviews/langs -lang:ar ask
python3 core8/pwb.py priorviews/langs -lang:ar ask

"""
import sys
import pywikibot
import json
import os
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
#---
from new_api.mdwiki_page import MainPage as md_MainPage
#---
#---
from priorviews.lists import creators 
# creators.Creators_by_lang_title
# creators.counts_creators_by_lang
#---
#---
def make_lang_textso(lang):
    #---
    authors = {}
    #---
    secs_texts = '==by section=='
    lang_views = 0
    lang_words = 0
    #---
    TD_all = 0
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
        diff = len(links) - len(tab)
        #---
        secs_texts += f'\n==={section}===\n'
        secs_texts += f'* section links: {len(links)}\n'
        secs_texts += f'* with ({lang}) translations: {len(tab)}\n\n'
        #---
        if len(tab) > 0:
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
                ar_tra  = translators.tra_by_lang.get(lang, {}).get(ar.lower(), 0)
                #---
                _creator = creators.Creators_by_lang_title.get(lang, {}).get(ar, {})
                _cr_   = _creator.get("actor", "")
                _time_ = _creator.get("time", "")
                TD     = _creator.get("TD")
                #---
                if TD:
                    TD_all += 1
                    ar_tra = _cr_
                    _cr_   = 'TD'
                #---
                if _cr_ not in ['TD', '']:
                    _cr_ = f"[[w:{lang}:User:{_cr_}|{_cr_}]]"
                #---
                if _time_ != '':
                    # Convert _time_ to a datetime object
                    datetime_obj = datetime.datetime.strptime(str(_time_), '%Y%m%d%H%M%S')
                    # Format the datetime object as "YYYY-MM-DD"
                    formatted_date = datetime_obj.strftime('%Y-%m-%d')
                    # Assign the formatted date to _time_
                    _time_ = formatted_date
                #---
                if ar_tra != '':
                    ar_tra = f"[[w:{lang}:User:{ar_tra}|{ar_tra}]]"
                    #---
                    if not ar_tra in authors: authors[ar_tra] = 0
                    #---
                    authors[ar_tra] += 1
                #---
                secs_texts += f"| {n} || [[{x}]] || [[w:{lang}:{ar}|{ar}]] || {view_u} || {arwords} || {ar_tra} || {_cr_} || {_time_}\n"
            #---
            secs_texts += "|}\n"
    #---
    newtext  = '[https://:' + f'{lang}.wikipedia.org {lang}.wikipedia.org] statistics:\n'
    newtext += f'* All links: {all_links:,}\n'
    newtext += f'* With ({lang}) translations: {all_links_with_ar:,}\n\n'
    newtext += f'* Views: {lang_views:,} (from July 2015 to June 2023)\n'
    newtext += f'* Words: {lang_words:,}\n'
    newtext += f"* articles translated by Translation Dashboard: {TD_all}"
    newtext += f'\n'
    #----
    # authors = sorted(authors.items(), key=lambda x: x[1])
    authors = { x: v for x, v in sorted(authors.items(), key=lambda item: item[1], reverse=True)}
    authors_text = "\n==Translators==\n* "
    authors_text += "\n*".join( [ f"{x}: {v}" for x, v in authors.items()])
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
    page      = md_MainPage(f'User:Mr. Ibrahem/priorviews/bylang/{lang}', 'www', family='mdwiki')
    exists    = page.exists()
    if not exists:
        create = page.Create(text=newtext, summary='update')
    else:
        #---
        text        = page.get_text()
        save_page   = page.save(newtext=newtext, summary='update', nocreate=1, minor='')
    #---
#---
if __name__ == "__main__":
    langs = links_by_lang.keys()
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langs = [value]
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