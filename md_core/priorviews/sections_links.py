'''

from priorviews.sections_links import get_sectios_links

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
replaces = {
    "Syncope" : "Syncope (medicine)",
}
#---
class Sectios_links:
    def __init__(self):
        self.title = "WikiProjectMed:List/Prior"
        #---
        self.page = md_MainPage(self.title, 'www', family='mdwiki')
        self.text = self.page.get_text()
        #---
        self.parser = wikitextparser.parse(self.text)
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
            self.all_sections[t] = _all_
#---
def get_sectios_links():
    #---
    bot = Sectios_links()
    secs_links = bot.get_sectios_links()
    #---
    return secs_links
#---
if __name__ == '__main__':
    if 'test' in sys.argv:
        work_test()
    else:
        work_all()