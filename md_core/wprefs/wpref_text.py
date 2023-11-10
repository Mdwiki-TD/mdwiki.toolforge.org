#!/usr/bin/python3
"""
from wprefs.wpref_text import fix_page
# fix_page(text, title)
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import sys

# ---
from wprefs.bots.Duplicatenew2 import DuplicateReferences
from wprefs.bots.fix_pt_months import pt_months

# ---
from wprefs.helps import print_s
from wprefs.es import fix_es
from wprefs.infobox import Expend_Infobox


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
    if lang == 'es':
        newtext = fix_es(newtext, title)
    # ---
    return newtext


# ---
