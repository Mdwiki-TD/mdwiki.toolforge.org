#!/usr/bin/python

"""
from wprefs.wpref_text import fix_page
# fix_page(text, title)
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import os
import sys
# ---
from wprefs.bots.Duplicatenew2 import DuplicateReferences
from mdpy.bots import txtlib2
from wprefs.bots.fix_pt_months import pt_months
# ---
from wprefs.helps import print_s
# ---


def add_lang_en(text, lang=''):
    # ---
    print_s('add_lang_en:')
    # ---
    # Match references
    REFS = re.compile(r'(?is)(?P<pap><ref[^>\/]*>)(?P<ref>.*?<\/ref>)')
    # ---
    for Match in REFS.finditer(text):
        pap = Match.group('pap')
        ref = Match.group('ref')
        # ---
        if not ref.strip():
            continue
        # ---
        if re.sub(r'\|\s*language\s*\=\s*\w+', '', ref) != ref:
            continue
        # ---
        ref2 = re.sub(r'(\|\s*language\s*\=\s*)(\|\}\})', r'\g<1>en\g<2>', ref)
        # ---
        if ref2 == ref:
            ref2 = ref.replace('}}</ref>', '|language=en}}</ref>')
        # ---
        if ref2 != ref:
            text = text.replace(pap + ref, pap + ref2)
    # ---
    return text
# ---


def remove_False_code(text):
    # ---
    if 'newcite' not in sys.argv:
        return text
    # ---
    # }}<cite class="citation journal cs1" data-ve-ignore="true" id="CITEREFSmithLopezSilberman2020">Smith, N; Lopez, RA; Silberman, M (January 2020). "Distributive Shock". [[PMID (identifier)|PMID]]&nbsp;[//pubmed.ncbi.nlm.nih.gov/29261964 29261964].</cite><span data-ve-ignore="true"> </span><span class="cs1-hidden-error citation-comment" data-ve-ignore="true"><code class="cs1-code"><nowiki>{{</nowiki>[[Template:cite journal|cite journal]]<nowiki>}}</nowiki></code>: </span><span class="cs1-hidden-error citation-comment" data-ve-ignore="true">Cite journal requires <code class="cs1-code">&#124;journal=</code> ([[Help:CS1 errors#missing_periodical|help]])</span></ref>
    # ---
    # Match references
    REFS = re.compile(r'(?is)(?P<pap><ref[^>\/]*>)(?P<ref>.*?<\/ref>)')
    # ---
    for Match in REFS.finditer(text):
        pap = Match.group('pap')
        ref = Match.group('ref')
        if not ref.strip():
            # pywikibot.output( "\tno ref" )
            continue
        # ---
        # find html code like <cite></cite> and all span code after it
        # find and get html code like <cite></cite>
        if not re.search(r'(?is)<cite[^>]*>', ref):
            # pywikibot.output( "\tno cite" )
            continue
        # ---
        # find and get html code like <cite></cite>
        ref2 = ref
        if ref.find('<span ') != -1:
            ref2 = re.sub(r'(\s*<span[^>]*>.*?<\/span>+?)</ref>', '</ref>', ref2)
        ref2 = re.sub(r'<cite[^>]*>.*?<\/cite>', '', ref2)
        # ---
        if ref2 != ref and ref2.strip() != '</ref>':
            text = text.replace(pap + ref, pap + ref2)
    # ---
    return text
# ---


def move_dots_text(newtext, lang=''):
    # ---
    dot = r'(\.|\,)'
    # ---
    if lang == 'zh':
        dot = '(。)'
    # ---
    regline = r'((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)'
    # ---
    newtext = re.sub(dot + r'\s*' + regline, r'\g<2>\g<1>', newtext)
    # ---
    return newtext
# ---


def Expend_Infobox(text, title, section_0):
    # ---
    newtext = text
    # ---
    if section_0 == '':
        if newtext.find('==') != -1:
            section_0 = newtext.split('==')[0]
        else:
            tagg = f"'''{title}'''1"
            if newtext.find(tagg) != -1:
                section_0 = newtext.split(tagg)[0]
            else:
                section_0 = newtext
                print_s('section_0 = newtext')
    # ---
    title2 = re.escape(title)
    # ---
    newtext = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, "}\n\n\g<1>", newtext)
    section_0 = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, "}\n\n\g<1>", section_0)
    # ---
    tempse_by_u = {}
    tempse = {}
    # ---
    ingr = txtlib2.extract_templates_and_params(section_0)
    u = 0
    for temp in ingr:
        u += 1
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        if len(params) > 4 and section_0.find(f'>{template}') == -1:
            tempse_by_u[u] = temp
            # ---
            tempse[u] = len(template)
            # ---
            print_s(namestrip)
    # ---
    main_temp = {}
    # ---
    if len(tempse_by_u) == 1:
        for x in tempse_by_u:
            main_temp = tempse_by_u[x]
    else:
        PP = [[y1, u1] for u1, y1 in tempse.items()]
        PP.sort(reverse=True)
        # ---
        for y2, u2 in PP:
            print_s(f'len: {y2}, u2: {u2}')
            main_temp = tempse_by_u[u2]
            break
    # ---
    # work in main_temp:
    if main_temp != {}:
        main_temp_text = main_temp.get('item', '')
        # ---
        new_temp = main_temp_text
        # ---
        for param in main_temp['params']:
            # new_temp = re.sub(r'\s*(\|\s*%s\s*\=)' % param, '\n\g<1>', new_temp)
            newparam = f'| {param.ljust(16)}='
            new_temp = re.sub(r'\s*(\|\s*%s\s*\=)' % param, '\n' + newparam, new_temp)
        # ---
        new_temp = re.sub(r'\s*\}\}\s*$', '\n}}', new_temp)
        # ---
        newtext = newtext.replace(main_temp_text, new_temp)
        newtext = newtext.replace(new_temp + "'''", new_temp + "\n'''")
    # ---
    return newtext
# ---


def fix_page(newtext, title, move_dots=False, infobox=False, section_0='', lang='', add_en_lang=False):
    # ---
    print_s(f'fix page: {title}, move_dots:{move_dots}, expend_infobox:{infobox}')
    # ---
    if infobox:
        newtext = Expend_Infobox(newtext, title, section_0)
    # ---
    newtext = remove_False_code(newtext)
    # ---
    newtext = DuplicateReferences(newtext)
    # ---
    if move_dots:
        newtext = move_dots_text(newtext, lang=lang)
    # ---
    if add_en_lang:
        newtext = add_lang_en(newtext, lang=lang)
    # ---
    if lang == 'pt':
        newtext = pt_months(newtext)
    # ---
    return newtext
# ---