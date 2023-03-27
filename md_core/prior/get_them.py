'''

'''
import sys
import os
import re
import json
import urllib.parse
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
        params = {"action": "query","format": "json","prop": "extlinks","titles": self.title,"formatversion": "2", "utf8": 1, "ellimit": "max"}
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
        liste1 = []
        # delete link like web.archive.org
        for x in links:
            x = x.replace('//www.', '//').replace('http://', 'https://')
            #---
            # un urlencode 
            # x = x.replace('%3A', ':').replace('%2F', '/').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
            x = urllib.parse.unquote(x)
            #---
            x = x.replace('//www.', '//').replace('http://', 'https://')
            if 'web.archive.org' in x:
                # match https://web.archive.org/web/20230123155031 and delete it
                x = re.sub(r'^https://web\.archive\.org/web/[\d+]/', '', x)
            #---
            if 'archive.is' in x:
                x = re.sub(r'^https://[\w]+\.archive\.is/[\d+]/', '', x)
            x = x.replace('//www.', '//').replace('http://', 'https://')
            #---
            liste1.append(x.lower())
        #---
        # remove duplicates
        liste1 = list(set(liste1))
        #---
        self.extlinks = liste1
        #---
#---
if __name__ == '__main__':
    #---
    lang = 'be_x_old'
    title = 'test'
    #---
    work_in_one_lang_link(lang, title)
    #---