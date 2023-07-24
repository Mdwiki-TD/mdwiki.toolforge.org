"""

python3 pwb.py priorviews/langs -lang:ar ask
python3 core8/pwb.py priorviews/langs -lang:ar ask

"""
from new_api.mdwiki_page import MainPage as md_MainPage
import sys
import json
import os
import re
import datetime
import codecs
# ---
Dir = os.path.dirname(os.path.abspath(__file__))
# ---


def work_all_old(translators_all):

    # sort translators_all by count
    translators_a = {x: v for x, v in sorted(translators_all.items(), key=lambda item: item[1]['all'], reverse=True)}
    # ---
    alllll = 0
    # ---
    text = ''
    for x, v in translators_a.items():
        # ---
        # skip user match ip address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', x):
            continue
        # skip user match ip address like: 2001:569:F867:EE00:1540:D99D:3F7:3EAE
        if re.match(r'^(?:(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}|::(?:[A-Fa-f0-9]{1,4}:){0,5}[A-Fa-f0-9]{1,4}|(?:[A-Fa-f0-9]{1,4}:){1,2}:|:(?::[A-Fa-f0-9]{1,4}){1,6}|(?:[A-Fa-f0-9]{1,4}:){1,6}:|:(?::[A-Fa-f0-9]{1,4}){1,7}|(?:[A-Fa-f0-9]{1,4}:){1,7}:|:(?::[A-Fa-f0-9]{1,4}){1,8}|(?:[A-Fa-f0-9]{1,4}:){1,8}:)$', x):
            continue
        # ---
        text += f"\n* [[w:en:User:{x}|{x}]]: {v['all']}\n**"
        bylang = v['by_lang']
        # sort by lang
        bylang = {o: v for o, v in sorted(bylang.items(), key=lambda item: item[1], reverse=True)}
        text += ", ".join([f"[[w:{langg}:User:{x}|{langg}]]: {v}" for langg, v in bylang.items()])
        # ---
        alllll += v['all']
        # ---
    # ---
    t = f"* all translations in the report: {alllll}\n"
    # ---
    text = t + text
    # ---
    page = md_MainPage('User:Mr. Ibrahem/priorviews/translators', 'www', family='mdwiki')
    exists = page.exists()
    oldtext = page.get_text()
    if not exists:
        page.Create(text=text, summary='update')
    elif oldtext != text:
        # ---
        page.save(newtext=text, summary='update', nocreate=1, minor='')
# ---


def make_by_lang(one_langs_only):
    tab2 = {}
    # ---
    for user, tab in one_langs_only.items():
        for lang, cunts in tab['by_lang'].items():
            if not lang in tab2:
                tab2[lang] = {}
            #---
            # tab2[lang][user] = cunts
            #---
            if not cunts in tab2[lang]:
                tab2[lang][cunts] = []
            tab2[lang][cunts].append(user)
    # ---
    return tab2

def sect_text(lang, users):
    # ---
    sc2 = '{| class=wikitable sortable\n|-\n!count!!users\n|-\n'
    # ---
    lang_cunt = 0
    # ---
    one = []
    # ---
    for cunts, users in users.items():
        # ---
        for u in users: 
            lang_cunt += cunts
        # ---
        usrs_line = ', '.join([f'[[w:{lang}:User talk:{x}|{x}]]' for x in users])
        # ---
        sc2 += f'\n! {cunts} \n| {usrs_line}\n|-'
        # ---
    # ---
    sc2 += '\n|}'
    seec = f'\n==={lang} ({lang_cunt})===\n{sc2}'
    # ---
    return seec

def work_all(translators_all):

    alllll = 0
    # ---
    # sort translators_all by count
    translators_a = {x: v for x, v in sorted(translators_all.items(), key=lambda item: item[1]['all'], reverse=True)}
    # ---
    for x in translators_a.copy():
        # ---
        # skip user match ip address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', x):
            del translators_a[x]
            continue
        # skip user match ip address like: 2001:569:F867:EE00:1540:D99D:3F7:3EAE
        if re.match(r'^(?:(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}|::(?:[A-Fa-f0-9]{1,4}:){0,5}[A-Fa-f0-9]{1,4}|(?:[A-Fa-f0-9]{1,4}:){1,2}:|:(?::[A-Fa-f0-9]{1,4}){1,6}|(?:[A-Fa-f0-9]{1,4}:){1,6}:|:(?::[A-Fa-f0-9]{1,4}){1,7}|(?:[A-Fa-f0-9]{1,4}:){1,7}:|:(?::[A-Fa-f0-9]{1,4}){1,8}|(?:[A-Fa-f0-9]{1,4}:){1,8}:)$', x):
            del translators_a[x]
            continue
        #---
        alllll += translators_a[x]['all']
    # ---
    one_langs_only = {x: v for x, v in translators_a.items() if len(v['by_lang']) == 1}
    multiple_langs = {x: v for x, v in translators_a.items() if len(v['by_lang']) > 1}
    # ---
    langs_a = make_by_lang(one_langs_only)
    # ---
    text = f"* all translations in the report: {alllll}\n==multi langs==\n"
    # ---
    for x, v in multiple_langs.items():
        # ---
        text += f"\n* [[w:en:User talk:{x}|{x}]]: {v['all']}\n**"
        bylang = v['by_lang']
        # sort by lang
        bylang = {o: v for o, v in sorted(bylang.items(), key=lambda item: item[1], reverse=True)}
        text += ", ".join([f"[[w:{langg}:User talk:{x}|{langg}]]: {v}" for langg, v in bylang.items()])
        # ---
    # ---
    seec = '\n\n==by lang==\n\n'
    # ---
    for lang, users in langs_a.items():
        # ---
        seec += sect_text(lang, users)
        # ---
    # ---
    text += seec
    # ---
    page = md_MainPage('User:Mr. Ibrahem/priorviews/translators', 'www', family='mdwiki')
    exists = page.exists()
    oldtext = page.get_text()
    if not exists:
        page.Create(text=text, summary='update')
    elif oldtext != text:
        # ---
        page.save(newtext=text, summary='update', nocreate=1, minor='')
# ---
