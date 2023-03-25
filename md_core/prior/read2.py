'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]
'''
import sys
from collections import namedtuple
import os
import re
import json
import urllib.parse
import requests
import pywikibot
import wikitextparser
import codecs
#---
from mdpy import printe
from mdpy import mdwiki_api
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior'
#---
all = json.loads(codecs.open(project + '/allennew.json', 'r', encoding='utf-8').read())
#--
# _all_ = { "Abacavir": { "refs": 23, "langs": { "ar": { "title": "title", "refs": 5, "same": 4 } } } }
#---
# make list of all lang in langs
all_langs = []
if True:
    for en, ta in all.items():  all_langs.extend(ta['langs'].keys())
    #---
    all_langs = list(set(all_langs))
    all_langs.sort()
#---
def match_p(refs, same):
    if same < 1: return False
    if 11 > same < ((refs/2)-1): return False
    #---
    return True
#---
text_main = '''
<div style="height:580px;width:100%;overflow-x:auto; overflow-y:auto">

{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! n
! style="position: sticky;top: 0;left: 0;" | en
!refs
!'''
#---
def make_text(allo):
    # create wikitable from json
    #---
    all_langs1 = []
    #---
    for en, ta in allo.items():  all_langs1.extend(ta['langs'].keys())
    #---
    all_langs1 = list(set(all_langs1))
    all_langs1.sort()
    #---
    all_langs1 = [ x.strip() for x in all_langs1 if x.strip() != '']
    #---
    all_langs_2 = {}
    #---
    for en, ta in allo.items():
        for la in ta['langs']:
            la = la.strip()
            if la in ['en', '']: continue
            if not la in all_langs_2: all_langs_2[la] = 0
            all_langs_2[la] += 1
    #---
    # sort all_langs_2 by number of references
    all_langs_2 = sorted(all_langs_2.items(), key=lambda x: x[1], reverse=True)
    #---
    # print(all_langs_2)
    #---
    text = text_main
    #---
    # text += " !! ".join(all_langs1)
    text += " !! ".join([x for x, ta in all_langs_2])
    #---
    n = 0
    #---
    for en, ta in allo.items():
        refs  = ta['refs']
        en    = ta.get('en', en)
        langs = ta['langs']
        #---
        if len(langs) == 0 :
            pywikibot.output(f'{en}: no langs.....')
        #---
        n += 1
        #---
        # print(f'a {n}/{len(allo)}:')
        #---
        if n > 100 and 'limit100' in sys.argv: break
        #---
        l_text = f'''
|-
! {n}
! style="position: sticky;left: 0;" | [[:en:{en}|{en}]]
! {refs}
'''
        #---
        # for l in all_langs1:
        for l, ta in all_langs_2:
            #---
            tit   = langs.get(l, {}).get('title', '')
            same  = langs.get(l, {}).get('same', 0)
            p_ref = langs.get(l, {}).get('refs', 0)        
            #---
            tito = '|'
            #---
            if l in langs:
                tito = f'[[:{l}:{tit}|{same}]]'
                #---
                color = '#fcc0c0'   # red
                #---
                if match_p(refs, same):
                    color = '#c0fcc0'   # green
                #---   
                tito = f'| style="background-color:{color} | {tito}'
            #---
            # make background color
            # if 
            l_text += f'\n{tito}'
        #---
        text += l_text
        #---
    text += '\n|}\n</div>'
    #---
    return text
#---
# mdwiki_api.post(params)
# mdwiki_api.wordcount(title, srlimit='30')
# mdwiki_api.purge(title)
# mdwiki_api.page_put(NewText, summary, title, time_sleep="", minor="")
# mdwiki_api.page_putWithAsk(oldtext, NewText, summary, title, Ask, minor="")
# mdwiki_api.create_Page(text, summary, title, ask, sleep=0, duplicate4="")
# mdwiki_api.Add_To_Bottom(appendtext, summary, title, ask)
# mdwiki_api.Add_To_Head(prependtext, summary, title, Ask)
# mdwiki_api.move(From, to, reason)
# mdwiki_api.Get_Newpages(limit="max", namespace="0", rcstart="")
# mdwiki_api.Get_UserContribs(user, limit="max", namespace="*", ucshow="")
# mdwiki_api.GetPageText(title)
# mdwiki_api.Get_All_pages(start, limit="max", namespace="*", apfilterredir='')
# mdwiki_api.Search(title, ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# mdwiki_api.import_page(title)
# mdwiki_api.Get_page_links(title, namespace="*", limit="max")
# mdwiki_api.subcatquery(title, depth=0, ns="all", without_lang="", with_lang="", tempyes=[], limit=0)
# mdwiki_api.get_redirect(liste)
# write text to file
if 'all' in sys.argv:
    filetitle = f'{project}/log/en.txt'
    #---
    if 'limit100' in sys.argv:  filetitle = f'{project}/en_limit100.txt'
    #---
    text = make_text(all)
    #---
    codecs.open(filetitle, 'w', encoding='utf-8').write(text)
    #---
else:
    title = "WikiProjectMed:List/Prior"
    text  = mdwiki_api.GetPageText(title)
    #---
    # get text sections use wikitextparser
    #---
    parser = wikitextparser.parse(text)
    sections = parser.get_sections(include_subsections=False)
    # print(sections)
    #---
    all_wikilinks = parser.wikilinks
    print(f'all_wikilinks: {len(all_wikilinks)}')
    #---
    Done = []
    #---
    mmm_links = []
    #---
    for s in sections:
        #---
        t = s.title
        c = s.contents
        #---
        if c == None or t == None: continue
        #---
        # parser2 = wikitextparser.parse(c)
        # wikilinks = parser2.wikilinks
        wikilinks = s.wikilinks
        #---
        wikilinks = [str(x.title) for x in wikilinks]
        #---
        if len(wikilinks) == 0 : continue
        #---
        t = t.replace('/', '-')
        # print(t)
        # print(len(c))
        #---
        # print(wikilinks)
        #---
        _all_ = { a : all[a] for a in wikilinks if a in all and not a in Done }
        #---
        lrnn = len(_all_.keys())
        #---
        print(f'section:({t}), \t\twikilinks: {lrnn}')
        #---
        Done.extend(_all_.keys())
        #---
        text = f'''=={t} ({lrnn})==\n'''
        #---
        text += make_text(_all_)
        #---
        filetitle = f'{project}/log/{t}.txt'
        #---
        codecs.open(filetitle, 'w', encoding='utf-8').write(text)
        #---
        ttt = f'User:Mr. Ibrahem/prior/{t}'
        mmm_links.append(ttt)
        mdwiki_api.page_put(text, 'update', ttt)
        # break
    # get text sections use wikitextparser
    #---
    n_text = "\n".join([ f'* [[{x}]]' for x in mmm_links])
    #---
    mdwiki_api.page_put(n_text, 'create', 'User:Mr. Ibrahem/prior')
    