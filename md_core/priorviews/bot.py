"""

python3 ./core8/pwb.py priorviews/bot test

"""
import sys
import pywikibot
import json
import os
import codecs
#---
from priorviews.links_by_section import sects_links_langlinks
from priorviews import sections_text
#---
# make text for each section
for section, links in sects_links_langlinks.items():
    #---
    text = sections_text.make_text(section, links)
    #---
    print(text)
    #---

    