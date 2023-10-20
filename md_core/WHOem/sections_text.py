'''

from priorviews.bots import sections_text #make_text(section, links)

python3 core8/pwb.py priorviews/sections_text

'''
import json
import codecs
import sys
from pathlib import Path

# ---
Dir = Path(__file__).parent
# ---
text_v = '''
<div style="height:1500px;width:100%;overflow-x:auto; overflow-y:auto">
{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! #
! style="position: sticky;top: 0;left: 0;" | Title
! Views
! Articles
!'''
# ---
section_langs_views = {}
# ---
with codecs.open(f'{Dir}/lists/lang_links_mdtitles.json', 'r', encoding='utf-8') as f:
    lang_links_mdtitles = json.load(f)
# ---
# sort lang_links_mdtitles by lenth
lang_to_wrks = dict(sorted(lang_links_mdtitles.items(), key=lambda x: len(x[1]), reverse=True))
# change it to list
lang_to_wrks = list(lang_to_wrks.keys())


def make_lang_text(mdtitle, langlinks, langs_keys_sorted):
    lang_text = ''
    u = 0

    # ---
    if 'test1' in sys.argv:
        print('mdtitle:', mdtitle)
        print('langlinks:', langlinks)
    # ---

    for l in langs_keys_sorted:
        u += 1
        if l not in section_langs_views:
            section_langs_views[l] = 0
        view = ''

        data = langlinks.get(l)
        # print('data:', data)#{'title': 'قائمة الأدوية الأساسية النموذجية لمنظمة الصحة العالمية', 'views': 159424}

        if data:
            title = data['title']
            view = data['views']
            section_langs_views[l] += view
            # ---
            # view = helps.views_url(title, l, view)
            view = f'[[:w:{l}:{title}|{view:,}]]'
            # ---
        # Create a formatted string with the view count for the current language and title
        tt = f' || {view}'

        # If this is the first language being processed, do not prepend the formatted string with ' || '
        if u == 1:
            tt = f'{view}'

        # Append the formatted string to the overall formatted string
        lang_text += tt

    # Return the overall formatted string containing view counts for all available languages
    return lang_text


def make_text(ViewsData):
    """
    Generate formatted text from given section and links.
    """
    text = text_v
    # ---
    langs_keys = [lang for mdtitle, tab in ViewsData.items() for lang in tab.keys()]
    langs_keys = sorted(set(langs_keys))
    # ---
    langs_keys = lang_to_wrks

    # ---
    # print(langs_keys)
    # ---
    # Add the language keys to text separated by '!!'.
    # text += " " + " !! ".join(langs_keys)

    def format_x(x):
        if len(x) < 4:
            return x
        # ---
        x2 = x.replace('-', '')
        x2 = x2[:3]
        # ---
        return "{{abbr|" + f"{x2}|{x}" + "}}"

    def fo_n(x):
        return f'{x:,}'

    langs_keys_text = " !! ".join([format_x(x) for x in langs_keys])
    text += f" {langs_keys_text}"

    n = 0

    section_views = 0

    # Loop through the dictionary of links.
    for mdtitle, langlinks in ViewsData.items():
        n += 1

        articles = len(langlinks)
        # Call make_lang_text to create the language text for this row.
        lang_text = make_lang_text(mdtitle, langlinks, langs_keys)

        mdtitle_views = sum([x['views'] for x in langlinks.values()])

        section_views += mdtitle_views
        # Create the table row with the language text and the row number.
        l_text = '\n|-\n'
        l_text += f'! {n}\n'
        l_text += f'! style="position: sticky;left: 0;" | [[{mdtitle}]]\n'
        l_text += f'! {mdtitle_views:,}\n'
        l_text += f'! {articles:,}\n'
        l_text += f'| {lang_text}'

        # Add the row to the text variable.
        text += l_text

    # total views by language
    text += '\n|-\n'
    text += f'! !! style="position: sticky;left: 0;colspan:2;" | Total views !! {section_views:,} \n'
    text += '! \n! '
    text += " !! ".join([str(fo_n(section_langs_views.get(l, 0))) for l in langs_keys])

    # Add the closing table tag and div tag to the text variable.
    text += '\n|}\n</div>'
    # ---
    all_articles = sum([len(x) for x in ViewsData.values()])
    # Create the final formatted text with the section header, number of links, and the table.
    # ---
    faf = f'* {all_articles:,} articles with work in {len(langs_keys):,} languages\n'
    faf += f'* {section_views:,} pageviews from July 2015 to Sept 2023\n{text}'

    # Return the final formatted text.
    return faf
