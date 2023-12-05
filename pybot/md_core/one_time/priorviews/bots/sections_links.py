'''

from priorviews.bots.sections_links import get_section_links

python3 core8/pwb.py priorviews/sections_links

'''
import os
from pathlib import Path
import json
import wikitextparser
import codecs

# ---
from mdpy import printe

# ---
from new_api.mdwiki_page import MainPage as md_MainPage

# ---
Dir = Path(__file__).parent
Dir = os.path.dirname(Dir)
# ---
sect_file = f'{Dir}/lists/secs_links.json'
if not os.path.exists(sect_file):
    with open(sect_file, 'w') as f:
        json.dump({}, f)
# ---
old = json.load(codecs.open(sect_file, 'r', 'utf-8'))
# ---
replaces = {
    "Syncope": "Syncope (medicine)",
}
# ---


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

            wikilinks = [str(x.title) for x in wikilinks if str(x.title).lower() not in self.titles_done]

            # remove duplicates
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


def dump_secs_links(secs_links):
    # ---
    global sect_file
    # ---
    if secs_links != {}:
        printe.output(f'<<lightyellow>> secs_links(): lenth: {len(secs_links.keys())}')
        json.dump(secs_links, codecs.open(sect_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


def get_section_links(new=False):
    """
    Retrieves the links to the sections from the Sectios_links bot.
    """
    if new or len(old) == 0:
        # Instantiate an object of the Sectios_links class.
        bot = Sectios_links()

        bot.run()

        # Retrieve the links to the sections
        secs_links = bot.SectionsToLinks

        dump_secs_links(secs_links)
    else:
        secs_links = old
    # ---
    return secs_links


# ---
if __name__ == '__main__':
    all_links = {}
    # ---
    ll = get_section_links()
    # ---
    for s, ls in ll.items():
        print(f'section: {s}')
        print(f'len of links: {len(ls)}')
        if len(ls) < 10:
            print(ls)
        # ---
        for link in ls:
            if link.lower() not in all_links:
                all_links[link.lower()] = []
            if s not in all_links[link.lower()]:
                all_links[link.lower()].append(s)
    # ---
    printe.output('<<red>>---------------')
    # ---
    for x, v in all_links.items():
        if len(v) > 1:
            sections = ", ".join(v)
            print(f'link: ({x}) in {len(v)} sections: {sections}')
    # ---
