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
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project_json = f'{project}/md_core/prior/json/'
project_jsonnew = f'{project}/md_core/prior/jsonnew/'
project_jsonnewen = f'{project}/md_core/prior/jsonnewen/'
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
    printe.output(f'{len(links)} links found')
    #---
    return links
#---
all = {}
allen = {}
#---
def log_all(main_File):
    #---
    if 'enonly' in sys.argv or 'newenonly' in sys.argv: return
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
    allen[title]['lead'] = tat.lead
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
    printe.output(f'p0/\ten\t\t{lenex} extlinks, {lenre} refsname')
    printe.output(f'p0/\ten\t\t{lenex_lead} lead_extlinks, {lenre_lead} lead_refsname')
    #---
    old = get_them.get_old(title)
    allen[title]['old'] = {}
    allen[title]['old']['extlinks'] = old.extlinks
    allen[title]['old']['refsname'] = old.refsname
    allen[title]['old']['lead'] = old.lead
    #---
    lenex1 = str(len(old.extlinks)).ljust(4)
    lenre1 = str(len(old.refsname)).ljust(4)
    #---
    lenex_lead1 = str(len(old.lead['extlinks'])).ljust(4)
    lenre_lead1 = str(len(old.lead['refsname'])).ljust(4)
    #---
    printe.output(f'p0/\told\t\t{lenex1} extlinks, {lenre1} refsname')
    printe.output(f'p0/\told\t\t{lenex_lead1} lead_extlinks, {lenre_lead1} lead_refsname')
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
    printe.output(f"<<blue>> en:{title}, \n\tlanglinks: {len(langlinks)}")
    #---
    advance_work_en(title, title2, page)
    #---
    if 'enonly' in sys.argv or 'newenonly' in sys.argv:
        return
    #---
    n = 0
    #---
    # if 'test' in sys.argv: printe.output(xss)
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
        printe.output(f'\tp{n}/{len(langlinks)}:\t{lang.ljust(20)}\t{lenex} extlinks, {lenre} refsname..')
        #---
        all[title]['langs'][lang] = tata
        #---
    #---
#---
n_al = 0
#---
def work_in_links(links, main_File, main_File_en, Log=True):
    #---
    global n_al
    global allen, all
    #---
    n = 0
    #---
    en_in = {}
    #---
    basefilename = os.path.basename(main_File_en)
    #---
    if os.path.exists(main_File_en):
        en_in = json.load(open(main_File_en, encoding='utf-8'))
        allen = en_in
        printe.output(f'<<green>> There are {len(en_in)} en title in file: {basefilename}, from {len(links)} links...')
    #---
    if os.path.exists(main_File):
        all = json.load(open(main_File, encoding='utf-8'))
    #---
    for x in links:
        n_al += 1
        n += 1
        #---
        pap = f'p {n}/{len(links)}: {x}'
        #---
        printe.output(pap)
        #---
        if 'newenonly' in sys.argv:
            if x in en_in and en_in[x] != {}:
                #---
                ext = en_in[x].get('extlinks', [])
                ref = en_in[x].get('refsname', [])
                lead_ex = en_in[x].get('lead', {}).get('extlinks', [])
                lead_re = en_in[x].get('lead', {}).get('refsname', [])
                #---
                if len(ext) > 0 and len(ref) > 0 and len(lead_ex) > 0 and len(lead_re) > 0:
                    #---
                    printe.output(f'<<lightyellow>> en {x} already in {basefilename}, skip..........')
                    continue
        #---
        work_in_en_page(x)
        #---
        # log every 30 pages
        if Log and n_al % 30 == 0:
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
    tanko = {}
    #---
    n = 0
    #---
    for i in range(0, len(links), 100):
        n += 1
        #---
        titles = links[i:i+100]
        #---
        main_File    = project_jsonnew + f'{n}.json'
        main_File_en = project_jsonnewen + f'en_{n}.json'
        #---
        tanko[str(n)] = {'file':main_File, 'file_en':main_File_en, 'links':titles}
        #---
        printe.output(f'jsub -N s{n} python3 ./core/pwb.py prior/p4 -s:{n}')
        #---
    #---
    valu = ''
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        if arg == '-s' and value != '':
            valu = value
            break
    #---
    if valu in tanko:
        printe.output(f'list number:{valu} found')
        #---
        tanko = { valu: tanko[valu] }
    else:
        printe.output(f'list number:{valu} not found.')
        #---
        if not 'all' in sys.argv:
            printe.output(f'Add "all" to sys.argv to work in all.. \n sys.exit()')
            sys.exit()
    #---
    for x, tab in tanko.items():
        valu = x
        links = tab['links']
        main_File    = tab['file']
        main_File_en = tab['file_en']
        #---
        printe.output(f'list number:{valu} len of it: {len(links)}')
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