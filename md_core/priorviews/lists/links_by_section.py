"""


from priorviews.lists.links_by_section import sects_links_langlinks

python3 core8/pwb.py priorviews/lists/links_by_section

"""
import sys
import json
import os
from pathlib import Path
import codecs

# ---
from mdpy import printe

# ---
from priorviews.bots.sections_links import get_section_links

# ---
Dir = Path(__file__).parent
# get the dir 2 levels back
# ---
_Dir_ = os.path.dirname(os.path.dirname(Dir))
# ---
all_pages_states = json.load(codecs.open(f'{_Dir_}/priorviews/lists/all_pages_states.json', 'r', 'utf-8'))
# ---
printe.output(f'<<lightgreen>> len of all_pages_states: {len(all_pages_states)}')
# ---
mdtitles_lang_title = {}
# ---
for mdtitle, langs in all_pages_states.items():
    # ---
    newlangs = {
        lang: v['title']
        for lang, v in langs.items() if v['title'] != '' and v['color'] == 'green'
    }
    # ---
    # if 'test' in sys.argv: print(newlangs)
    # ---
    mdtitles_lang_title[mdtitle] = newlangs
# ---
printe.output(f'<<lightgreen>> len of mdtitles_lang_title: {len(mdtitles_lang_title)}')
# ---
sections_links = get_section_links()
# ---
sects_links_langlinks = {}
# ---
links_done = []
# ---
# split lists by sections
for section, links in sections_links.items():
    # ---
    _links_ = ['Tooth decay', 'Angular cheilitis', 'Bad breath', 'Leukoplakia', 'Periodontal disease', 'Tonsil stones']
    # ---
    sec_links = {
        x: tab
        for x, tab in mdtitles_lang_title.items() if x in links
    }
    # ---
    links_done.extend(sec_links.keys())
    # ---
    sects_links_langlinks[section] = sec_links
# ---
links_by_lang = {}
# ---
least_section = min(sects_links_langlinks, key=lambda x: len(sects_links_langlinks[x]))
# ---
if 'small' in sys.argv:
    sects_links_langlinks = {
        least_section: sects_links_langlinks[least_section]
    }
# ---
# make text for each section
for section, links in sects_links_langlinks.items():
    # ---
    for md, langs in links.items():
        for lang, title in langs.items():
            if lang not in links_by_lang:
                links_by_lang[lang] = []
            links_by_lang[lang].append(title)
# ---
printe.output(f'<<lightgreen>> len of sects_links_langlinks: {len(sects_links_langlinks)}')
# ---
links_done = list(set(links_done))
# ---
if len(links_done) != len(mdtitles_lang_title.keys()):
    print(f'len of links_done: {len(links_done)}')
    # ---
    # find diff
    # ---
    diff = list(set(mdtitles_lang_title.keys()) - set(links_done))
    # ---
    printe.output(f'<<lightred>> len of diff: {len(diff)}')
    print(diff)
# ---
# find the section with the least links
print(f'least section: {least_section}')
# print lenth of least_section in sects_links_langlinks
print(f'lenth of least_section: {len(sects_links_langlinks[least_section])}')
# ---
# ---
sects_links_langlinks = sects_links_langlinks.copy()
# ---
if 'test' in sys.argv:
    sects_links_langlinks = {
        least_section: sects_links_langlinks[least_section]
    }
# ---
if __name__ == '__main__':
    ll = sects_links_langlinks
    # ---
    '''
    for s, ls in ll.items():
        print(f'section: {s}')
        print(f'len of links: {len(ls)}')
        if len(ls) < 10:
            print(ls)
    '''
    # ---
    # print(links_by_lang['ar'])
    print(len(links_by_lang['ar']))
    # ---
