'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]

python3 ./core/pwb.py prior/p3 s1
python3 ./core/pwb.py prior/p3 s2
python3 ./core/pwb.py prior/p3 s3
python3 ./core/pwb.py prior/p3 s4

python3 ./core/pwb.py prior/p3 test
'''
import sys
from collections import namedtuple
import os
import re
import pywikibot
import json
import urllib.parse
import wikitextparser
import codecs
#---
from mdpy import printe
#---
from new_api.mdwiki_page import MainPage as md_MainPage
'''
page      = md_MainPage(title, 'www', family='mdwiki')
text        = page.get_text()
'''
#---
from new_api.wiki_page import MainPage, change_codes
#---
from prior import get_them
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project_json = f'{project}/md_core/prior/json/'
#---
def main_links():
    title = "WikiProjectMed:List/Prior"
    #---
    page    = md_MainPage(title, 'www', family='mdwiki')
    text    = page.get_text()
    #---
    links   = page.page_links()
    #---
    links = [ x['title'] for x in links if x['ns'] == 0 ]
    #---
    # log all links to file
    # codecs.open(project_json + 'links.json', 'w', encoding='utf-8').write(json.dumps(links))
    #---
    pywikibot.output(f'{len(links)} links found')
    #---
    return links
#---
all = {}
#---
def work_in_en_page(title):
    #---
    if not title in all:
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
    lenex = str(len(extlinks)).ljust(4)
    lenre = str(len(refsname)).ljust(4)
    #---
    pywikibot.output(f'p0/{len(langlinks)}:\ten\t\t{lenex} extlinks, {lenre} refsname')
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
        #---
        lenex = str(len(tata["extlinks"])).ljust(4)
        lenre = str(len(tata["refsname"])).ljust(4)
        #---
        pywikibot.output(f'\tp{n}/{len(langlinks)}:\t{lang.ljust(20)}\t{lenex} extlinks, {lenre} refsname..')
        #---
        all[title]['langs'][lang] = tata
        #---
    #---
#---
def work_in_links(links, main_File):
    #---
    n = 0
    #---
    for x in links:
        n += 1
        #---
        pap = f'p {n}/{len(links)}: {x}'
        #---
        pywikibot.output(pap)
        #---
        work_in_en_page(x)
        #---
        # log every 30 pages
        if n % 30 == 0:
            codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(all))
    #---
#---
def start_test():
    #---
    links = ["Cardiac arrest", "Angular cheilitis", "Bad breath", "Leukoplakia", "Periodontal disease", "Tonsil stones", "Tooth decay"]
    # start work in all links
    #---
    links.sort()
    #---
    main_File = project_json + 'test.json'
    #---
    # python3 ./core/pwb.py prior/p3 test
    #---
    work_in_links(links, main_File)
    #---
    codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(all))
    #---
    return all
#---
def start_all():
    #---
    links = main_links()
    # start work in all links
    #---
    links.sort()
    #---
    main_File = project_json + 'allennew_2.json'
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
        if   's1' in sys.argv:    main_File, links = project_json + 'new_1.json', links_Tab[1]
        elif 's2' in sys.argv:    main_File, links = project_json + 'new_2.json', links_Tab[2]
        elif 's3' in sys.argv:    main_File, links = project_json + 'new_3.json', links_Tab[3]
        elif 's4' in sys.argv:    main_File, links = project_json + 'new_4.json', links_Tab[4]
        else :                    main_File, links = project_json + 'new_1.json', links
    #---
    work_in_links(links, main_File)
    #---
    codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(all))
#---
if __name__ == '__main__':
    if 'test' in sys.argv:
        start_test()
    else:
        start_all()