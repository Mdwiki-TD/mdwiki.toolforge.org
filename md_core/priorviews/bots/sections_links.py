'''

from priorviews.bots.sections_links import get_section_links

python3 ./core8/pwb.py priorviews/sections_links

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
        """
        Initializes an instance of the class.
        """
        # Set the title of the page to be scraped
        self.title = "WikiProjectMed:List/Prior"

        # Create a new instance of md_MainPage with the specified title and family
        self.page = md_MainPage(self.title, 'www', family='mdwiki')

        # Get the text content of the page
        self.text = self.page.get_text()

        # Parse the text content of the page using wikitextparser
        self.parser = wikitextparser.parse(self.text)

        # Get the top-level sections of the parsed page
        self.sections = self.parser.get_sections(include_subsections=False)

        # Create an empty dictionary to store all sections of the page
        self.SectionsToLinks = {}

        self.titles_done = []

    def run(self):
        """
        Generate links for each section in the given wiki page.
        """
        # Loop through each section in the wiki page
        for s in self.sections:
            # Get the title and contents of the section
            t = s.title
            c = s.contents

            # If either the contents or title are None, skip the section
            if c is None or t is None:
                continue

            # Get the wikilinks for the section and convert them to strings
            wikilinks = s.wikilinks
            
            wikilinks = [str(x.title) for x in wikilinks if not str(x.title).lower() in self.titles_done]

            # remove duplicts
            wikilinks = list(set(wikilinks))

            # expend self.titles_done
            self.titles_done.extend([x.lower() for x in wikilinks])

            # Replace any links with their corresponding values in the replaces dict
            wikilinks = [replaces.get(x, x) for x in wikilinks]

            # If there are no wikilinks in the section, skip it
            if len(wikilinks) == 0:
                continue

            # Replace any forward slashes in the section title with hyphens
            t = t.replace('/', '-')

            # Add the section and its links to the all_sections dict
            self.SectionsToLinks[t] = wikilinks
#---
def get_section_links():
    """
    Retrieves the links to the sections from the Sectios_links bot.
    """
    # Instantiate an object of the Sectios_links class.
    bot = Sectios_links()

    bot.run()

    # Retrieve the links to the sections
    secs_links = bot.SectionsToLinks

    # Return the list of links to the sections.
    return secs_links
#---
if __name__ == '__main__':
    all_links = {}
    #---
    ll = get_section_links()
    #---
    for s, ls in ll.items():
        print(f'section: {s}')
        print(f'len of links: {len(ls)}')
        if len(ls) < 10:
            print(ls)
        #---
        for link in ls:
            if not link.lower() in all_links: all_links[link.lower()] = []
            if not s in all_links[link.lower()]: all_links[link.lower()].append(s)
    #---
    printe.output('<<red>>---------------')
    #---
    for x, v in all_links.items():
        if len(v) > 1:
            sections = ", ".join(v)
            print(f'link: ({x}) in {len(v)} sections: {sections}')
    #---