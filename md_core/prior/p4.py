'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]

python3 ./core/pwb.py prior/p4 test
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
project_jsonnew = f'{project}/md_core/prior/jsonnew/'
#---
def main_links():
    title = "WikiProjectMed:List/Prior"
    #---
    page    = md_MainPage(title, 'www', family='mdwiki')
    text    = page.get_text()
    #---
    links   = page.page_links()
    #---
    replaces = {
        "Syncope" : "Syncope (medicine)",
    }
    #---
    links = [ replaces.get(x['title'], x['title']) for x in links if x['ns'] == 0 ]
    #---
    pywikibot.output(f'{len(links)} links found')
    #---
    return links
#---
all = {}
allen = {}
#---
def log_all(main_File):
    #---
    if 'enonly' in sys.argv: return
    #---
    codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(all))
#---
def log_allen(main_File):
    codecs.open(main_File, 'w', encoding='utf-8').write(json.dumps(allen))
#---
def advance_work_en(title, title2, page):
    #---
    tat = get_them.work_in_one_lang_link('en', title2)
    #---
    text = tat.text
    #---
    allen[title]['lead'] = {}
    allen[title]['lead']['extlinks'] = tat.lead['extlinks']
    allen[title]['lead']['refsname'] = tat.lead['refsname']
    #---
    extlinks = tat.extlinks
    refsname = tat.refsname
    #---
    allen[title]['extlinks'] = extlinks
    allen[title]['refsname'] = refsname
    #---
    lenex = str(len(extlinks)).ljust(4)
    lenre = str(len(refsname)).ljust(4)
    #---
    lenex_lead = str(len(tat.lead['extlinks'])).ljust(4)
    lenre_lead = str(len(tat.lead['refsname'])).ljust(4)
    #---
    pywikibot.output(f'p0/\ten\t\t{lenex} extlinks, {lenre} refsname')
    pywikibot.output(f'p0/\ten\t\t{lenex_lead} lead_extlinks, {lenre_lead} lead_refsname')
    #---
#---
def work_in_en_page(title):
    #---
    if not title in all:
        all[title] = {'langs':{}}
    #---
    if not title in allen:
        allen[title] = {
            'extlinks':[],
            'refsname':[],
            'en':title,
            'lead' : {'extlinks':[], 'refsname':[]}
            }
    #---
    page = MainPage(title, 'en')
    #---
    title2 = title
    #---
    if page.isRedirect() :
        target = page.get_redirect_target()
        if target != '':
            page = MainPage(target, 'en')
            allen[title]['en'] = target
            title2 = target
    #---
    langlinks = page.get_langlinks()
    #---
    pywikibot.output(f"langlinks: {len(langlinks)}")
    #---
    advance_work_en(title, title2, page)
    #---
    pywikibot.output(f'p0 langlinks: {len(langlinks)}')
    #---
    if 'enonly' in sys.argv:
        return
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
        refsname1 = tatnn.refsname
        #---
        tata['extlinks'] = extlinks1
        tata['refsname'] = refsname1
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
def work_in_links(links, main_File, main_File_en, Log=True):
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
        if Log and n % 30 == 0:
            log_all(main_File)
    #---
    if Log:
        log_allen(main_File_en)
#---
def start_test(links=[]):
    #---
    if links == []:
        links = ["Syncope (medicine)"]
    # start work in all links
    #---
    # links.sort()
    #---
    main_File    = project_json + 'test.json'
    main_File_en = project_json + 'en_test.json'
    #---
    # python3 ./core/pwb.py prior/p4 test
    #---
    work_in_links(links, main_File, main_File_en, Log=False)
    #---
    # log_all(main_File)
    # log_allen(main_File_en)
    #---
    return all, allen
#---
def start_all():
    #---
    links = main_links()
    # start work in all links
    #---
    links.sort()
    #---
    main_File = project_json + 'allennew_2.json'
    main_File_en = project_json + 'en_allennew_2.json'
    #---
    if len(links) > 300:
        links_Tab = {}
        #---
        # split links to 10 lists
        sub_list_len = len(links) // 10 # طول كل قائمة فرعية
        sub_lists = [links[i:i+sub_list_len] for i in range(0, len(links), sub_list_len)] # تقسيم القائمة الأساسية إلى قوائم فرعية
        #---
        for i in range(len(sub_lists)):
            links_Tab[str(i+1)] = sub_lists[i]
            print(f'jsub -N s{i+1} python3 ./core/pwb.py prior/p4 -s:{i+1}')
        #---
        valu = ''
        #---
        for arg in sys.argv:
            arg, sep, value = arg.partition(':')
            if arg == '-s' and value != '':
                valu = value
                break
        #---
        if valu in links_Tab:
            links = links_Tab[valu]
            main_File    = project_jsonnew + f'{valu}.json'
            main_File_en = project_jsonnew + f'en_{valu}.json'
            print(f'list number:{valu} len of it: {len(links)}')
        else:
            print(f'list number:{valu} not found')
            sys.exit()
    #---
    work_in_links(links, main_File, main_File_en)
    #---
    log_all(main_File)
    log_allen(main_File_en)
#---
if __name__ == '__main__':
    if 'test' in sys.argv:
        start_test()
    else:
        start_all()