'''
from newapi.page import NEW_API
# api_new  = NEW_API('ar', family='wikipedia')
# login    = api_new.Login_to_wiki()
# pages    = api_new.Find_pages_exists_or_not(liste)
# json1    = api_new.post_params(params)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# search   = api_new.Search(value, ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
'''
#---
'''
from newapi.page import NEW_API
#---
login_done_lang = {1:''}
#---
# في بعض البوتات التي يتم ادخال اللغة من خلال وظائف معينة
#---
if login_done_lang[1] != code:
    login_done_lang[1] = code
    api_new = NEW_API(code, family='wikipedia')
    api_new.Login_to_wiki()
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

    def post_params(self, params):
        return self.log.post(params)
    
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
            params = { "action": "query", "titles": "|".join(titles), "formatversion" : 2 }
            #---
            json1 = self.post_params(params)
            #---
            if not json1 or json1 == {}:
                pywikibot.output("<<lightred>> error when Find_pages_exists_or_not")
                return table
            #---
            query = json1.get("query", {})
            normalz = query.get("normalized", [])
            #---
            for red in normalz: normalized[red["to"]] = red["from"]
            #---
            query_pages = query.get("pages", [])
            #---
            for kk in query_pages:
                #---
                if type(query_pages) == dict: kk = query_pages[kk]
                #---
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
    def Get_All_pages(self, start='', namespace="0", limit="max", apfilterredir='', limit_all=0):
        #---
        pywikibot.output(f'Get_All_pages for start:{start}, limit:{limit},namespace:{namespace},apfilterredir:{apfilterredir}')
        #---
        numb = 0
        #---
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "apnamespace": namespace,
            "aplimit": limit,
            "apfilterredir": "nonredirects",
        }
        #---
        if apfilterredir in ['redirects', 'all', 'nonredirects']: params['apfilterredir'] = apfilterredir
        #---
        if start != '' : params['apfrom'] = start
        #---
        apcontinue = 'x'
        #---
        Main_table = []
        #---
        while apcontinue != '':
            #---
            numb += 1
            #---
            pywikibot.output(f'Get_All_pages {numb}, apcontinue:{apcontinue}..')
            #---
            if apcontinue != 'x' : params['apcontinue'] = apcontinue
            #---
            json1 = self.post_params(params)
            #---
            if not json1 or json1 == {}: break
            #---
            apcontinue = json1.get( "continue" , {} ).get( "apcontinue" , '' )
            #---
            newp = json1.get("query", {}).get("allpages", [])
            pywikibot.output( "<<lightpurple>> --- Get_All_pages : find %d pages." % len(newp) )
            #---
            for x in newp:
                if not x[ "title" ] in Main_table : 
                    Main_table.append(x["title"])
            #---
            pywikibot.output( "len of Main_table %d." % len(Main_table) )
            #---
            if limit_all > 0 and len(Main_table) > limit_all : 
                apcontinue = '' 
                pywikibot.output( "<<lightgreen>> limit_all > len(Main_table) " )
                break
            #---
        #---
        if numb > 0 and apcontinue == '' : 
            pywikibot.output( "<<lightgreen>> apcontinue == '' " )
        #---
        pywikibot.output( "bot_api.py Get_All_pages : find %d pages." % len(Main_table) )
        #---
        return Main_table
    #---
    def Search(self, valu, ns="*", offset='', srlimit="max", RETURN_dict=False, addparams={}):
        #---
        results = []
        #---
        pywikibot.output( 'bot_api.Search for "%s",ns:%s' % (valu, ns) )
        #---
        if srlimit == "":   srlimit = "max"
        #---
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": valu,
            "srnamespace": 0,
            "srlimit": srlimit,
        }
        #---
        if addparams != {} :
            for pp, vv in addparams.items():
                if vv != '':    params[pp] = vv
        #---
        if ns != "" :  params["srnamespace"] = ns
        #---
        if offset != "" :   params["sroffset"] = offset
        #---
        json1 = self.post_params(params)
        #---
        if not json1 or json1 == {}:
            pywikibot.output("<<lightred>> error when Find_pages_exists_or_not")
            return results
        #---
        search = json1.get("query", {}).get("search", [])
        #---
        for pag in search:
            if RETURN_dict:
                results.append( pag )
            else:
                results.append( pag["title"] )
        #---
        pywikibot.output( 'bot_api.Search find "%d" result. s' % len(results) )
        #---
        return results
    #---
    def Get_Newpages(self, limit="max", namespace="0", rcstart="", user=''):
        #---
        rccontinue = "x"
        #---
        params = {
            "action": "query",
            "format": "json",
            "list": "recentchanges",
            #"rcdir": "newer",
            "rcnamespace": namespace,
            "rclimit": limit,
            "utf8": 1,
            "rctype": "new"
        }
        #---
        if rcstart != "" :  params["rcstart"] = rcstart
        if user != "" :     params["rcuser"] = user
        #---
        Main_table = []
        #---
        numb = 0
        #---
        while rccontinue != '':
            #---
            numb += 1
            #---
            pywikibot.output(f'Get_All_pages {numb}, rccontinue:{rccontinue}..')
            #---
            if rccontinue != 'x' : params['rccontinue'] = rccontinue
            #---
            json1 = self.post_params(params)
            #---
            if not json1 or json1 == {}:    return Main_table
            #---
            newp = json1.get("query", {}).get("recentchanges", {})
            #---
            rccontinue = json1.get("continue", {}).get( "rccontinue", '')
            #---
            ccc = { 
                "type": "new", "ns": 0, "title": "تشارلز مسيون ريمي", "pageid": 7004776, 
                "revid": 41370093, "old_revid": 0, "rcid": 215347464, "timestamp": "2019-12-15T13:14:34Z"
                }
            #---
            Main_table.extend( [ x[ "title" ] for x in newp ] )
        #---
        pywikibot.output( 'bot_api.Get_Newpages find "%d" result. s' % len(Main_table) )
        #---
        return Main_table
    #---
#---