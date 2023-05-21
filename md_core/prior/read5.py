'''
write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]

python3.10 ./core8/pwb.py prior/read5 dontsave 2050

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
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior'
#---
project_json      = f'{project}/json'
project_jsonnew   = f'{project}/jsonnew/'
project_jsonnewen = f'{project}/jsonnewen/'
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
def work_test(all, allen):
    # This function takes in two dictionaries as input, 'all' and 'allen'.

    # Loop through each key-value pair in 'allen' dictionary.
    for a, tab in allen.items():
        # If the current key in 'allen' dictionary also exists in 'all' dictionary,
        # then update some specific values with the corresponding values in 'allen' dictionary.
        if a in all:
            all[a]['extlinks'] = tab['extlinks']
            all[a]['refsname'] = tab['refsname']
            all[a]['lead']     = tab['lead']
            all[a]['old']     = tab.get('old', {})

    # Create a file title for the log file
    filetitle = f'{project}/log_test.txt'

    # Call a function 'make_text' with 'all' dictionary as input and store the output in 'text' variable.
    text = text_bot.make_text(all)

    # Remove a specific string from 'text' variable.
    text = text.replace("height:580px;", "")

    # Print the number of links found in 'all' dictionary.
    printe.output(f'{len(all)} links found')

    # Print a message stating where the log file was saved.
    printe.output(f'<<lightyellow>> text loged to {filetitle}')

    # Define a page title and create an object of 'md_MainPage' class with some arguments.
    title = 'User:Mr. Ibrahem/prior/test'
    page  = md_MainPage(title, 'www', family='mdwiki')

    # Get the current text of the page.
    oldtext = page.get_text()

    # Save the updated 'text' to the page with some additional parameters.
    page.save(newtext=text, summary='update', nocreate=0, minor='')

    # Return the updated 'text' variable.
    return text
#---
def get_all_json():
    all   = {}
    allen = {}
    #---
    # get all json file inside dir project_jsonnew
    for filename in os.listdir(project_jsonnew):
        if filename.endswith('.json'):
            filename2 = os.path.join(project_jsonnew, filename)
            #---
            print(f'filename: {filename2}..')
            #---
            data = json.load(open(filename2, 'r'))
            all   = {**all, **data}
    #---
    for filename in os.listdir(project_jsonnewen):
        if filename.endswith('.json'):
            filename2 = os.path.join(project_jsonnewen, filename)
            #---
            print(f'filename: {filename2}..')
            #---
            data = json.load(open(filename2, 'r'))
            #---
            allen = {**allen, **data}
    #---
    for a, tab in allen.items():
        if a in all:
            all[a]['extlinks'] = tab['extlinks']
            all[a]['refsname'] = tab['refsname']
            all[a]['lead']     = tab['lead']
            all[a]['old']      = tab.get('old', {})
    #---
    print(f'new all len:{len(all)}')
    #---
    return all
#---
replaces = {
    "Syncope" : "Syncope (medicine)",
}
#---
class WorkAll:
    def __init__(self):
        self.title = "WikiProjectMed:List/Prior"
        #---
        self.all = get_all_json()
        #---
        self.page = md_MainPage(self.title, 'www', family='mdwiki')
        self.text = self.page.get_text()
        #---
        self.parser = wikitextparser.parse(self.text)
        #---
        print(f'all_wikilinks: {len(self.parser.wikilinks)}')
        #---
        self.sections = self.parser.get_sections(include_subsections=False)
        #---
        self.all_sections = {}

    def get_sectios_links(self):
        for s in self.sections:
            #---
            t = s.title
            c = s.contents
            #---
            if c is None or t is None: continue
            #---
            # parser2 = wikitextparser.parse(c)
            # wikilinks = parser2.wikilinks
            wikilinks = s.wikilinks
            #---
            wikilinks = [str(x.title) for x in wikilinks]
            #---
            wikilinks = [replaces.get(x, x) for x in wikilinks]
            #---
            if len(wikilinks) == 0: continue
            #---
            t = t.replace('/', '-')
            #---
            _all_ = {a: self.all[a] for a in wikilinks if a in self.all}
            #---
            if len(_all_) < 150:
                self.all_sections[t] = _all_
                continue
            #---
            numb = 150
            #---
            if t == 'Other drugs - procedures':
                numb = 103
            #---
            elif len(_all_) < 300:
                numb = 150
            elif len(_all_) > 400:
                numb = 120
            #---
            n = 1
            #---
            for i in range(0, len(_all_), numb):
                #---
                las = dict(list(_all_.items())[i:i+numb])
                #---
                ta = f'{t}_{n}'
                #---
                self.all_sections[ta] = las
                #---
                n += 1
            #---
    def run(self):
        #---
        self.get_sectios_links()
        #---
        for t, _all_ in self.all_sections.items():
            lrnn = len(_all_.keys())
            #---
            print(f'section:({t}), \t\twikilinks: {lrnn}')
            #---
            ttt = f'User:Mr. Ibrahem/prior/{t}'
            #---
            filetitle = f'{project}/log/{t}.txt'
            #---
            text = text_bot.make_text(_all_, ttt=t)
            #---
            if not 'dontsave' in sys.argv:
                codecs.open(filetitle, 'w', encoding='utf-8').write(text)
                #---
                page_x = md_MainPage(ttt, 'www', family='mdwiki')
                #---
                exists    = page_x.exists()
                if not exists: 
                    page_x.Create(text=text, summary='update')
                #---
                else:
                    page_x_text = page_x.get_text()
                    #---
                    page_x.save(newtext=text, summary='update', nocreate=0)
        #---
    #---
#---
def work_all():
    #---
    bot = WorkAll()
    bot.run()
    #---
    page_x  = md_MainPage('User:Mr. Ibrahem/prior', 'www', family='mdwiki')
    #---
    if not 'dontsave' in sys.argv:
        t_sec   = text_bot.get_t_sections()
        #---
        page_x.save(newtext=t_sec, summary='update', nocreate=0)
    #---
    if 'logall' in sys.argv:
        text_bot.log_all_pages_states()
    else:
        printe.output(f'<<lightyellow>> add "logall" to args to log all pages links green/red..')
    #---
#---
if __name__ == '__main__':
    if 'test' in sys.argv:
        work_test()
    else:
        work_all()