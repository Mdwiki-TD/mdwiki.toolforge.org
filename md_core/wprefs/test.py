"""
"""

import pywikibot
from wprefs.bot import *

# ---
title = 'Utilizator:Mr._Ibrahem/teste'
lang = 'ro'
log(lang)
# ---
text = GetPageText(title, lang=lang)
# ---
newtext = fix_page_here(text, title, lang)
# ---
# ---
pywikibot.showDiff(text, newtext)
# ---
