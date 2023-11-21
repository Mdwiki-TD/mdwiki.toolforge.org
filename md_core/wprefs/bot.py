#!/usr/bin/python3
"""

تجميع المراجع في الصفحات

python3 core8/pwb.py wprefs/bot -lang:es ask savetofile
python3 core8/pwb.py wprefs/bot -lang:or ask -page:ପାଟେଲୋଫିମୋରାଲ_ଯନ୍ତ୍ରଣା_ସିଣ୍ଡ୍ରୋମ
python3 core8/pwb.py wprefs/bot -lang:or ask -page:ପୋଷ୍ଟିରିଅର_ୟୁରେଥ୍ରାଲ_ଭଲଭ ask
python3 core8/pwb.py wprefs/bot -lang:or -page:user:Mr._Ibrahem/sandbox ask

python3 core8/pwb.py wprefs/bot -lang:ro ask

python3 core8/pwb.py wprefs/bot ask

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import os
import sys

# ---
# newtext = fix_page(text,title, move_dots= move_dot[1], infobox = False)
# ---
sys.path.append('/data/project/mdwiki/md_core/')
# ---
if 'returnfile' not in sys.argv:
    from mdpy.bots import sql_for_mdwiki
# ---
from wprefs.api import log, GetPageText, missingtitles, page_put
from wprefs.helps import print_s, ec_de_code
from wprefs.files import reffixed_list, setting, append_reffixed_file, save_wprefcash
from wprefs.wpref_text import fix_page

# ---
move_dot = {1: False}
expend_infobox = {1: False}
# ---
project = '/data/project/mdwiki'
# ---
if not os.path.isdir(project):
    project = 'I:/mdwiki'


def fix_page_here(text, title, langcode):
    newtext = text
    # ---
    section_0_text = ''
    # ---
    lang_default = setting.get(langcode, {})
    # ---
    dots = move_dot[1]
    if lang_default.get('move_dots', 0) == 1:
        dots = True
    # ---
    expend = expend_infobox[1]
    if lang_default.get('expend', 0) == 1:
        expend = True
    # ---
    adden = False
    if lang_default.get('add_en_lang', 0) == 1:
        adden = True
    # ---
    newtext = fix_page(newtext, title, move_dots=dots, infobox=expend, section_0=section_0_text, lang=langcode, add_en_lang=adden)
    # ---
    return newtext


def work_one_lang(list_, lang):
    # ---
    print_s(f'<<lightblue>> work on lang: {lang}.wikipedia......................')
    # ---
    newlist = list_
    # ---
    if 'lala' not in sys.argv:
        newlist = [x for x in list_ if f"{lang}:{x}" not in reffixed_list]
        dd = int(len(list_)) - int(len(newlist))
        print("already in reffixed_list :%d" % dd)
    # ---
    if len(newlist) > 0:
        log(lang)
    # ---
    number = 0
    # ---
    dns = []
    # ---
    for title in newlist:
        # ---
        lio = f'{lang}:{title}'
        number += 1
        print_s('<<lightyellow>> %d from %d, page: %s' % (number, len(newlist), lio))
        # ---
        if lio in reffixed_list and 'lala' not in sys.argv:
            print_s('<<lightred>>\talready in reffixed_list.')
            continue
        # ---
        if 'adddone' in sys.argv:
            dns.append(title)
            continue
        # ---
        text = GetPageText(title, lang=lang)
        # ---
        if text == '':
            print_s('\ttext == ""')
            continue
        # ---
        newtext = fix_page_here(text, title, lang)
        # ---
        donee = False
        # ---
        if text != newtext:
            aa = page_put(text, newtext, 'Fix references, Expend infobox mdwiki.toolforge.org.', title, lang)
            # ---
            if aa:
                donee = True
        # ---
        if donee or 'donee' in sys.argv:
            append_reffixed_file(lang, title)
    # ---
    if dns:
        append_reffixed_file(lang, '', dns)


# ---
for arg in sys.argv:
    arg, _, value = arg.partition(':')
    arg = arg[1:] if arg.startswith("-") else arg
    # ---
    if arg == 'infobox':
        expend_infobox[1] = True
    if arg == 'movedots':
        move_dot[1] = True


def maine():
    # ---
    page = ''
    lange = ''
    nolange = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # remove the - from the argument
        arg = arg[1:] if arg.startswith("-") else arg
        # ---
        if arg == 'nolang':
            nolange = value
        if arg == 'lang':
            lange = value
        if arg == 'page':
            page = value.replace("_", " ")
    # ---
    newtable = {}
    # ---
    if page != "" and lange != "":
        newtable[lange] = [page]
    # ---
    if page != "" and lange != "" and 'returnfile' in sys.argv:
        # ---
        title = ec_de_code(page, 'decode')
        log(lange)
        text = GetPageText(title, lang=lange, Print=False)
        # ---
        if text == '':
            print('notext')
            return ''
        # ---
        newtext = fix_page_here(text, title, lange)
        # ---
        if text == newtext:
            print('no changes')
            return ''
        # ---
        if newtext == '':
            print('notext')
            return ''
        # ---
        filee = save_wprefcash(title, newtext)
        print(filee)
        # ---
        return ''
    # ---
    if page == "":
        # ---
        que = 'select lang, target from pages where target != "" and lang != "" and lang != "ar";'
        # ---
        if nolange != '':
            que = que.replace('and lang != ""', f'and lang != "{nolange}"')
        elif lange != '':
            que = f'select lang, target from pages where target != "" and lang = "{lange}";'
        # ---
        print_s(que)
        # ---
        sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
        # ---
        for tab in sq:
            lang = tab['lang']
            target = tab['target']
            # ---
            if lang not in newtable:
                newtable[lang] = []
            if target not in newtable[lang]:
                newtable[lang].append(target)
    # ---
    for lang in newtable:
        work_one_lang(newtable[lang], lang)
    # ---
    if 'returnfile' not in sys.argv:
        print_s(f'find {len(missingtitles)} pages in missingtitles')
        for x, lang in missingtitles.items():
            print_s(f'lang: {lang}, title: {x}')

    # ---


# ---
if __name__ == '__main__':
    maine()
# ---
