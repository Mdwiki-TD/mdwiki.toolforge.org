
import sys
import pywikibot
import json
import os
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
text_v = '''
<div style="height:580px;width:100%;overflow-x:auto; overflow-y:auto">
{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! n
! style="position: sticky;top: 0;left: 0;" | title
!'''
#---
from priorviews import views
#---
all_view_by_lang = views.views_by_lang
#---
def make_lang_text(mdtitle, langlinks, langs_keys_sorted):
    """
    Returns a formatted string containing view counts for all available languages.
    """
    lang_text = ''
    u = 0

    # Loop through all available languages in the sorted order
    for l in langs_keys_sorted:
        u += 1

        # Get the title of the current language, or an empty string if not found
        title = langlinks.get(l, {}).get('title', '')

        # Get the view count for the current language and title, or 0 if not found
        view = all_view_by_lang.get(l, {}).get(title, 0)

        # Create a formatted string with the view count for the current language and title
        tt = f' || {view} '

        # If this is the first language being processed, do not prepend the formatted string with ' || '
        if u == 1:
            tt = f'{view} '

        # Append the formatted string to the overall formatted string
        lang_text += tt

    # Return the overall formatted string containing view counts for all available languages
    return lang_text
#---
def make_text(section, links):
    """
    Generate formatted text from given section and links.
    """

    # Create an empty list to store language keys.
    langs_keys = []

    # Loop through the dictionary of links and add the keys to langs_keys.
    for mdtitle, langs in links.items():
        langs_keys.extend(langs.keys())

    # Strip whitespace from keys in langs_keys and remove any empty strings.
    langs_keys = [x.strip() for x in langs_keys if x.strip() != '']

    # Remove duplicates from langs_keys and sort the list.
    langs_keys = list(set(langs_keys))
    langs_keys.sort()

    text = text_v
    # Add the language keys to text separated by '!!'.
    text += " !! ".join(langs_keys)
    n = 0

    # Loop through the dictionary of links.
    for mdtitle, langlinks in links.items():
        n += 1

        # Call make_lang_text to create the language text for this row.
        lang_text = make_lang_text(mdtitle, langlinks, langs_keys)

        # Create the table row with the language text and the row number.
        l_text = f'''|-\n! {n}\n! style="position: sticky;left: 0;" | [[{mdtitle}]]\n| {lang_text}'''

        # Add the row to the text variable.
        text += l_text

    # Add the closing table tag and div tag to the text variable.
    text += '\n|}\n</div>'

    # Create the final formatted text with the section header, number of links, and the table.
    faf = f'=={section} ({len(links)})==\n{text}'

    # Return the final formatted text.
    return faf
#---