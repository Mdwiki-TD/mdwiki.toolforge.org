"""

python3 ./core8/pwb.py priorviews/bot test

"""
import sys
import pywikibot
import json
import os
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
file = f'{Dir}/all_pages_states.json'
#---
from priorviews.links_by_section import sections_to_views
from priorviews import sections_text
#---
# find the section with the least links
least_section = min(sections_to_views, key=lambda x: len(sections_to_views[x]))
print(f'least section: {least_section}')
# print lenth of least_section in sections_to_views
print(f'lenth of least_section: {len(sections_to_views[least_section])}')
#---
sections_to_views = sections_to_views.copy()
#---
if 'test' in sys.argv:
    sections_to_views = { least_section : sections_to_views[least_section] }
#---
# make text for each section
for section, links in sections_to_views.items():
    #---
    text = sections_text.make_text(section, links)
    #---
    print(text)
    #---

    