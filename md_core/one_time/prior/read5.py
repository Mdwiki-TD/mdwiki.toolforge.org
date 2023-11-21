'''
write code to read page in en.wikipedia.org using API, then create list with All links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]

python3 core8/pwb.py prior/read5 dontsave
python3 core8/pwb.py prior/read5 logall split
python3 core8/pwb.py prior/read5 dontsave logall

'''
import sys
import os
import json
import wikitextparser
import codecs

# ---
from new_api.mdwiki_page import MainPage as md_MainPage
from mdpy import printe
from prior import text_bot

# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
project += '/md_core/prior'
# ---
project_json = f'{project}/json'
project_js_new = f'{project}/json_langs/'
project_js_newen = f'{project}/json_en/'
# ---
'''
page      = md_MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
# ---
text        = page.get_text()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
'''
# ---
replaces = {
    "Syncope": "Syncope (medicine)",
}


def work_test(All, allen):
    # This function takes in two dictionaries as input, 'All' and 'allen'.

    # Loop through each key-value pair in 'allen' dictionary.
    for a, tab in allen.items():
        # If the current key in 'allen' dictionary also exists in 'All' dictionary,
        # then update some specific values with the corresponding values in 'allen' dictionary.
        if a in All:
            All[a]['extlinks'] = tab['extlinks']
            All[a]['refsname'] = tab['refsname']
            All[a]['lead'] = tab['lead']
            All[a]['old'] = tab.get('old', {})

    # Create a file title for the log file
    filetitle = f'{project}/log_test.txt'

    # Call a function 'make_text' with 'All' dictionary as input and store the output in 'text' variable.
    text = text_bot.make_text(All)

    # Remove a specific string from 'text' variable.
    text = text.replace("height:580px;", "")

    # Print the number of links found in 'All' dictionary.
    printe.output(f'{len(All)} links found')

    # Print a message stating where the log file was saved.
    printe.output(f'<<lightyellow>> text loged to {filetitle}')

    # Define a page title and create an object of 'md_MainPage' class with some arguments.
    title = 'User:Mr. Ibrahem/prior/test'
    page = md_MainPage(title, 'www', family='mdwiki')

    # Get the current text of the page.
    oldtext = page.get_text()

    # Save the updated 'text' to the page with some additional parameters.
    page.save(newtext=text, summary='update', nocreate=0, minor='')

    # Return the updated 'text' variable.
    return text


def get_all_json():
    All = {}
    allen = {}
    # ---
    # get All json file inside dir project_js_new
    for filename in os.listdir(project_js_new):
        if filename.endswith('.json'):
            filename2 = os.path.join(project_js_new, filename)
            # ---
            printe.output(f'filename: {filename2}..')
            # ---
            data = json.load(open(filename2))
            All = {**All, **data}
    # ---
    for filename in os.listdir(project_js_newen):
        if filename.endswith('.json'):
            filename2 = os.path.join(project_js_newen, filename)
            # ---
            printe.output(f'filename: {filename2}..')
            # ---
            data = json.load(open(filename2))
            # ---
            allen = {**allen, **data}
    # ---
    for a, tab in allen.items():
        if a in All:
            All[a]['extlinks'] = tab['extlinks']
            All[a]['refsname'] = tab['refsname']
            All[a]['lead'] = tab['lead']
            All[a]['old'] = tab.get('old', {})
    # ---
    printe.output(f'new All len:{len(All)}')
    # ---
    return All


class WorkAll:
    def __init__(self):
        self.title = "WikiProjectMed:List/Prior"
        # ---
        self.All = get_all_json()
        # ---
        self.page = md_MainPage(self.title, 'www', family='mdwiki')
        self.text = self.page.get_text()
        # ---
        self.parser = wikitextparser.parse(self.text)
        # ---
        printe.output(f'all_wikilinks: {len(self.parser.wikilinks)}')
        # ---
        self.sections = self.parser.get_sections(include_subsections=False)
        # ---
        self.all_sections = {}

    def get_sectios_links(self):
        for s in self.sections:
            # ---
            t = s.title
            c = s.contents
            # ---
            if c is None or t is None:
                continue
            # ---
            # parser2 = wikitextparser.parse(c)
            # wikilinks = parser2.wikilinks
            wikilinks = s.wikilinks
            # ---
            wikilinks = [str(x.title) for x in wikilinks]
            # ---
            wikilinks = [replaces.get(x, x) for x in wikilinks]
            # ---
            if len(wikilinks) == 0:
                continue
            # ---
            t = t.replace('/', '-')
            # ---
            _all_ = {a: self.All[a] for a in wikilinks if a in self.All}
            # ---
            if len(_all_) < 150 or 'split' not in sys.argv:
                self.all_sections[t] = _all_
                continue
            # ---
            numb = 150
            # ---
            if t == 'Other drugs - procedures':
                numb = 103
            # ---
            elif len(_all_) < 300:
                numb = 150
            elif len(_all_) > 400:
                numb = 120
            # ---
            n = 1
            # ---
            for i in range(0, len(_all_), numb):
                # ---
                las = dict(list(_all_.items())[i : i + numb])
                # ---
                ta = f'{t}_{n}'
                # ---
                self.all_sections[ta] = las
                # ---
                n += 1

    def run(self):
        # ---
        self.get_sectios_links()
        # ---
        for t, _all_ in self.all_sections.items():
            lrnn = len(_all_.keys())
            # ---
            printe.output(f'<<lightyellow>> section:({t}), \t\twikilinks: {lrnn}')
            # ---
            ttt = f'User:Mr. Ibrahem/prior/{t}'
            # ---
            filetitle = f'{project}/log/{t}.txt'
            # ---
            text = text_bot.make_text(_all_, ttt=t)
            # ---
            if 'dontsave' not in sys.argv:
                codecs.open(filetitle, 'w', encoding='utf-8').write(text)
                # ---
                page_x = md_MainPage(ttt, 'www', family='mdwiki')
                # ---
                exists = page_x.exists()
                if not exists:
                    page_x.Create(text=text, summary='update')
                # ---
                else:
                    page_x_text = page_x.get_text()
                    # ---
                    page_x.save(newtext=text, summary='update', nocreate=0)


def work_all():
    # ---
    bot = WorkAll()
    bot.run()
    # ---
    page_x = md_MainPage('User:Mr. Ibrahem/prior', 'www', family='mdwiki')
    # ---
    if 'dontsave' not in sys.argv:
        t_sec = text_bot.get_t_sections()
        # ---
        page_x.save(newtext=t_sec, summary='update', nocreate=0)
    # ---
    if 'logall' in sys.argv:
        text_bot.log_all_pages_states()
    else:
        printe.output('<<lightyellow>> add "logall" to args to log All pages links green/red..')

    # ---


# ---
if __name__ == '__main__':
    if 'test' in sys.argv:
        work_test()
    else:
        work_all()
