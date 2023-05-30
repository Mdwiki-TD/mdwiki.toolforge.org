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
        self.all_sections = {}

    def get_sectios_links(self):
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
            wikilinks = [str(x.title) for x in wikilinks]

            # Replace any links with their corresponding values in the replaces dict
            wikilinks = [replaces.get(x, x) for x in wikilinks]

            # If there are no wikilinks in the section, skip it
            if len(wikilinks) == 0:
                continue

            # Replace any forward slashes in the section title with hyphens
            t = t.replace('/', '-')

            # Get all the sections for the wikilinks that are in the 'all' dict
            _all_ = {a: self.all[a] for a in wikilinks if a in self.all}

            # Add the section and its links to the all_sections dict
            self.all_sections[t] = _all_
#---
def get_section_links():
    """
    Retrieves the links to the sections from the Sectios_links bot.
    """
    # Instantiate an object of the Sectios_links class.
    bot = Sectios_links()

    # Retrieve the links to the sections using the get_sectios_links method of the bot object.
    secs_links = bot.get_sectios_links()

    # Return the list of links to the sections.
    return secs_links
#---
if __name__ == '__main__':
    if 'test' in sys.argv:
        work_test()
    else:
        work_all()