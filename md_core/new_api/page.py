from warnings import warn
import pywikibot
import urllib
import requests
import os
import json
import sys
import wikitextparser
#---
"""

from new_api.page import MainPage
'''
page      = MainPage(title, 'ar')
exists    = page.exists()
if not exists: return
#---
page_edit = page.can_edit()
if not page_edit: return
#---
if page.isRedirect() :  return
# target = page.get_redirect_target()
#---
text        = page.get_text()
ns          = page.namespace()
links       = page.page_links()
categories  = page.get_categories(with_hidden=False)
langlinks   = page.get_langlinks()
wiki_links  = page.get_wiki_links_from_text()
refs        = page.Get_tags(tag='ref')# for x in ref: name, contents = x.name, x.contents
words       = page.get_words()
templates   = page.get_templates()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
create      = page.Create(text='', summary='')
#---
back_links  = page.page_backlinks()
text_html   = page.get_text_html()
hidden_categories= page.get_hidden_categories()
flagged     = page.is_flagged()
timestamp   = page.get_timestamp()
user        = page.get_user()
purge       = page.purge()
'''

"""
#---

#---
# from API import botEdit
from new_api import txtlib
from new_api import printe
# ingr = txtlib.extract_templates_and_params(text)
# for temp in ingr: name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
#---
ar_lag = { 1 : 3 }
#---
print_test = {1:False}
#---
from mdpy import user_account_new
#---
Edit_summary_line = { 1 : ' -Edit summary: %s:' }
#---
himo_file = __file__.replace('\\','/').split("/")[-1]
#---
User_tables = { "username" : user_account_new.my_username, "password" : user_account_new.my_password }
#---
Main_User = { 1: User_tables['username'] }
Bot_or_himo = { 1: ""}
#---
import inspect
def warn_err(err):
    err = str(err)
    nn = inspect.stack()[1][3]
    return f'\ndef {nn}(): {err}'
#---
def make_user(himo_file):
    #---
    Main_User[1] = User_tables['username']
    #---
    if Main_User[1].find("bot") == -1:
        Bot_or_himo[1] = 1
