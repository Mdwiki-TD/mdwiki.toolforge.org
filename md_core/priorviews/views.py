
import sys
import pywikibot
import json
import os
import re
import codecs
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
file = f'{Dir}/views_mdwiki_langs.json'
#---
if not os.path.exists(file):
    with open(file, 'w') as f:  json.dump({}, f)
#---
data = json.load(codecs.open(file, 'r', 'utf-8'))
#---
_data = { 
    "mdtitle" : {
        "ar" : {"title": "artitle", "views" : 0},
        "en" : {"title": "entitle", "views" : 0}
    }
}
#---
all_views_by_mdtitle = {}
count_views_by_lang    = {}
views_by_lang        = {}
#---
def makeviews():
    global _data_, all_views_by_mdtitle, count_views_by_lang, views_by_lang
    #---
    for mdtitle, langs in _data_.items():
        #---
        all_views_by_mdtitle[mdtitle] = {}
        #---
        for lang, v in langs.items():
            if not lang in views_by_lang:   views_by_lang[lang] = {}
            #---
            if not lang in count_views_by_lang:   count_views_by_lang[lang] = 0
            #---
            all_views_by_mdtitle[mdtitle][lang] = v['views']
            #---
            views_by_lang[lang][v['title']] = v['views']
            #---
            count_views_by_lang[lang] += v['views']
#---
makeviews()
#---