'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]
'''
import sys
from collections import namedtuple
import os
import re
import pywikibot
import json
import urllib.parse
import requests
import wikitextparser
import codecs
from mdpy import mdwiki_api
from mdpy import printe
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior/json/'
#---
def main_links():
    title = "WikiProjectMed:List/Prior"
    text  = mdwiki_api.GetPageText(title)
    links = mdwiki_api.Get_page_links(title, namespace="*", limit="max")
    # print(links)
    #---
    links = [ x['title'] for s, x in links['links'].items() if x['ns'] == 0 ]
    #---
    # log all links to file
    # codecs.open(project + 'links.json', 'w', encoding='utf-8').write(json.dumps(links))
    #---
    pywikibot.output(f'{len(links)} links found')
    #---
    return links
#---
from new_api.wiki_page import MainPage, change_codes
#---
# if not os.path.exists(project + 'allen2.json'): codecs.open(project + 'allen2.json', 'w', encoding='utf-8').write(json.dumps({}))
#---
# all = json.loads(codecs.open(project + 'allen2.json', 'r', encoding='utf-8').read())
all = {}
#---
from prior import get_them
#---
def work_in_en_page(title):
    #---
    if not title in all : 
        all[title] = {'extlinks':[], 'langs':{}, 'refsname':[]}
    #---
    all[title]['en'] = title
    #---
    page = MainPage(title, 'en')
    #---
    title2 = title
    #---
    if page.isRedirect() :
        target = page.get_redirect_target()
        if target != '':
            page = MainPage(target, 'en')
            all[title]['en'] = target
            title2 = target
    #---
    langlinks = page.get_langlinks()
    #---
    pywikibot.output(f"langlinks: {len(langlinks)}")
    #---
    tat = get_them.work_in_one_lang_link('en', title2)
    #---
    text = tat.text
    extlinks = tat.extlinks
    refsname = tat.refsnames
    #---
    all[title]['extlinks'] = extlinks
    all[title]['refsname'] = refsname
    #---
    pywikibot.output(f'p0/{len(langlinks)}:\ten\t\t{len(extlinks)} extlinks, {len(refsname)} refsname')
    #---
    n = 0
    #---
    # if 'test' in sys.argv: print(xss)
    #---
    for lang, tit in langlinks.items():
        #---
        n += 1
        #---
        lang = change_codes.get(lang) or lang
        #---
        if lang == 'simple' : continue
        #---
        tata = {'title':tit, 'extlinks':[], 'refsname':[]}
        #---
        tatnn = get_them.work_in_one_lang_link(lang, tit)
        #---
        text1     = tatnn.text
        extlinks1 = tatnn.extlinks
        refsname1 = tatnn.refsnames
        #---
        tata['extlinks'] = extlinks1
        tata['refsname'] = refsname1
        #---
        pywikibot.output(f'p{n}/{len(langlinks)}:\t{lang}\t\t{len(tata["extlinks"])} extlinks, {len(tata["refsname"])} refsname')
        #---
        all[title]['langs'][lang] = tata
        #---
    #---
#---
def startn():
    #---
    if 'test' in sys.argv:  
        # links = ["Angular cheilitis", "Bad breath", "Leukoplakia", "Periodontal disease", "Tonsil stones", "Tooth decay"]
        links = ["Bronchiectasis"]
    else:
        links = main_links()
    # start work in all links
    #---
    links.sort()
    #---
    main_File = project + 'allennew_2.json'
    #---
    if len(links) > 300:
        links_Tab = {}
        #---
        # split links to 4 lists
        len2 = len(links)//4
        links_Tab[1] = links[:len2]
        links_Tab[2] = links[len2:len2*2]
        links_Tab[3] = links[len2*2:len2*3]
        links_Tab[4] = links[len2*3:]
        #---
        # for x in links_Tab: print(len(links_Tab[x]))
        #---
        if 's1' in sys.argv:    main_File, links = project + 'new_1.json', links_Tab[1]
        if 's2' in sys.argv:    main_File, links = project + 'new_2.json', links_Tab[2]
        if 's3' in sys.argv:    main_File, links = project + 'new_3.json', links_Tab[3]
        if 's4' in sys.argv:    main_File, links = project + 'new_4.json', links_Tab[4]
    #---
    # if 
    n = 0
    for x in links:
        n += 1
        pap = f'p {n}/{len(links)}: {x}'
        pywikibot.output(pap)
        work_in_en_page(x)
        # log every 30 pages
        if n % 30 == 0:
            codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(all))
    #---
    codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(all))
#---
if __name__ == '__main__':
    startn()