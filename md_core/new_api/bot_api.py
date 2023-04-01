
'''
from newapi.page import NEW_API
# api_new = NEW_API('ar', family='wikipedia')
# login   = api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
'''
#---
import pywikibot
from new_api import printe
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
def login_def(lang, family) :{}
#---
class NEW_API():
    def __init__(self, lang, family='wikipedia'):
        #---
        self.lang = change_codes.get(lang) or lang
        #---
        self.family = family
        self.endpoint = f'https://{lang}.{family}.org/w/api.php'
        #---
        self.log = login_def(self.lang, family=self.family)
        
    def Login_to_wiki(self):
        #---
        self.log.Log_to_wiki()
    
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

    def Find_pages_exists_or_not(self, liste):
        #---
        normalized = {}
        table = {}
        #---
        done = 0
        #---
        missing = 0
        exists = 0
        #---
        for i in range(0, len(liste), 50):
            titles = liste[i:i+50]
            #---
            done += len(titles)
            #---
            pywikibot.output(f"Find_pages_exists_or_not : {done}/{len(liste)}")
            #---
            params = { "action": "query", "titles": "|".join(titles) }
            #---
            json1 = self.log.post(params)
            #---
            if not json1 or json1 == {}:
                pywikibot.output("<<lightred>> error when Find_pages_exists_or_not")
                return table
            #---
            query = json1.get("query", {})
            normalz = query.get("normalized", {})
            #---
            for red in normalz: normalized[red["to"]] = red["from"]
            #---
            query_pages = query.get("pages", {})
            #---
            for _, kk in query_pages.items():
                tit = kk.get("title", "")
                if tit != "":
                    tit = normalized.get(tit, tit)
                    #---
                    table[tit] = True
                    #---
                    if "missing" in kk: 
                        table[tit] = False
                        missing += 1
                    else:
                        exists += 1
        #---
        pywikibot.output(f"Find_pages_exists_or_not : missing:{missing}, exists: {exists}")
        #---
        return table
    #---
#---