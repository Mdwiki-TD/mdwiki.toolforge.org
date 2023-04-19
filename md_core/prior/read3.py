'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]
'''
import sys
import os
import re
import json
import urllib.parse
import pywikibot
import wikitextparser
import codecs
#---
from mdpy import printe
from prior import text_bot
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior'
#---
project_json = f'{project}/md_core/prior/json/'
#---
from new_api.mdwiki_page import MainPage as md_MainPage
'''
page      = md_MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
#---
text        = page.get_text()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
'''
#---
def work_test(all=''):
    #---
    if all == '':
        all = json.loads(codecs.open(project_json + '/test.json', 'r', encoding='utf-8').read())
    #---
    filetitle = f'{project}/log_test.txt'
    #---
    text = text_bot.make_text(all)
    #---
    text = text.replace("height:580px;", "")
    #---
    codecs.open(filetitle, 'w', encoding='utf-8').write(text)
    #---
    pywikibot.output(f'{len(all)} links found')
    #---
    pywikibot.output(f'<<lightyellow>> text loged to {filetitle}')
    #---
    title = 'User:Mr. Ibrahem/prior/test'
    #---
    page      = md_MainPage(title, 'www', family='mdwiki')
    #---
    page.save(newtext=text, summary='update', nocreate=0, minor='')
    #---
    return text
#---
def work_all():
    #---
    #if os.path.exists(project_json + '/new_1.json'):
    all1 = json.loads(codecs.open(project_json + '/new_1.json', 'r', encoding='utf-8').read())
    all2 = json.loads(codecs.open(project_json + '/new_2.json', 'r', encoding='utf-8').read())
    all3 = json.loads(codecs.open(project_json + '/new_3.json', 'r', encoding='utf-8').read())
    all4 = json.loads(codecs.open(project_json + '/new_4.json', 'r', encoding='utf-8').read())
    #---
    all = {**all1, **all2, **all3, **all4}
    #---
    print(f'new all len:{len(all)}')
    #---
    title = "WikiProjectMed:List/Prior"
    #---
    page      = md_MainPage(title, 'www', family='mdwiki')
    #---
    text        = page.get_text()
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
        text += text_bot.make_text(_all_)
        #---
        filetitle = f'{project}/log/{t}.txt'
        #---
        codecs.open(filetitle, 'w', encoding='utf-8').write(text)
        #---
        ttt = f'User:Mr. Ibrahem/prior/{t}'
        #---
        mmm_links.append(ttt)
        #---
        page_x      = md_MainPage(ttt, 'www', family='mdwiki')
        page_x.save(newtext=text, summary='update', nocreate=0)
        # break
    #---
    # n_text = "\n".join([ f'* [[{x}]]' for x in mmm_links])
    #---
#---
if __name__ == '__main__':
    if 'test' in sys.argv:
        work_test()
    else:
        work_all()