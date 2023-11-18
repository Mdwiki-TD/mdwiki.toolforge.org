'''
from newapi.page import NEW_API
# api_new  = NEW_API('ar', family='wikipedia')
# login    = api_new.Login_to_wiki()
# pages    = api_new.Find_pages_exists_or_not(liste)
# json1    = api_new.post_params(params)
# pages    = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# search   = api_new.Search(value='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# newpages = api_new.Get_Newpages(limit="max", namespace="0", rcstart="", user='', three_houers=False)
# usercont = api_new.UserContribs(user, limit=5000, namespace="*", ucshow="")
# l_links  = api_new.Get_langlinks_for_list(titles, targtsitecode="", numbes=50)
# text_w   = api_new.expandtemplates(text)
# subst    = api_new.Prase_Text('{{subst:page_name}}', title)
'''
# ---
'''
from newapi.page import NEW_API
# ---
login_done_lang = {1:''}
# ---
# في بعض البوتات التي يتم ادخال اللغة من خلال وظائف معينة
# ---
if login_done_lang[1] != code:
    login_done_lang[1] = code
    api_new = NEW_API(code, family='wikipedia')
    api_new.Login_to_wiki()
'''
# ---
# ---
import pywikibot
import datetime
from datetime import timedelta
if __file__.find('mdwiki') == -1:
    from API import printe
else:
    from new_api import printe
# ---
change_codes = {
    "nb": "no",
    "bat_smg": "bat-smg",
    "be_x_old": "be-tarask",
    "be-x-old": "be-tarask",
    "cbk_zam": "cbk-zam",
    "fiu_vro": "fiu-vro",
    "map_bms": "map-bms",
    "nds_nl": "nds-nl",
    "roa_rup": "roa-rup",
    "zh_classical": "zh-classical",
    "zh_min_nan": "zh-min-nan",
    "zh_yue": "zh-yue",
}


def login_def(lang, family):
    return {}


# ---


