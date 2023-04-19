'''

'''
import sys
import os
import re
import json
import urllib.parse
from urllib.parse import urlparse
import requests
import wikitextparser
import codecs
from mdpy import printe
#---
'''
#---
from prior import get_them
tt = get_them.work_in_one_lang_link()
#---
'''
#---
change_codes = {
    "bat_smg" : "bat-smg",
    "be_x_old" : "be-tarask",
    "be-x-old" : "be-tarask",
    "cbk_zam" : "cbk-zam",
    "fiu_vro" : "fiu-vro",
    "map_bms" : "map-bms",
    "nds_nl" : "nds-nl",
    "roa_rup" : "roa-rup",
    "zh_classical" : "zh-classical",
    "zh_min_nan" : "zh-min-nan",
    "zh_yue" : "zh-yue",
}
#---
def url_parser(url):
    parts = urlparse(url)
    directories = parts.path.strip('/').split('/')
    queries = parts.query.strip('&').split('&')
    #---
    queries1 = {}
    # x.split('=')[0] : x.split('=')[1] for x in queries
    #---
    for q in queries:
        if '=' not in q: continue
        k, v = q.split('=')
        queries1[k] = v
    #---
    elements = {
        'scheme': parts.scheme,
        'netloc': parts.netloc,
        'path': parts.path,
        'params': parts.params,
        'query': parts.query,
        'fragment': parts.fragment,
        'directories': directories,
        'queries': queries1,
    }
    
    return elements
#---
def filter_urls(links):
    #---
    liste1 = []
    #---
    # delete link like web.archive.org
    for x in links:
        #---
        if x.startswith('//'):  x = 'https:' + x
        #---
        x = x.replace('//www.', '//').replace('http://', 'https://')
        #---
        # un urlencode 
        # x = x.replace('%3A', ':').replace('%2F', '/').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
        x = urllib.parse.unquote(x)
        #---
        x = x.replace('//www.', '//').replace('http://', 'https://')
        # https://web.archive.org/web/20100724032458/https://nlm.nih.gov/medlineplus/druginfo/natural/patient-riboflavin.html
        if 'web.archive.org' in x:
            # match https://web.archive.org/web/20230123155031 and delete it
            x = re.sub(r'^https://web\.archive\.org/web/[\d]+/', '', x)
        elif 'archive.org/details' in x:
            # https://archive.org/details/masterdentistry0000unse/page/180
            x = x.split('/page')[0]
        #---
        if 'archive.is' in x:
            x = re.sub(r'^https://[\w]+\.archive\.is/[\d]+/', '', x)
        x = x.replace('//www.', '//').replace('http://', 'https://')
        #---
        # https://books.google.ca/books?id=JaOoXdSlT9sC&pg=PA11
        if 'books.google' in x and not 'books' in sys.argv:
            #---
            prased = url_parser(x)
            # {'scheme': 'https', 'netloc': 'books.google.ca', 'path': '/books', 'params': '', 'query': 'id=JaOoXdSlT9sC&pg=PA11', 'fragment': '', 'directories': ['books'], 'queries': {'id': 'JaOoXdSlT9sC', 'pg': 'PA11'}}
            #---
            x = re.sub(prased['netloc'], 'books.google.com', x)
            book_id = prased['queries'].get('id', '')
            if book_id != '':
                x2 = f'https://books.google.com/books?id={book_id}'
                if x2 != x:
                    # printe.output('<<yellow>> google books + 1')
                    x = x2
        #---
        liste1.append(x.lower())
    #---
    # remove duplicates
    liste1 = list(set(liste1))
    #---
    liste1.sort()
    #---
    return liste1
#---
class work_in_one_lang_link(object):

    def __init__(self, lang, title):
        self.lang = change_codes.get(lang) or lang
        #---

        #---
        self.title = title
        self.url = 'https://' +  self.lang + '.wikipedia.org/w/api.php'
        self.text = ''
        self.extlinks = []
        self.refsnames = []
        #---
        self.session = requests.Session()
        #---
        self.start()

    def start(self):
        self.get_text()
        #---
        self.get_extlinks()
        #---
        self.get_ref_names()
        
    def post_to_json(self, params):
        json1 = {}
        #---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        #---
        return json1

    def get_ref_names(self):
        #---
        parsed = wikitextparser.parse(self.text)
        tags = parsed.get_tags()
        #---
        _tags_ = []
        #---
        for x in tags:
            if x.name != 'ref': continue
            #---
            attrs = x.attrs
            name = attrs.get('name', '').replace('/', '').lower().strip()
            #---
            if name == '' : continue
            #---
            if not name in _tags_:  _tags_.append(name)
        #---
        self.refsnames = _tags_
    
    #---
    def get_text(self):
        params = { "action": "parse", "format": "json", "prop": "wikitext", "page": self.title, "utf8": 1}
        #---
        json1 = self.post_to_json(params)
        #---
        self.text = json1.get('parse',{}).get('wikitext',{}).get('*','')
        #---
    
    #---
    def get_extlinks(self):
        params = {
            "action": "query",
            "format": "json",
            "prop": "extlinks", 
            "titles": self.title, 
            "formatversion": "2", 
            "utf8": 1, 
            "ellimit": "max"
            }
        #---
        elcontinue = 'x'
        #---
        links = []
        #---
        while elcontinue != '':
            #---
            if elcontinue not in ['x', '']:
                params['elcontinue'] = elcontinue
            #---
            json1 = self.post_to_json(params)
            #---
            elcontinue = json1.get('continue', {}).get('elcontinue', '')
            #---
            linkso = json1.get('query',{}).get('pages',[{}])[0].get('extlinks',[])
            #---
            links.extend(linkso)
        #---
        links = [ x['url'] for x in links ]
        #---
        liste1 = filter_urls(links)
        #---
        self.extlinks = liste1
        #---
#---
if __name__ == '__main__':
    #---
    t = work_in_one_lang_link('or', 'ଓଠକୋଣ_ପ୍ରଦାହ')
    orex = t.extlinks
    print(f'orex: {len(orex)}')
    print("\n".join(orex))
    #---
    print('------------------------')
    #---
    t2 = work_in_one_lang_link('en', 'Angular_cheilitis')
    enex = t2.extlinks
    print(f'enex: {len(enex)}')
    print("\n".join(enex))
    #---
    print('------------------------')
    #---
    new = [ x for x in orex if x in enex ]
    print(f'new: {len(new)}')
    #---