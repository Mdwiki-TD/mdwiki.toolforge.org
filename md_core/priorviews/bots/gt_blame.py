'''

python3 pwb.py priorviews/bots/gt_blame

'''
import sys
import os
import re
import json
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import urlencode
import requests
import wikitextparser
import codecs
from mdpy import printe
#---
from wikiblame.bot import get_blame #first, result = get_blame({"lang": "es", "article": "Letrina " ,"needle": "Till2014"})
#---
from prior.json_langs.lists import json_langs_by_langs
# tab = json_langs_by_langs.get(lang, {}).get(title, {})# {'extlinks': extlinks, 'refsname': refsname}
#---
class FindInHistory:


    def __init__(self, title, lang="en", refname=[], extlinks=[]):
        #---
        self.lang = lang
        self.title = title
        self.url = 'https://' +  self.lang + '.wikipedia.org/w/api.php'
        self.author = ''
        #---
        self.revisions = []
        self.refname = refname
        self.extlinks = extlinks
        #---
        self.session = requests.Session()
        #---
        self.start()

    def post_to_json(self, params):
        json1 = {}
        #---
        unurl = f"{self.url}?{urlencode(params)}"
        #---
        if "printurl" in sys.argv and "text" not in params:
            printe.output(f"post_to_json:\t\t{unurl}")
        #---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        #---
        return json1

    def post_continue(self, params, action, _p_, p_empty):
        #---
        continue_params = {}
        #---
        results = p_empty
        #---
        while continue_params != {} or len(results) == 0:
            #---
            if continue_params:
                params = {**params, **continue_params}
            #---
            json1 = self.post_to_json(params)
            #---
            if not json1 or json1 == {}:    break
            #---
            continue_params = json1.get("continue", {})
            #---
            data = json1.get(action, {}).get(_p_, p_empty)
            #---
            if not data: break
            #---
            printe.output(f'post_continue, len:{len(data)}, all: {len(results)}')
            #---
            if isinstance(results, list):
                results.extend(data)
            else:
                results = {**results, **data}
        #---
        return results

    def get_revisions(self, title):
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": title,
            "utf8": 1,
            "formatversion": "2",
            "rvprop": "comment|timestamp|user|content|ids",
	        "rvdir": "newer",
            "rvlimit": "max"
        }
        #---
        pages = self.post_continue(params, "query", "pages", [])
        #---
        return pages

    def start(self):
        pages = self.get_revisions(self.title)
        for p in pages:
            for r in p.get("revisions", []):
                if r.get('anon'):
                    continue
                self.revisions.append(r)
    
def search_history(title, lang, refname=[], extlinks=[]):
    #---
    tab = {"lang": lang, "article": title, "needle": ""}
    #---
    if refname == [] or extlinks == []:
        infos = json_langs_by_langs.get(lang, {}).get(title)# {'extlinks': extlinks, 'refsname': refsname}
        #---
        if not infos:
            return ''
        #---
        refname  = infos.get('refsname')
        extlinks = infos.get('extlinks')
    #---
    bot = FindInHistory(title, lang, refname, extlinks)
    revisions = bot.revisions
    #---
    for r in revisions:
        print(r.keys())
        # dict_keys(['revid', 'parentid', 'user', 'timestamp', 'contentformat', 'contentmodel', 'content', 'comment'])
        #---
        user = r.get('user', '')
        #---

    #---
    print(f'len of revisions: {len(revisions)}')
    #---
    return ''
#---
if __name__ == '__main__':
    #---
    t = search_history('نكاف', "ar")
    print(f'au: {t}')
    sys.exit()
    #---