#---
make_user(himo_file)
#---
wiki_loged = {'lang':''}
#---
SS = {}
#---
class Login():
    def __init__(self, lang):
        self.lang = lang
        wiki_loged['lang'] = self.lang
        self.family   = 'wikipedia'
        self.endpoint = 'https://' + f'{self.lang}.{self.family}.org/w/api.php'
        self.username = User_tables['username']
        self.password = User_tables['password']
        self.r3_token = ''
    #---
    def Log_to_wiki(self):
        #---
        SS["ss"] = requests.Session()
        printe.output( "new_api/page.py: Log_to_wiki %s," % self.endpoint  )
        #---
        r2_params = {
            'format': 'json',
            'action': 'login',
            'lgname': self.username,
            'lgpassword': self.password,
            'lgtoken' : ''
            }
        #---
        printe.output( "new_api/page.py: log to %s:%s. user:%s" % (self.lang, self.family, self.username )  )
        #---
        r1_params = { 'format': 'json', 'action': 'query', 'meta': 'tokens', 'type': 'login'}
        #---
        try:
            r11 = SS["ss"].post(self.endpoint, data=r1_params)
            r11.raise_for_status()
            r2_params['lgtoken'] = r11.json()['query']['tokens']['logintoken']
        except Exception as e:
            # WARNING: /data/project/himo/core/new_api/page.py:101: UserWarning: Exception:502 Server Error: Server Hangup for url: https://ar.wikipedia.org/w/api.php
            #---
            pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
            warn(warn_err('Exception:' + str(e)), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return False
        #---
        r22 = {}
        #---
        if r2_params['lgtoken'] != '':
            try:
                uu  = SS["ss"].post(self.endpoint, data=r2_params)
                r22 = uu.json()
            except Exception as e:
                pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
                warn(warn_err('Exception:' + str(e)), UserWarning)
                pywikibot.output( 'CRITICAL:' )
                return False
        #---
        if r22.get('login', {}).get('result', '') != 'Success':
            pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
            warn(warn_err('Exception:' + str(r22)), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return False
        else:
            printe.output(f'<<green>> {__file__} login Success')
        #---
        try:
            # get edit token
            r33 = SS["ss"].post(self.endpoint, data={'format': 'json', 'action': 'query', 'meta': 'tokens' })
            self.r3_token = r33.json()['query']['tokens']['csrftoken']
            SS['r3_token'] = self.r3_token
        except Exception as e:
            pywikibot.output( '<<lightred>> Traceback (most recent call last):' )
            warn(warn_err('Exception:' + str(e)), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return False
#---
Save_Edit_Pages = { 1 : False}
#---
change_codes = {
    "nb" : "no",
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
class MainPage():
    def __init__(self, title, lang):
        self.title = title
        #---
        self.lang = change_codes.get(lang) or lang
        #---
        self.family = 'wikipedia'
        self.endpoint = f'https://{lang}.wikipedia.org/w/api.php'
        #---
        self.Exists = ''
        self.is_redirect = ''
        self.flagged = ''
        self.can_be_edit = False
        #---
        self.wikibase_item = ""
        self.text = ""
        self.text_html = ""
        self.revid = ""
        self.pageid = ""
        self.timestamp = ""
        self.user = ""
        #---
        self.back_links = []
        self.links = []
        self.iwlinks = []
        self.links_here = []
        #---
        self.info = {'done':False}
        #---
        self.categories = {}
        self.hidden_categories = {}
        self.all_categories_with_hidden = {}
        #---
        self.langlinks = {}
        self.templates = {}

        self.r3_token = ''
        self.summary = ''
        self.words = 0
        self.length = 0
        self.ns = False
        self.newtext = ""
        #---
        if self.lang != "" and self.lang != wiki_loged.get("lang", False) :
            log = Login(self.lang)
            #---
            log.Log_to_wiki()
            #---
            self.r3_token = log.r3_token
        #---
    def post_new(self, params, Type='get', addtoken = False):
        #---
        params['format'] = 'json'
        params['utf8']   = 1
        params['bot']    = Bot_or_himo[1]
        params["maxlag"] = ar_lag[1]
        #---
        if addtoken:
            params["token"] = SS.get('r3_token') or self.r3_token
        #---
        if params.get("summary") and Main_User[1] == useraccount.hiacc :
            params["summary"] = ""
        #---
        if 'workibrahem' in sys.argv: params["summary"] = ""
        #---
        if params['action'] in ['query']:
            if "bot" in params: del params["bot"]
            if "summary" in params: del params["summary"]
        #---
        params["formatversion"] = params.get("formatversion") or "1"
        #---
        url = self.endpoint + '?' + urllib.parse.urlencode(params)
        if print_test[1]:   printe.output(url.replace('&format=json', ''))
        #---
        data = {}
        #---
        try:
            if Type=='post':
                response = SS["ss"].post(self.endpoint, data=params)
            else:
                response = SS["ss"].post(self.endpoint, data=params)
        except Exception as e:
            printe.output(e)
            return {}
        #---
        try:
            data = response.json()
        except Exception as e:
            printe.output(e)
        #---
        error = data.get("error",{})
        #---
        if error != {}:
            # printe.output(data)
            #---
            Invalid = error.get("info",'')
            code = error.get("code",'')
            #---
            # printe.output(Invalid)
            #---
            if Invalid == "Invalid CSRF token." :
                pywikibot.output('<<lightred>> ** error "Invalid CSRF token.". ')
                #---
                log = Login(self.lang)
                log.Log_to_wiki()
                self.r3_token = log.r3_token
                #---
                return self.post_new(params, Type=Type, addtoken=addtoken)
        #---
        if 'printdata' in sys.argv:
            # printe.output( json.dumps(data,ensure_ascii=False) )
            printe.output( data )
        #---
        return data
    #---
    def get_text(self, redirects=False):
        params = {
            "action": "query",
            "prop": "revisions|pageprops|flagged",
            "titles": self.title,
            "ppprop": "wikibase_item",              # pageprops
            "rvprop": "timestamp|content|user|ids", # revisions
            "rvslots": "*"                          # revisions
        }
        #---
        if redirects:    params["redirects"] = 1
        data = self.post_new(params)
        #---
        _dat_ = {"batchcomplete": "","query": {
                "normalized": [{"from": "وب:ملعب", "to": "ويكيبيديا:ملعب"}],
                "pages": {
                    "361534": {
                        "pageid": 361534,
                        "ns": 4,
                        "title": "ويكيبيديا:ملعب",
                        "revisions": [{
                            "revid": 61421668,
                            "parentid": 61421528,
                            "user": "Al-shazali Sabeel",
                            "timestamp": "2023-03-07T13:50:29Z",
                            "slots": {"main": {"contentmodel": "wikitext","contentformat": "text/x-wiki","*": "{{عنوان الملعب}}"}}
                        }],
                        "pageprops": {"wikibase_item": "Q3938" }
                    }
                }
        }}
        #---
        pages = data.get("query", {}).get("pages", {})
        #---
        for k, v in pages.items():
            #---
            if print_test[1] or 'printdata' in sys.argv: warn(warn_err('v:' + str(v)), UserWarning)
            #---
            if 'missing' in v :
                self.Exists = False
                break
            else:
                self.Exists = True
            #---
            title   = v["title"]
            #---
            pageprops = v.get("pageprops", {})
            self.wikibase_item   = pageprops.get("wikibase_item") or self.wikibase_item
            #---
            # "flagged": { "stable_revid": 61366100, "level": 0, "level_text": "stable"}
            self.flagged = v.get('flagged', False) != False
            #---
            self.ns      = v.get("ns") or self.ns
            self.pageid  = v.get("pageid") or self.pageid
            #---
            page = v.get("revisions", [{}])[0]
            #---
            self.text   = page.get("slots",{}).get("main",{}).get("*",'')
            self.user   = page.get("user")  or self.user
            self.revid  = page.get("revid") or self.revid
            #---
            self.timestamp = page.get("timestamp") or self.timestamp
            #---
            break
        #---
        return self.text

    def get_infos(self):
        #---
        params = {
            "action": "query",
            "titles": self.title,
            "prop": "categories|langlinks|templates|linkshere|iwlinks|info",
            "clprop": "sortkey|hidden",

            "cllimit": "max",       # categories
            "lllimit": "max",       # langlinks
            "tllimit": "max",       # templates
            "lhlimit": "max",       # linkshere
            "iwlimit": "max",       # iwlinks
            "formatversion": "2",
            # "normalize": 1,
            "tlnamespace": "10"
        }
        #---
        _data_ = {
            "continue": {},
            "query": {
                "pages": {
                    "9124097": {
                        "pageid": 9124097,
                        "ns": 0,
                        "title": "طواف العالم للدراجات 2023",
                        "categories": [],
                        "langlinks": [],
                        "templates": [{"ns": 10,"title": "قالب:-"}],
                        "linkshere": [{"pageid": 189150,"ns": 0,"title": "طواف فرنسا"}],
                        "iwlinks": [{"prefix": "commons","*": "Category:2023_UCI_World_Tour"}],
                        "contentmodel": "wikitext",
                        "pagelanguage": "ar",
                        "pagelanguagehtmlcode": "ar",
                        "pagelanguagedir": "rtl",
                        "touched": "2023-03-07T11:53:53Z",
                        "lastrevid": 61366100,
                        "length": 985
                    }
                }
            }
        }
        #---
        data = self.post_new(params)
        #---
        xs = {'batchcomplete': True, 'query': {'pages': [{'pageid': 151314, 'ns': 10, 'title': 'قالب:أوب',

        'categories': [
            {'ns': 14, 'title': 'تصنيف:قوالب تستخدم أنماط القوالب', 'sortkey': '', 'sortkeyprefix': '', 'hidden': False}, 
            {'ns': 14, 'title': 'تصنيف:cc', 'sortkey': 'v', 'sortkeyprefix': 'أوب', 'hidden': True}
            ],

        'langlinks': [{'lang': 'bh', 'title': 'टेम्पलेट:AWB'}], 

        'templates': [{'ns': 10, 'title': 'قالب:No redirect'}], 

        'linkshere': [{'pageid': 308641, 'ns': 10, 'title': 'قالب:AWB', 'redirect': True}], 

        'iwlinks': [{'prefix': 'd', 'title': 'Q4063270'}], 

        'contentmodel': 'wikitext', 'pagelanguage': 'ar', 'pagelanguagehtmlcode': 'ar', 'pagelanguagedir': 'rtl', 'touched': '2023-03-05T22:10:23Z', 'lastrevid': 61388266, 'length': 3477
        }
        ]}}
        #---
        ta = data.get("query", {}).get("pages", [{}])[0]
        #---
        #for _, ta in pages.items():
        #---
        self.ns     = ta.get('ns')        or self.ns
        self.pageid = ta.get('pageid')    or self.pageid
        self.length = ta.get('length')    or self.length
        self.revid  = ta.get('lastrevid') or self.revid
        #---
        self.is_redirect = True if 'redirect' in ta else False
        #---
        for cat in ta.get('categories', []):
            #---
            _cat_ = {"ns": 14,"title": "تصنيف:بوابة سباق الدراجات الهوائية/مقالات متعلقة","sortkey": "d8b7","sortkeyprefix": "","hidden": True  }
            #---
            if 'sortkey' in cat: del cat['sortkey']
            #---
            tit = cat["title"]
            #---
            self.all_categories_with_hidden[tit] = cat
            #---
            if cat.get('hidden') == True:
                self.hidden_categories[tit] = cat
            else:
                del cat['hidden']
                self.categories[tit] = cat
        #---
        if ta.get('langlinks', []) != []:
            #---
            # {"lang": "ca", "*": "UCI World Tour 2023"} or {'lang': 'bh', 'title': 'टेम्पलेट:AWB'}
            #---
            self.langlinks = { ta["lang"]: ta.get("*") or ta.get("title") for ta in ta.get('langlinks', []) }
        #---
        # "linkshere": [{"pageid": 189150,"ns": 0,"title": "طواف فرنسا"}, {"pageid": 308641,"ns": 10,"title": "قالب:AWB","redirect": ""}]
        self.links_here = ta.get('linkshere', [])
        #---
        self.iwlinks = ta.get('iwlinks', [])
        #---
        self.info['done'] = True

    def page_backlinks(self, ns=0):
        params = {
            "action": "query",
            "maxlag": "3",
            # "prop": "info",
            "generator": "backlinks",
            "redirects": 1,
            # 'gblfilterredir': 'redirects',
            "gbltitle":self.title,
            "gblnamespace": ns,
            "gbllimit": "max",
            "formatversion": "2",
            "gblredirect": 1
        }
        data = self.post_new(params)
        #---
        x = {
            'batchcomplete': True,
            'limits': {'backlinks': 2500},
            'query': {
                'redirects': [{'from': 'فريدريش زيمرمان','to': 'فريدريش تسيمرمان'}],
                'pages': [
                    {'pageid': 2941285,'ns': 0,'title': 'فولفغانغ شويبله'},
                    {'pageid': 4783977,'ns': 0,'title': 'وزارة الشؤون الرقمية والنقل'},
                    {'pageid': 5218323,'ns': 0,'title': 'فريدريش تسيمرمان'},
                    {'pageid': 6662649,'ns': 0,'title': 'غونتر كراوزه'}
                    ]
        }}
        #---
        pages = data.get("query", {}).get("pages", [])
        #---
        back_links = [ x for x in pages if x['title'] != self.title]
        #---
        self.back_links = back_links
        #---
        return self.back_links

    def page_links(self):
        params = {
            "action": "parse",
            "prop": "links",
            "formatversion": "2",
            "page": self.title
        }
        data = self.post_new(params)
        #---
        # [{'ns': 14, 'title': 'تصنيف:مقالات بحاجة لشريط بوابات', 'exists': True}, {'ns': 14, 'title': 'تصنيف:مقالات بحاجة لصندوق معلومات', 'exists': False}]
        #---
        self.links = data.get('parse', {}).get('links', [])
        #---
        return self.links

    def get_text_html(self):
        params = {
            "action": "parse",
            "page": self.title,
            "formatversion": "2",
            "prop": "text"
        }
        #---
        data = self.post_new(params)
        #---
        _data_ = {'warnings': {'main': {'warnings': 'Unrecognized parameter: bot.'}}, 'parse': {'title': 'ويكيبيديا:ملعب', 'pageid': 361534, 'text': ''}}
        #---
        self.text_html = data.get('parse', {}).get('text', '')
        #---
        return self.text_html

    def get_redirect_target(self):
        #---
        params = {
            "action": "query",
            "titles": self.title,
            "prop": "info",
            "redirects": 1
        }
        #---
        data = self.post_new(params)
        #---
        _pages_ = {'batchcomplete': '', 'query': {'redirects': [{'from': 'Yemen', 'to': 'اليمن'}], 'pages': {}, 'normalized': [{'from': 'yemen', 'to': 'Yemen'}] }}
        #---
        __redirects__ = {'from': 'Yemen', 'to': 'اليمن'}
        #---
        redirects = data.get("query", {}).get("redirects", [{}])[0]
        #---
        to = redirects.get("to", '')
        #---
        if to != '' :
            printe.output(f'<<lightyellow>>Page:{self.title} redirect to {to}')
        #---
        return to

    def get_words(self):
        srlimit = "30"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": self.title,
            "srlimit": srlimit,
        }
        data = self.post_new(params, addtoken = True)
        #---
        if data == {}: return 0
        #---
        search = data.get('query', {}).get('search', [])
        #---
        for pag in search:
            tit = pag["title"]
            count = pag["wordcount"]
            if tit == self.title:
                self.words = count
                break
        #---
        return self.words

    def purge(self):
        #---
        params = {
            "action": "purge",
            "forcelinkupdate": 1,
            "forcerecursivelinkupdate": 1,
            "titles": self.title
        }
        #---
        data = self.post_new(params, Type='post')
        #---
        if data == {}:
            printe.output('<<lightred>> ** purge error. ')
            return False
        #---
        title2 = self.title
        #---
        #  'normalized': [{'from': 'وب:ملعب', 'to': 'ويكيبيديا:ملعب'}]}
        #---
        for x in data.get('normalized', []):
            # printe.output(f"normalized from {x['from']} to {x['to']}")
            if x['from'] == self.title :
                title2 = x['to']
                break
        #---
        for t in data.get('purge', []):
            # t = [{'ns': 4, 'title': 'ويكيبيديا:ملعب', 'purged': '', 'linkupdate': ''}]
            ti = t['title']
            if title2 == ti and 'purged' in t:
                return True
            if "missing" in t:
                printe.output( 'page "%s" missing' % t['title'] )
                return "missing"
        return False

    def isRedirect(self):
        #---
        if self.is_redirect == '': self.get_infos()
        #---
        return self.is_redirect
    #---
    def get_categories(self, with_hidden=False):
        #---
        # if self.categories == {}: self.get_infos()
        if not self.info['done']: self.get_infos()
        #---
        if with_hidden:
            return self.all_categories_with_hidden
        #---
        return self.categories

    def get_hidden_categories(self):
        #---
        if self.categories == {} and self.hidden_categories == {} : self.get_infos()
        #---
        return self.hidden_categories

    def get_langlinks(self):
        #---
        if not self.info['done']: self.get_infos()
        #---
        return self.langlinks

    def get_links_here(self):
        #---
        if not self.info['done']: self.get_infos()
        #---
        return self.links_here

    def get_wiki_links_from_text(self):
        if self.text == '' : self.text = self.get_text()
        #---        
        parsed = wikitextparser.parse(self.text)
        wikilinks = parsed.wikilinks
        #---
        printe.output(f'wikilinks:{str(wikilinks)}')
        #---
        for x in wikilinks:
            print(x.title)
        #---
        return self.can_be_edit

    def Get_tags(self, tag=''):
        if self.text == '' : self.text = self.get_text()
        #---
        self.text = self.text.replace('<ref>', '<ref name="ss">', 1)
        #---
        parsed = wikitextparser.parse(self.text)
        tags = parsed.get_tags()
        #---
        # printe.output(f'tags:{str(tags)}')
        #---
        if tag == '':
            return tags
        #---
        new_tags = []
        #---
        for x in tags:
            if x.name == tag:
                new_tags.append(x)
        #---
        return new_tags

    def can_edit(self, script=''):
        if self.text == '' : self.text = self.get_text()
        #---
        self.can_be_edit = True#botEdit.botMayEdit( False, text= self.text, title_page=self.title, botjob=script)
        #---
        return self.can_be_edit

    def is_flagged(self):
        #---
        if self.text == '' : self.text = self.get_text()
        #---
        return self.flagged

    def get_timestamp(self):
        if self.timestamp == '' : self.get_text()
        return self.timestamp

    def exists(self):
        if self.Exists == '' : self.get_text()
        if not self.Exists:
            printe.output( f'page "{self.title}" not exists' )
        return self.Exists

    def namespace(self):
        if self.ns == False : self.get_text()
        return self.ns

    def get_user(self):
        if self.user == '' : self.get_text()
        return self.user

    def get_templates(self):
        if self.text == '' : self.text = self.get_text()
        self.templates = txtlib.extract_templates_and_params(self.text)
        return self.templates

    def ask_put(self, nodiff = False):
        yes_answer = [ "y", "a", "", "Y", "A", "all", "aaa" ]
        #---
        if 'ask' in sys.argv and not Save_Edit_Pages[1] or print_test[1]:
            #---
            if not "nodiff" in sys.argv and not nodiff:
                printe.showDiff(self.text, self.newtext)
            #---
            printe.output(Edit_summary_line[1] % self.summary )
            sa = pywikibot.input('<<lightyellow>>page.py: Do you want to accept these changes? (yes, no): for page %s:%s user:%s'  % (self.lang, self.title, User_tables['username'] ))
            #---
            if sa == "a":
                printe.output('<<lightgreen>> ---------------------------------' )
                printe.output(f'<<lightgreen>> {__file__} save all without asking.' )
                printe.output('<<lightgreen>> ---------------------------------' )
                Save_Edit_Pages[1] = True
            #---
            if not sa in yes_answer:
                printe.output( "wrong answer" )
                return False
        #---
        return True

    def handel_err(self, error, function):
        #---
        # {'error': {'code': 'articleexists', 'info': 'The article you tried to create has been created already.', '*': 'See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1425'}
        #---
        err_code = error.get('code', '')
        err_info = error.get('info', '')
        #---
        printe.output(f'<<lightred>>{function} ERROR: <<defaut>>code:{err_code}.')
        #---["protectedpage", 'تأخير البوتات 3 ساعات', False]
        if err_code == "abusefilter-disallowed":
            #---
            # oioioi = {'error': {'code': 'abusefilter-disallowed', 'info': 'This', 'abusefilter': {'id': '169', 'description': 'تأخير البوتات 3 ساعات', 'actions': ['disallow']}, '*': 'See https'}, 'servedby': 'mw1374'}
            #---
            abusefilter = error.get("abusefilter","")
            description = abusefilter.get('description','')
            printe.output('<<lightred>> ** abusefilter-disallowed: %s ' % description )
            if description == 'تأخير البوتات 3 ساعات' :
                return False
            return description
        #---
        if err_code == "protectedpage":
            printe.output('<<lightred>> ** protectedpage. ')
            # return "protectedpage"
            return False
        #---
        if err_code == "articleexists":
            printe.output('<<lightred>> ** article already created. ')
            return "articleexists"
        #---
        printe.output(f'<<lightred>>{function} ERROR: <<defaut>>info: {err_info}.')

    def save(self, newtext='', summary='', nocreate=1, minor='', tags='', nodiff = False):
        #---
        if minor == '' : minor = Bot_or_himo[1]
        #---
        self.newtext = newtext
        if summary != '':
            self.summary = summary
        #---
        ask = self.ask_put(nodiff=nodiff)
        if ask == False : return False
        #---
        params = {
            "action": "edit",
            "title": self.title,
            "text": newtext,
            "summary": self.summary,
            "minor": minor,
            "nocreate": nocreate,
        }
        #---
        if self.revid != '' : params['baserevid'] = self.revid
        #---
        if tags != "" :params["tags"] = tags
        #---
        # params['basetimestamp'] = self.timestamp
        #---
        pop = self.post_new(params, addtoken=True)
        #---
        if pop == {}: return False
        #---
        if 'Success' in str(pop):
            self.text = newtext
            self.user = ''
            printe.output('<<lightgreen>> ** true .. ' + '[[%s:%s:%s]] ' % (self.lang, self.family, self.title)  )
            printe.output( 'تم بنجاح... time.sleep() ')
            #---
            new_time_stamp = pop.get('edit',{}).get('newtimestamp','')
            if new_time_stamp != '':
                self.timestamp = new_time_stamp
            #---
            return True
        #---
        error = pop.get("error",{})
        #---
        if error != {}:
            er = self.handel_err(error, function='Save')
            #---
            return er
            #---
        return False

    def Create(self, text='', summary=''):
        #---
        self.newtext = text
        #---
        ask = self.ask_put()
        #---
        if ask == False : return False
        #---
        params = {
            "action": "edit",
            "title": self.title,
            "text": text,
            "summary": summary,
            "notminor": 1,
            "createonly": 1,
        }
        #---
        pop = self.post_new(params, addtoken=True)
        #---
        if pop == {}: return False
        #---
        error  = pop.get('error',{})
        edit   = pop.get('edit',{})
        result = edit.get('result','')
        #---
        if print_test[1] :
            print('pop:')
            print(pop)
        #---
        if result == 'Success':
            #---
            #{'edit': {'new': '', 'result': 'Success', 'pageid': 9090918, 'title': 'مستخدم:Mr. Ibrahem/test2024', 'contentmodel': 'wikitext', 'oldrevid': 0, 'newrevid': 61016221, 'newtimestamp': '2023-02-01T21:52:42Z'}}
            #---
            self.text = text
            #---
            printe.output('<<lightgreen>> ** true .. ' + '[[%s:%s:%s]] ' % (self.lang, self.family, self.title)  )
            printe.output( 'تم بنجاح... time.sleep() ')
            #---
            self.pageid = edit.get('pageid')   or self.pageid
            self.revid  = edit.get('newrevid') or self.revid
            self.timestamp = edit.get('newtimestamp') or self.timestamp
            #---
            return True
        #---
        if error != {}:
            er = self.handel_err(error, function='Create')
            #---
            return er
            #---
        return False
#---
def test():
    '''
    page      = MainPage(title, 'ar')
    exists    = page.exists()
    text      = page.get_text(redirects=False)
    timestamp = page.get_timestamp()
    user      = page.get_user()
    links     = page.page_links()
    words     = page.get_words()
    purge     = page.purge()
    templates = page.get_templates()
    save_page = page.save(newtext='', summary='', nocreate=1, minor='')
    create    = page.Create(text='', summary='')
    '''
    #---
    page = MainPage("فريدريش تسيمرمان", 'ar')
    #---
    # text = page.get_text()
    # print(xs)
    #---
    ex = page.page_backlinks()
    print(f'---------------------------')
    print(f'page_backlinks:{ex}')
    #---
    # hidden_categories= page.get_hidden_categories()
    # print(f'---------------------------')
    # print(f'hidden_categories:{hidden_categories}')
    #---
    # red = page.page_links()
    # print(f'page_links:{red}')
    #---
    # save = page.save(newtext='')
#---
if __name__ == '__main__':
    # python3 pwb.py new_api/page
    print_test[1] = True
    test()
#---