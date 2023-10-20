"""

python3 core8/pwb.py priorviews/bot test

"""
from new_api.mdwiki_page import MainPage as md_MainPage
from priorviews import by_lang
from priorviews.lists import views
from priorviews.bots import sections_text
from priorviews.lists.links_by_section import sects_links_langlinks
import sys
from pathlib import Path

# ---
Dir = Path(__file__).parent
# ---
# ---
'''
page      = md_MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
# ---
text        = page.get_text()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
'''
# ---
titles = []
titles_1 = []
# ---
# make text for each section
for section, links in sects_links_langlinks.items():
    # ---
    ntext = sections_text.make_text(section, links)
    # ---
    if 'test' in sys.argv:
        print(ntext)
    # ---
    title = f'User:Mr. Ibrahem/priorviews/{section}'
    # ---
    titles_1.append(section)
    titles.append(title)
    # ---
    if 'write' in sys.argv:
        page = md_MainPage(title, 'www', family='mdwiki')
        exists = page.exists()
        if not exists:
            create = page.Create(text=ntext, summary='update')
        else:
            # ---
            text = page.get_text()
            save_page = page.save(newtext=ntext, summary='update', nocreate=1, minor='')

# ---
all_section_views = sections_text.all_section_views - by_lang.en_views
print(f'<<lightgreen>> all_section_views: {all_section_views:,}')
# ---
newtext = ''
newtext += '; (Views from July 2015 to June 2023).\n'
newtext += '* Enwiki: ([[WikiProjectMed:List/Prior|1338 articles]]):\n'
newtext += f'** Total views: {by_lang.en_views:,}\n'

newtext += f'* Translations: {by_lang.total_tra:,}:\n'

total_langs = len(views.count_views_by_lang) - 1
# ---
newtext += f'''
** Total languages: {total_langs:,}
** Total views: {by_lang.total_views:,}
** Total words: {by_lang.total_wrds:,}
* [[User:Mr. Ibrahem/priorviews/bylang|Views, Words and Translators by language]]
* [[User:Mr. Ibrahem/priorviews/translators|All translators]]

==Views by section==
* Views by section and language and title:
'''
# ---
newtext += '\n'.join([f'** [[User:Mr. Ibrahem/priorviews/{t}|{t}]]' for t in titles_1])
# ---
page = md_MainPage('User:Mr. Ibrahem/priorviews', 'www', family='mdwiki')
exists = page.exists()
if not exists:
    create = page.Create(text=newtext, summary='update')
else:
    # ---
    text = page.get_text()
    save_page = page.save(newtext=newtext, summary='update', nocreate=1, minor='')

# ---

# ---
