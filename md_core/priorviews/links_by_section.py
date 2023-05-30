
import sys
import pywikibot
import json
import os
import codecs
#---
from priorviews.links_by_section import sections_to_views
from priorviews.sections_links import get_sectios_links
#---
Dir = os.path.dirname(os.path.abspath(__file__))
file = f'{Dir}/all_pages_states.json'
#---
data = json.load(codecs.open(file, 'r', 'utf-8'))
#---
mdtitles_lang_title = {}
#---
for mdtitle, langs in data.items():
    #---
    newlangs = {lang: v['title'] for lang, v in langs.items() if v['title'] != '' and v['color'] == 'green'}
    #---
    mdtitles_lang_title[mdtitle] = newlangs
#---
print(newlangs)
#---
print(f'len of mdtitles_lang_title: {len(mdtitles_lang_title)}')
#---
sections_links = get_sectios_links()
#---
sections_to_views = {}
#---
links_done = []
#---
# split lists by sections
for section, links in sections_links.items():
    #---
    sec_links = {x: tab for x, tab in mdtitles_lang_title.items() if x in links}
    #---
    links_done.extend(sec_links.keys())
    #---
    sections_to_views[section] = sec_links
#---
print(f'len of sections_to_views: {len(sections_to_views)}')
#---
links_done = list(set(links_done))
#---
if len(links_done) != len(mdtitles_lang_title.keys()):
    print(f'len of links_done: {len(links_done)}')
    print(f'len of mdtitles_lang_title: {len(mdtitles_lang_title)}')
    #---
    # find diff
    #---
    diff = list(set(mdtitles_lang_title.keys()) - set(links_done))
    #---
    print(f'len of diff: {len(diff)}')
    print(diff)
#---
