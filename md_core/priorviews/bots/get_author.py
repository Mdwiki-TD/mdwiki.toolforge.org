'''

python3 pwb.py priorviews/bots/get_author

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
'''
#---
from priorviews.bots import get_author
tt = get_author.get_au(title, lang)
#---
'''
#---
def isv(comment):
    #---
    comment = comment.lower()
    #---
    if comment.find('translators without borders') != -1 :  return True
    if comment.find('(twb)') != -1 :  return True
    #---
    return False
#---
class FindAuthor(object):

    def __init__(self, title, lang="en"):
        #---
        self.lang = lang
        self.title = title
        self.url = 'https://' +  self.lang + '.wikipedia.org/w/api.php'
        self.author = ''
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
            printe.output(f"get_old:\t\t{unurl}")
        #---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        #---
        return json1

    def start(self):
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": self.title,
            "formatversion": "2",
            "rvprop": "comment|user",
	        "rvdir": "newer",
            "rvlimit": "max"
        }
        #---
        rvcontinue = 'x'
        #---
        while rvcontinue != '':
            #---
            if rvcontinue != 'x' : params['rvcontinue'] = rvcontinue
            #---
            json1 = self.post_to_json(params)
            #---
            rvcontinue = json1.get( "continue" , {} ).get( "rvcontinue" , '' )
            #---
            pages = json1.get('query',{}).get('pages',[{}])
            #---
            for p in pages:
                revisions = p.get("revisions", [])
                for r in revisions:
                    # print(r)
                    comment = r.get('comment', '').lower()
                    if isv(comment):
                        # print(r)
                        self.author = r.get('user', '')
                        return
        #---

    def Author(self):
        printe.output(f'\t\t Author: {self.author}')
        return self.author
def get_au(title, lang):
    #---
    bot = FindAuthor(title, lang=lang)
    #---
    auu = bot.Author()
    #---
    return auu
#---
if __name__ == '__main__':
    #---
    t = get_au('نكاف', "ar")
    print(f'au: {t}')
    sys.exit()
    #---