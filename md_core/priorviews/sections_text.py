
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
    #---
    lang_text = ''
    #---
    u = 0
    #---
    for l in langs_keys_sorted:
        #---
        u += 1
        #---
        title = langlinks.get(l, {}).get('title', '')
        #---
        view = all_view_by_lang.get(l, {}).get(title, 0)
        #---
        tt = f' || {view} '
        #---
        if u == 1:  tt = f'{view} '
        #---
        lang_text += tt
        #---
    #---
    return lang_text
#---
def make_text(section, links):
    """
    Generate formatted text from given section and links.
    """
    #---
    langs_keys = []
    #---
    for mdtitle, langs in links.items():
        langs_keys.extend(langs.keys())
    #---
    langs_keys = [ x.strip() for x in langs_keys if x.strip() != '']
    #---
    langs_keys = list(set(langs_keys))
    langs_keys.sort()
    #---
    text       = text_v
    #---
    text += " !! ".join(langs_keys)
    #---
    n = 0
    #---
    for mdtitle, langlinks in links.items():
        #---
        n += 1
        #---
        lang_text = make_lang_text(mdtitle, langlinks, langs_keys)
        #---
        l_text = f'''|-\n! {n}\n! style="position: sticky;left: 0;" | [[{mdtitle}]]\n| {lang_text}'''
        #---
        text += l_text
    #---
    text += '\n|}\n</div>'
    #---
    green_line = ''
    red_line   = ''
    #---
    faf = f'=={section} ({len(links)})==\n{text}'
    #---
    return faf
#---