class NEW_API:

    def __init__(self, lang, family='wikipedia'):
        # ---
        self.lang = change_codes.get(lang) or lang
        # ---
        self.family = family
        self.endpoint = f'https://{lang}.{family}.org/w/api.php'
        # ---
        self.log = login_def(self.lang, family=self.family)

    def Login_to_wiki(self):
        # ---
        self.log.Log_to_wiki()

    def handel_err(self, error, function):
        # ---
        # {'error': {'code': 'articleexists', 'info': 'The article you tried to create has been created already.', '*': 'See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1425'}
        # ---
        err_code = error.get('code', '')
        err_info = error.get('info', '')
        # ---
        printe.output(f'<<lightred>>{function} ERROR: <<defaut>>code:{err_code}.')
        # ---["protectedpage", 'تأخير البوتات 3 ساعات', False]
        if err_code == "abusefilter-disallowed":
            # ---
            # oioioi = {'error': {'code': 'abusefilter-disallowed', 'info': 'This', 'abusefilter': {'id': '169', 'description': 'تأخير البوتات 3 ساعات', 'actions': ['disallow']}, '*': 'See https'}, 'servedby': 'mw1374'}
            # ---
            abusefilter = error.get("abusefilter", "")
            description = abusefilter.get('description', '')
            printe.output(f'<<lightred>> ** abusefilter-disallowed: {description} ')
            if description in ['تأخير البوتات 3 ساعات', 'تأخير البوتات 3 ساعات- 3 من 3', 'تأخير البوتات 3 ساعات- 1 من 3', 'تأخير البوتات 3 ساعات- 2 من 3']:
                return False
            return description
        # ---
        if err_code == "protectedpage":
            printe.output('<<lightred>> ** protectedpage. ')
            # return "protectedpage"
            return False
        # ---
        if err_code == "articleexists":
            printe.output('<<lightred>> ** article already created. ')
            return "articleexists"
        # ---
        printe.output(f'<<lightred>>{function} ERROR: <<defaut>>info: {err_info}.')

    def post_params(self, params):
        return self.log.post(params)

    def post_continue(self, params, action, _p_, p_empty, Max=50000):
        # ---
        if not isinstance(Max, int) and Max.isdigit():
            Max = int(Max)
        # ---
        continue_params = {}
        # ---
        results = p_empty
        # ---
        while continue_params != {} or len(results) == 0:
            # ---
            if continue_params:
                params = {
                    **params,
                    **continue_params
                }
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1 or json1 == {}:
                break
            # ---
            continue_params = json1.get("continue", {})
            # ---
            data = json1.get(action, {}).get(_p_, p_empty)
            # ---
            if not data:
                break
            # ---
            printe.output(f'post_continue, len:{len(data)}, all: {len(results)}')
            # ---
            if Max <= len(results) and len(results) > 1:
                break
            # ---
            if isinstance(results, list):
                results.extend(data)
            else:
                results = {
                    **results,
                    **data
                }
        # ---
        return results

    def Find_pages_exists_or_not(self, liste):
        # ---
        normalized = {}
        table = {}
        # ---
        done = 0
        # ---
        missing = 0
        exists = 0
        # ---
        for i in range(0, len(liste), 50):
            titles = liste[i:i + 50]
            # ---
            done += len(titles)
            # ---
            printe.output(f"Find_pages_exists_or_not : {done}/{len(liste)}")
            # ---
            params = {
                "action": "query",
                "titles": "|".join(titles),
                "formatversion": 2
            }
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1 or json1 == {}:
                printe.output("<<lightred>> error when Find_pages_exists_or_not")
                return table
            # ---
            query = json1.get("query", {})
            normalz = query.get("normalized", [])
            # ---
            for red in normalz:
                normalized[red["to"]] = red["from"]
            # ---
            query_pages = query.get("pages", [])
            # ---
            for kk in query_pages:
                # ---
                if isinstance(query_pages, dict):
                    kk = query_pages[kk]
                # ---
                tit = kk.get("title", "")
                if tit != "":
                    tit = normalized.get(tit, tit)
                    # ---
                    table[tit] = True
                    # ---
                    if "missing" in kk:
                        table[tit] = False
                        missing += 1
                    else:
                        exists += 1
        # ---
        printe.output(f"Find_pages_exists_or_not : missing:{missing}, exists: {exists}")
        # ---
        return table


    def Get_All_pages(self, start='', namespace="0", limit="max", apfilterredir='', limit_all=0):
        # ---
        printe.output(f'Get_All_pages for start:{start}, limit:{limit},namespace:{namespace},apfilterredir:{apfilterredir}')
        # ---
        numb = 0
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "allpages",
            "apnamespace": namespace,
            "aplimit": limit,
            "apfilterredir": "nonredirects",
        }
        # ---
        if apfilterredir in ['redirects', 'all', 'nonredirects']:
            params['apfilterredir'] = apfilterredir
        # ---
        if start != '':
            params['apfrom'] = start
        # ---
        apcontinue = 'x'
        # ---
        Main_table = []
        # ---
        while apcontinue != '':
            # ---
            numb += 1
            # ---
            printe.output(f'Get_All_pages {numb}, apcontinue:{apcontinue}..')
            # ---
            if apcontinue != 'x':
                params['apcontinue'] = apcontinue
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1 or json1 == {}:
                break
            # ---
            apcontinue = json1.get("continue", {}).get("apcontinue", '')
            # ---
            newp = json1.get("query", {}).get("allpages", [])
            printe.output(f"<<lightpurple>> --- Get_All_pages : find {len(newp)} pages.")
            # ---
            for x in newp:
                if x["title"] not in Main_table:
                    Main_table.append(x["title"])
            # ---
            printe.output(f"len of Main_table {len(Main_table)}.")
            # ---
            if limit_all > 0 and len(Main_table) > limit_all:
                apcontinue = ''
                printe.output("<<lightgreen>> limit_all > len(Main_table) ")
                break
            # ---
        # ---
        if numb > 0 and apcontinue == '':
            printe.output("<<lightgreen>> apcontinue == '' ")
        # ---
        printe.output(f"bot_api.py Get_All_pages : find {len(Main_table)} pages.")
        # ---
        return Main_table


    def Search(self, value='', ns="*", offset='', srlimit="max", RETURN_dict=False, addparams={}):
        # ---
        printe.output(f'bot_api.Search for "{value}",ns:{ns}')
        # ---
        if srlimit == "":
            srlimit = "max"
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": value,
            "srnamespace": 0,
            "srlimit": srlimit,
        }
        # ---
        if addparams != {}:
            for pp, vv in addparams.items():
                if vv != '':
                    params[pp] = vv
        # ---
        if ns != "":
            params["srnamespace"] = ns
        # ---
        if offset != "":
            params["sroffset"] = offset
        # ---
        search = self.post_continue(params, "query", "search", [])
        # ---
        results = []
        # ---
        for pag in search:
            if RETURN_dict:
                results.append(pag)
            else:
                results.append(pag["title"])
        # ---
        printe.output(f'bot_api.Search find "{len(search)}" all result: {len(results)}')
        # ---
        return results


    def Get_Newpages(self, limit=5000, namespace="0", rcstart="", user='', three_houers=False):
        # ---
        if three_houers:
            dd = datetime.datetime.utcnow() - timedelta(hours=3)
            # ---
            rcstart = dd.strftime('%Y-%m-%dT%H:%M:00.000Z')
            # ---
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "recentchanges",
            # "rcdir": "newer",
            "rcnamespace": namespace,
            "rclimit": 'max',
            "utf8": 1,
            "rctype": "new"
        }
        # ---
        if rcstart != "":
            params["rcstart"] = rcstart
        if user != "":
            params["rcuser"] = user
        # ---
        Main_table = []
        # ---
        numb = 0
        # ---
        if limit.isdigit():
            limit = int(limit)
            params['rclimit'] = limit
        else:
            limit = 5000
        # ---
        rccontinue = "x"
        # ---
        while rccontinue != '':
            # ---
            numb += 1
            # ---
            printe.output(f'Get_All_pages {numb}, rccontinue:{rccontinue}, all :{len(Main_table)}..')
            # ---
            if rccontinue != 'x':
                params['rccontinue'] = rccontinue
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1 or json1 == {}:
                break
            # ---
            newp = json1.get("query", {}).get("recentchanges", {})
            # ---
            rccontinue = json1.get("continue", {}).get("rccontinue", '')
            # ---
            ccc = {
                "type": "new",
                "ns": 0,
                "title": "تشارلز مسيون ريمي",
                "pageid": 7004776,
                "revid": 41370093,
                "old_revid": 0,
                "rcid": 215347464,
                "timestamp": "2019-12-15T13:14:34Z"
            }
            # ---
            Main_table.extend([x["title"] for x in newp])
            # ---
            if limit <= len(Main_table) and len(Main_table) > 1:
                break
            # ---
        # ---
        printe.output(f'bot_api.Get_Newpages find "{len(Main_table)}" result. s')
        # ---
        if three_houers:
            arsite = pywikibot.Site('ar', "wikipedia")
            # ---
            Main_table = [pywikibot.Page(arsite, x) for x in Main_table]
            # ---
        # ---
        return Main_table


    def UserContribs(self, user, limit=5000, namespace="*", ucshow=""):
        # ---
        params = {
            "action": "query",
            "format": "json",
            "list": "usercontribs",
            "ucdir": "older",
            "ucnamespace": namespace,
            "uclimit": "max",
            "ucuser": user,
            "utf8": 1,
            "bot": 1,
            "ucprop": "title"
        }
        # ---
        if ucshow != "":
            params["ucshow"] = ucshow
        # ---
        results = self.post_continue(params, "query", "usercontribs", [], Max=limit)
        # ---
        results = [x["title"] for x in results]
        # ---
        return results


    def Get_langlinks_for_list(self, titles, targtsitecode="", numbes=50):
        # ---
        printe.output(f'bot_api.Get_langlinks_for_list for "{len(titles)} pages"')
        # ---
        if targtsitecode.endswith("wiki"):
            targtsitecode = targtsitecode[:-4]
        # ---
        if self.lang != 'ar':
            numbes = 100
        # ---
        find_targtsitecode = 0
        # ---
        normalized = {}
        # ---
        table = {}
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "langlinks",
            # "redirects": 1,
            'lllimit': "max",
            "utf8": 1,
            # "normalize": 1
        }
        # ---
        if targtsitecode != "":
            params["lllang"] = targtsitecode
            printe.output(f'params["lllang"] = {targtsitecode}')
        # ---
        for i in range(0, len(titles), numbes):
            titles_1 = titles[i:i + numbes]
            # ---
            params["titles"] = "|".join(titles_1)
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1 or json1 == {}:
                continue
            # ---
            norma = json1.get("query", {}).get("normalized", {})
            for red in norma:
                normalized[red["to"]] = red["from"]
            # ---
            query_pages = json1.get("query", {}).get("pages", {})
            for page, kk in query_pages.items():
                if "title" in kk:
                    titlle = kk.get("title", "")
                    titlle = normalized.get(titlle, titlle)
                    # ---
                    table[titlle] = {}
                    # ---
                    for lang in kk.get('langlinks', []):
                        table[titlle][lang['lang']] = lang['*']
                        # ---
                        if lang['lang'] == targtsitecode:
                            find_targtsitecode += 1
                    # ---
        # ---
        printe.output('bot_api.Get_langlinks_for_list find "%d" in table,find_targtsitecode:%s:%d' % (len(table), targtsitecode, find_targtsitecode))
        # ---
        return table


    def expandtemplates(self, text):
        # ---
        params = {
            "action": "expandtemplates",
            "format": "json",
            "text": text,
            "prop": "wikitext",
            "formatversion": "2"
        }
        # ---
        data = self.post_params(params)
        # ---
        if not data or data == {}:
            return text
        # ---
        newtext = data.get("expandtemplates", {}).get("wikitext") or text
        # ---
        return newtext


    def Prase_Text(self, line, title):
        # ---
        params = {
            "action": "parse",
            "prop": "wikitext",
            "text": line,
            "title": title,
            "pst": 1,
            "contentmodel": "wikitext",
            "utf8": 1,
            "formatversion": "2"
        }
        # ---
        _data_ = {
            "parse": {
                "title": "كريس فروم",
                "pageid": 2639244,
                "wikitext": "{{subst:user:Mr._Ibrahem/line2|Q76|P31}}",
                "psttext": "\"Q76\":{\n\"P31\":\"إنسان\"\n\n\n\n\n},"
            }
        }
        # ---
        data = self.post_params(params)
        # ---
        if not data or data == {}:
            return ""
        # ---
        textnew = data.get("parse", {}).get("psttext", "")
        # ---
        textnew = textnew.replace("\\n\\n", "")
        # ---
        return textnew


    def get_extlinks(self, title):
        params = {
            "action": "query",
            "format": "json",
            "prop": "extlinks",
            "titles": title,
            "formatversion": "2",
            "utf8": 1,
            "ellimit": "max"
        }
        # ---
        continue_params = {}
        # ---
        results = []
        # ---
        while continue_params != {} or results == []:
            # ---
            if continue_params:
                params = {
                    **params,
                    **continue_params
                }
            # ---
            json1 = self.post_params(params)
            # ---
            if not json1 or json1 == {}:
                break
            # ---
            continue_params = json1.get("continue", {})
            # ---
            elcontinue = json1.get('continue', {}).get('elcontinue', '')
            # ---
            linkso = json1.get('query', {}).get('pages', [{}])[0].get('extlinks', [])
            # ---
            results.extend(linkso)
        # ---
        links = [x['url'] for x in results]
        # ---
        # remove duplicates
        liste1 = sorted(set(links))
        # ---
        # ---
        return liste1


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
        # ---
        results = self.post_continue(params, "query", "pages", [])
        # ---
        return results
        # ---
