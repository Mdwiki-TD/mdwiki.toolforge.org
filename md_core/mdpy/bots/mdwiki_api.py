#!/usr/bin/python3
"""

"""
#
# (C) Ibrahem Qasim, 2023
#
#
# ---
# import pywikibot
import sys
import traceback
import json
import time
import urllib
import pywikibot
import urllib.parse
import requests

from mdpy.bots import user_account_new
from mdpy import printe

# ---
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
'''
# ---
from mdpy.bots import mdwiki_api
# mdwiki_api.post(params)
# mdwiki_api.wordcount(title, srlimit='30')
# mdwiki_api.purge(title)
# mdwiki_api.page_put(oldtext='', newtext='', summary='', title='', returntrue=False, diff=True)
# mdwiki_api.create_Page(text, summary, title, ask, sleep=0, duplicate4="")
# mdwiki_api.Add_To_Bottom(appendtext, summary, title, ask)
# mdwiki_api.Add_To_Head(prependtext, summary, title, Ask)
# mdwiki_api.move(From, to, reason)
# mdwiki_api.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
# mdwiki_api.Get_UserContribs(user, limit="max", namespace="*", ucshow="")
# mdwiki_api.GetPageText(title)
# mdwiki_api.Get_All_pages(start, limit="max", namespace="*", apfilterredir='')
# mdwiki_api.Search(value="", ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# mdwiki_api.import_page(title)
# mdwiki_api.Get_page_links(title, namespace="*", limit="max")
# mdwiki_api.subcatquery(title, depth=0, ns="all", without_lang="", with_lang="", tempyes=[], limit=0)
# mdwiki_api.get_redirect(liste)
# mdwiki_api.
# mdwiki_api.
# ---
'''
# ---
maxlag = 3
ar_lag = {1: maxlag}
# ---

# ---
account = {
    'u': user_account_new.my_username,  # user_account_new.bot_username
    'p': user_account_new.mdwiki_pass,  # user_account_new.bot_password      #user_account_new.my_password
}
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
# ---
SS = {}
SS["ss"] = requests.Session()
SS["r3_token"] = ""
# ---
timesleep = 0
# ---
login_not_done = {1: True}


def py_input(s):
    # ---
    sa = pywikibot.input(s)
    # ---
    return sa


def get_status(req):
    try:
        st = req.status_code
        return st
    except Exception:
        pywikibot.output('<<lightred>> Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        st = req.status
        return st


def post_all(params, addtoken=False, **kwargs):
    # ---
    params["format"] = "json"
    params["utf8"] = 1
    # ---
    if addtoken:
        params["token"] = SS["r3_token"]
    # ---
    if 'printurl' in sys.argv:
        url = SS["url"] + '?' + urllib.parse.urlencode(params)
        print(url.replace('&format=json', ''))
    # ---
    r4 = False
    try:
        r4 = SS["ss"].post(SS["url"], data=params)
    except Exception:
        pywikibot.output('<<lightred>> Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        return {}
    # ---
    jsone = {}
    try:
        jsone = r4.json()
    except Exception as e:
        pywikibot.output('<<lightred>> Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output(r4.text)
        pywikibot.output('CRITICAL:')
        if 'Exception' in sys.argv:
            raise Exception(e)
        jsone = {}
    # ---
    if r4:
        status = get_status(r4)
        if status != 200:
            pywikibot.output(f" mdAPI: post_s error: {r4.text}")
            return {}
    # ---
    return jsone


def Log_to_wiki(family='mdwiki', lang="www"):
    # ---
    printe.output(f"mdwiki/mdpy/mdwiki_api.py: log to {lang}.{family}.org user:{account['u']}")
    SS["family"] = family
    SS["lang"] = lang
    SS["url"] = 'https://' + f'{lang}.{family}.org/w/api.php'
    SS["ss"] = requests.Session()
    # ---
    r1_params = {'format': 'json', 'action': 'query', 'meta': 'tokens', 'type': 'login'}
    # ---
    r22 = {}
    # if SS:
    try:
        r11 = SS["ss"].get(SS["url"], params=r1_params)
        r11.raise_for_status()
    except Exception:
        pywikibot.output('<<lightred>> Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        return False
    # ---
    r2_params = {'format': 'json', 'action': 'login', 'lgname': account['u'], 'lgpassword': account['p']}
    r2_params['lgtoken'] = r11.json()['query']['tokens']['logintoken']
    # ---
    r22 = post_all(r2_params)
    if r22:
        if r22['login']['result'] != 'Success':
            pywikibot.output(r22['login']['reason'])
        else:
            printe.output('mdwiki_api.py login Success')
    else:
        pywikibot.output('mdwiki_api.py login error')
        return False
    # ---
    # get edit token
    try:
        SS["r33"] = SS["ss"].get(
            SS["url"],
            params={
                'format': 'json',
                'action': 'query',
                'meta': 'tokens',
            },
        )
    except Exception as e:
        pywikibot.output(f"mdwiki_api.py: Log_to_wiki error: {e}")
        return False
    # ---
    SS["url"] = 'https://' + f'{lang}.{family}.org/w/api.php'
    # ---
    SS["r3_token"] = SS["r33"].json()['query']['tokens']['csrftoken']
    # ---
    login_not_done[1] = False


def post_s(params, addtoken=False, **kwargs):
    # ---
    if login_not_done[1]:
        Log_to_wiki("mdwiki", lang="www")
    # ---
    return post_all(params, addtoken=addtoken, **kwargs)


def post(p, **kwargs):
    return post_s(p, **kwargs)


def outbot(text2):
    text = {}
    # ---
    if isinstance(text2, dict):
        text = text2
    else:
        try:
            text = json.loads(text2)
        except BaseException:
            pywikibot.output("error when json loads text2")
    # ---{'error': {'*': 'See https://mdwiki.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes.', 'info': 'Invalid CSRF token.', 'code': 'badtoken'}}
    # {'error': {'info': 'Invalid CSRF token.', '*': 'See https://mdwiki.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes.', 'code': 'badtoken'}}
    # ---
    Invalid = ''
    if isinstance(text.get("error", {}), dict):
        Invalid = text.get("error", {}).get("info", '')
    # ---
    if Invalid == "Invalid CSRF token.":
        pywikibot.output('<<lightred>> ** error "Invalid CSRF token.". ')
        pywikibot.output(text)
        Log_to_wiki("mdwiki", lang="www")
    elif 'maxlag' in text:
        pywikibot.output('<<lightred>> maxlag: sleep for %d secound.' % 3)
        tabe = text.get("error", {}).get("lag", 0)
        lagese = int(tabe)
        if lagese != ar_lag[1]:
            ar_lag[1] = lagese + 1
            slee = ar_lag[1] / 4
            pywikibot.output('<<lightpurple>> maxlag:%d sleep for %d secound.' % (ar_lag[1], slee))
            time.sleep(slee)
        else:
            pywikibot.output('<<lightpurple>> lagese == ar_lag[1] (%d)' % ar_lag[1])
            time.sleep(3)
        # ---
    elif 'تأخير البوتات 3 ساعات' in text:
        pywikibot.output('<<lightred>> ** تأخير البوتات 3 ساعات. ')
        # ---
    elif 'error' in text:
        pywikibot.output('<<lightred>> ** error. ')
        pywikibot.output(text)
        # ---
        if 'code' in text['error']:
            if text['error']['code'] == "articleexists":
                pywikibot.output('<<lightred>> ** article already created. ')
                return "articleexists"
        else:
            pywikibot.output(text)
        # ---
    elif 'success' in text or 'Success' in text:
        pywikibot.output('<<lightgreen>> ** true. ')
    else:
        pywikibot.output(text2)


def import_history2(FILE_PATH, title):
    # ---
    printe.output(f'<<lightpurple>> import_history for page:{title}:')
    # ---
    if login_not_done[1]:
        Log_to_wiki("mdwiki", lang="www")
    # ---
    namespace = 0
    if title.lower().startswith('user:'):
        namespace = 2
    # ---
    pp = {
        "action": "import",
        # "xml": "...",
        "interwikiprefix": "user:",
        "fullhistory": 1,
        "namespace": namespace,
        # "assignknownusers": 1,
        "token": SS["r3_token"],
        "utf8": 1,
    }
    # ---
    NewList = []
    # ---
    if FILE_PATH and not isinstance(FILE_PATH, list):
        NewList.append(FILE_PATH)
    elif FILE_PATH and isinstance(FILE_PATH, list):
        NewList = FILE_PATH
    # ---
    for fff in NewList:
        printe.output(f' file:"{fff}"')
        FILE = {'xml': ('file.xml', open(fff))}
        # DATA = R.json()
        # print(DATA)
        r4 = SS["ss"].post(url=SS["url"], files=FILE, data=pp)
        # ---
        DATA = r4.json()
        printe.output(DATA)
        # ---
        if 'Success' in r4.text:
            printe.output('<<lightgreen>> ** true .. . ')
        # ---
        outbot(r4.text)


def import_history(FILE_PATH, title):
    # ---
    printe.output(f'<<lightpurple>> import_history for page:{title}:')
    # ---
    if login_not_done[1]:
        Log_to_wiki("mdwiki", lang="www")
    # ---
    namespace = 0
    if title.lower().startswith('user:'):
        namespace = 2
    # ---
    pparams = {
        "action": "import",
        "interwikisource": "wikipedia",
        "interwikipage": title,
        "token": SS["r3_token"],
        # "summary": "",
        "fullhistory": 1,
        "namespace": namespace,
    }
    # ---
    NewList = []
    # ---
    if FILE_PATH and not isinstance(FILE_PATH, list):
        NewList.append(FILE_PATH)
    elif FILE_PATH and isinstance(FILE_PATH, list):
        NewList = FILE_PATH
    # ---
    for fff in NewList:
        printe.output(f' file:"{fff}"')
        FILE = {'xml': ('file.xml', open(fff))}
        # DATA = R.json()
        # print(DATA)
        # ---
        try:
            r4 = SS["ss"].post(url=SS["url"], files=FILE, data=pparams)
            # ---
            if 'Success' in r4.text:
                printe.output('<<lightgreen>> ** true .. . ')
        except Exception:
            pywikibot.output('<<lightred>> Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
            r4 = {}
        # ---
        DATA = r4  # .json()
        printe.output(DATA)
        # ---
        # outbot(r4.text)


def import_page(title):
    params = {"action": "import", "format": "json", "interwikisource": "wikipedia", "interwikipage": title, "fullhistory": 1, "assignknownusers": 1}
    # ---
    r4 = post_s(params, addtoken=True)
    # ---
    outbot('import_page:')
    outbot(r4)
    # ---
    return r4


def page_put_new(NewText, summary, title, time_sleep="", family="", lang="", minor="", nocreate=1, tags="", returntrue=False, return_table=False):
    # ---
    printe.output(f' page_put {title}:')
    # ---
    pparams = {"action": "edit", "title": title, "text": NewText, "summary": summary, "nocreate": nocreate}
    # ---
    if sys.argv and "workibrahem" in sys.argv:
        pparams["summary"] = ""
    # ---
    if tags != "":
        pparams["tags"] = tags
    # ---
    tts = timesleep
    if time_sleep != "":
        tts = time_sleep
    # ---
    r4 = post_s(pparams, addtoken=True)
    # ---
    Invalid = ''
    if isinstance(r4.get("error", {}), dict):
        Invalid = r4.get("error", {}).get("info", '')
    # ---
    if 'Success' in str(r4):
        printe.output('<<lightgreen>> ** true .. ' + f'[[mdwiki:{title}]]   time.sleep({tts}) ')
        printe.output('Save True.. time.sleep(%d) ' % tts)
        time.sleep(tts)
        if return_table:
            return r4
        elif returntrue:
            return True
    # ---
    elif Invalid == "Invalid CSRF token.":
        printe.output('<<lightred>> ** error "Invalid CSRF token.". ')
        printe.output(r4)
        # ---
        Log_to_wiki("mdwiki", lang="www")
        # ---
        return page_put_new(NewText, summary, title, time_sleep=time_sleep, family=family, lang=lang, minor=minor, nocreate=nocreate, tags=tags, returntrue=returntrue)
    # ---
    else:
        outbot(r4)
        if returntrue:
            return False
        elif return_table:
            return {}


# ---
Save_2020 = {1: False}
Save_2040 = {1: False}


def page_put(oldtext='', newtext='', summary='', title='', time_sleep="", family="", lang="", minor="", nocreate=1, tags="", returntrue=False, diff=True):
    # ---
    if not Save_2020[1] and "ask" in sys.argv and "save" not in sys.argv:
        if diff:
            try:
                pywikibot.showDiff(oldtext, newtext)
            except BaseException:
                printe.output(' -mdwiki cant showDiff')
        printe.output(f' -Edit summary: {summary}:')
        sa = py_input(f"<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Do you want to accept these changes? ([y]es, [N]o, [a]ll): for page {lang}:{title}.org user:{account['u']}")
        # ---
        if sa == "a":
            printe.output('<<lightgreen>> ---------------------------------')
            printe.output('<<lightgreen>> mdwiki.py save all without asking.')
            printe.output('<<lightgreen>> ---------------------------------')
            Save_2020[1] = True
        # ---
        if sa not in yes_answer:
            printe.output("wrong answer")
            return False
    # ---
    return page_put_new(newtext, summary, title, time_sleep=time_sleep, family=family, lang=lang, minor=minor, nocreate=nocreate, tags=tags, returntrue=returntrue)


def Add_To_Bottom2(aptext, summary, title, poss="", family="", minor=""):
    if title.strip() != "":
        printe.output('** Add_To_Bottom2 .. ' + '[[' + title + ']] ')
        # pywikibot.showDiff("" , aptext)
        # ---
        Paramso = {
            "action": "edit",
            "title": title,
            "summary": summary,
            "notminor": 1,
            "nocreate": 1,
        }
        # ---
        if poss == "Head":
            Paramso["prependtext"] = aptext.strip() + "\n"
        else:
            Paramso["appendtext"] = "\n" + aptext.strip()
        # ---
        if sys.argv and "workibrahem" in sys.argv:
            Paramso["summary"] = ""
        # ---
        r4 = post_s(Paramso, addtoken=True)
        # ---
        if 'Success' in r4:
            printe.output(f"<<lightgreen>>** true .. {SS['family']} : [[{title}]] ")
            printe.output('Save True... time.sleep(%d) ' % timesleep)
        else:
            outbot(r4)
    else:
        printe.output('** Add_To_Bottom2 ..  title == ""')


def Add_To_Head(prependtext, summary, title, Ask, minor=""):
    if title.strip() != "":
        # ---
        printe.output(f' Add_To_Head for Page {title}:')
        # printe.output(prependtext)
        faso = False
        if Ask or "ask" in sys.argv and "save" not in sys.argv:
            # if Ask:
            # pywikibot.showDiff( "" , prependtext )
            sa = py_input(f'<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Add_To_Head of page "{title}" ? ([y]es, [N]o):')
            if sa in yes_answer:
                faso = True
                Add_To_Bottom2(prependtext, summary, title, poss="Head", minor=minor)
            else:
                printe.output("wrong answer")
            return sa
        else:
            faso = True
            Add_To_Bottom2(prependtext, summary, title, poss="Head", minor=minor)
        # ---
    else:
        printe.output('** Add_To_Head ..  title == ""')


def Add_To_Bottom(appendtext, summary, title, Ask, family="", minor=""):
    if title.strip() != "":
        # ---
        printe.output(f' Add_To_Bottom for Page {title}:')
        printe.output(appendtext)
        faso = False
        if Ask or "ask" in sys.argv and "save" not in sys.argv:
            # if Ask:
            sa = py_input(f'<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Add_To_Bottom of page "{title}" ? ([y]es, [N]o):')
            if sa in yes_answer:
                faso = True
                Add_To_Bottom2(appendtext, summary, title, family=family, minor=minor)
            else:
                printe.output("wrong answer")
            return sa
        else:
            faso = True
            Add_To_Bottom2(appendtext, summary, title, family=family, minor=minor)
        # ---
    else:
        printe.output('** Add_To_Bottom ..  title == ""')


def create_Page(text, summary, title, ask, sleep=0, family="", duplicate4="", minor="", printtext=True):
    printe.output(f' create Page {title}:')
    time_sleep = timesleep
    # ---
    if title.startswith("نقاش القالب:") and title.endswith("/ملعب"):
        printe.output(' skip make talk to sandboxes..')
        return False
    # ---
    if sleep != False:
        time_sleep = sleep
    # ---
    params = {
        "action": "edit",
        "title": title,
        "text": text,
        "summary": summary,
        "notminor": 1,
        "createonly": 1,
    }
    # ---
    if sys.argv and "workibrahem" in sys.argv:
        params["summary"] = "+"
    # ---
    sa = {"error": {"code": "articleexists", "info": "The article you tried to create has been created already.", "*": "See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes."}, "servedby": "mw1284"}
    Faco = False
    # ---
    if not Save_2040[1] and (ask or "ask" in sys.argv and "save" not in sys.argv):
        # if ask or "ask" in sys.argv and "save" not in sys.argv:
        # if ask:
        # pywikibot.showDiff("" , text)
        if printtext:
            printe.output("<<lightgreen>> " + text)
        printe.output(" summary: " + summary)
        sa = py_input(f"<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: create {family}:\"{title}\" page ? ([y]es, [N]o):user:{account['u']}")
        if sa.strip() in yes_answer:
            # ---
            if sa.strip() == "a":
                printe.output('<<lightgreen>> ---------------------------------------------')
                printe.output('<<lightgreen>> mdwiki.py create_Page save all without asking.')
                printe.output('<<lightgreen>> ---------------------------------------------')
                Save_2040[1] = True
            # ---
            r4 = post_s(params, addtoken=True)
            Faco = True
        else:
            printe.output("wrong answer")
            return False
    else:
        r4 = post_s(params)
        Faco = True
    # ---a
    if Faco:
        # ---
        if 'Success' in r4:
            printe.output(f'<<lightgreen>>** true .. : [[{title}]] ')
            printe.output(f'Save True... time.sleep({time_sleep}) ')
            time.sleep(time_sleep)
            return True
        elif 'error' in r4:
            if 'code' in r4['error']:
                if r4['error']['code'] == "articleexists":
                    printe.output("error when create_Page")
            outbot(r4)
        else:
            printe.output("create_Page: outbot(r4.text)")
            outbot(r4)
            return False
    # ---a
    printe.output(f"<<lightred>> end of create_Page def return False title:({title})")
    printe.output(r4)
    # ---a
    return False


def move(From, to, reason, lang='ar', nosleep=False):
    # ---
    printe.output(f'<<lightyellow>> ** move .. [[{lang}:{From}]] to [[{to}]] ')
    Params = {
        "action": "move",
        "from": From,
        "to": to,
        "movetalk": 1,
    }
    # ---
    printe.output(f' -Edit reason: {reason}:')
    # ---
    if From == to:
        printe.output(f'<<lightred>>** From == to {to} ')
        return False
    # ---
    JustMove = True
    # ---
    if not Save_2020[1] and "ask" in sys.argv:
        sa = py_input(f"<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Do you move page:[[{lang}:{From}]] to [[{to}]]? ([y]es, [N]o, [a]ll): user:{account['u']}")
        # ---
        if sa == "a":
            printe.output('<<lightgreen>> ---------------------------------')
            printe.output('<<lightgreen>> mdwiki.py move all without asking.')
            printe.output('<<lightgreen>> ---------------------------------')
            Save_2020[1] = True
        # ---
        if sa not in yes_answer:
            JustMove = False
            printe.output(' mdwiki/mdpy/mdwiki_api.py: wrong answer')
        # return sa
    # ---
    if JustMove:
        r4 = post_s(Params, addtoken=True)
        # ---
        if 'Success' in r4.text or "redirectcreated" in r4.text:
            printe.output('<<lightgreen>>** true .. ' + '[[' + to + ']] ')
            printe.output('Save True... time.sleep(%d) ' % 7)
            if nosleep:
                time.sleep(7)
            return True
        elif "Please wait some time and try again" in r4.text or "ratelimited" in r4.text:
            printe.output(r4.text)
            if nosleep:
                time.sleep(7)
            return move(From, to, reason, lang=lang)
        elif "Please choose another name." in r4.text:
            printe.output(r4.text)
            return "Please choose another name."
        else:
            return outbot(r4.text)
            # printe.output(r4.text)
    return False


def wordcount(title, srlimit='30'):
    # srlimit = "30"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "srlimit": srlimit,
        "format": "json",
    }
    data = post_s(params)
    # ---
    if not data or data == {}:
        return 0
    # ---
    search = data.get('query', {}).get('search', [])
    # ---
    words = 0
    # ---
    for pag in search:
        tit = pag["title"]
        count = pag["wordcount"]
        if tit == title:
            words = count
            break
    # ---
    return words


def Get_cat(enlink, ns, lllang="", tempyes=[], lang_no='', print_url=True):
    # ---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    # ---
    # printe.output(' Get_cat for %s' % (enlink) )
    # ---
    if not enlink.startswith('Category:'):
        enlink = 'Category:' + enlink
    # ---
    params = {
        "action": "query",
        "generator": "categorymembers",
        "gcmtitle": enlink,
        "gcmprop": "title",
        "gcmtype": "page|subcat",
        "gcmlimit": "max",
        "redirects": 1,
        # "prop": "templates",
        # "tllimit": "max",
        # "lllang": langcode,
        # "lllimit": "max",
    }
    # ---
    # if "tempapi" not in sys.argv :
    # params["prop"] = "templates"
    # params["tllimit"] = "max"
    # ---
    if tempyes != []:
        params["prop"] = "templates"
        params["tllimit"] = "max"
        params["tltemplates"] = "|".join(tempyes)
    # ---
    if lllang != "" or lang_no:  # مع وصلة لغة معينة
        params["prop"] = params["prop"] + "|langlinks"
        # params["lllang"] = lllang
        params["lllimit"] = "max"
    # ---all
    if ns == "0" or ns == "10":
        params["gcmtype"] = "page"
    elif ns == "14":
        params["gcmtype"] = "subcat"
    elif ns == "all":
        params["gcmtype"] = "page|subcat"
    # ---
    # printe.output('<<lightblue>> API_CALLS %d   for %s' % (API_CALLS[1],enlink) )
    # ---
    if print_url or "printurl" in sys.argv:
        lis = [f"{x}={y}" for x, y in params.items()]
        url = "api.php?" + "&".join(lis)
        printe.output(url)
    # ----
    continue_p = ''
    continue_v = 'x'
    # ---
    table = {}
    # ----
    while continue_v != '':
        # ---
        if continue_v != 'x':
            params[continue_p] = continue_v
        # ---
        continue_v = ''
        # ---
        api = post_s(params)
        # ---
        if not api:
            break
        # ---
        continue_d = api.get("continue", {})
        for p, v in continue_d.items():
            if p == 'continue':
                continue
            continue_v = v
            continue_p = p
        # ----
        pages = api.get("query", {}).get("pages", {})
        # ----
        for category in pages:
            # ---
            caca = category
            # ---
            if isinstance(pages, dict):
                caca = pages[category]
            # ---
            cate_title = caca["title"]
            tablese = {}
            # printe.output("<<lightblue>> cate_title: %s" % cate_title )
            # ---
            if "ns" in caca:
                tablese['ns'] = caca['ns']
                # printe.output("<<lightblue>> ns: %s" %   caca['ns'])
            # ---
            if 'templates' in caca:
                tablese['templates'] = [x['title'] for x in caca['templates']]
            # ---
            if 'langlinks' in caca:
                tablese['langlinks'] = {}
                for fo in caca['langlinks']:
                    result = fo['*']
                    tablese['langlinks'][fo['lang']] = fo['*']
            # ---
            table[cate_title] = tablese
            # ---
    # ---
    subcats = [x for x in table if str(table[x]['ns']) == "14"]
    # ---
    printe.output(f"<<lightgreen>> Getcat: find {len(subcats)} subcat:{','.join(subcats)}")
    # ---
    printe.output(f'<<lightyellow>> cat:{enlink} has:{len(table)} pages.')
    # ---
    return table


def subcatquery(title, depth=0, ns="all", limit=0, test=False, without_lang="", with_lang="", tempyes=[]):
    # ---
    # ---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    # ---
    # printe.output('<<lightyellow>> catdepth.py sub cat query for %s:%s,depth:%d,ns:%s.' % ('',title,depth,ns) )
    # ---
    start = time.time()
    final = time.time()
    # ---
    if not title.strip().startswith('Category:'):
        title = 'Category:' + title.strip()
    # ---
    tablemember = Get_cat(title, ns, tempyes=tempyes, lang_no=without_lang, lllang=with_lang, print_url=False)
    # ---
    result_table = {}
    # ---
    for x in tablemember:
        # ---
        vaild = True
        # ---
        # البحث عن وصلة لغة غير مرغوب بوجودها
        if without_lang and without_lang != "":
            no_langs = tablemember[x].get('langlinks', {}).get(without_lang, '')
            if no_langs and no_langs != "":
                vaild = False
        # ---
        # البحث عن وصلة لغة مرغوب بوجودها
        if with_lang and with_lang != "":
            langs = tablemember[x].get('langlinks', {}).get(with_lang, '')
            if langs != "":
                vaild = True
            else:
                vaild = False
        # ---
        if vaild:
            result_table[x] = tablemember[x]
    # ---
    cat_done = []
    # ---
    new_list = [x for x in tablemember if int(tablemember[x]["ns"]) == 14]
    # ---
    depth_done = 0
    # ---
    if not isinstance(depth, int):
        try:
            depth = int(depth)
        except BaseException:
            printe.output('<<lightblue>> type(depth) != int ')
    # ---
    while depth > depth_done:  # and ( limit > 0 and len(result_table) < limit ):
        depth_done += 1
        new_tab2 = []
        # ---
        for cat in new_list:
            # ---
            printe.output(f'get pages from subcat:{cat}')
            # ---
            if cat not in cat_done:
                cat_done.append(cat)
                table2 = Get_cat(cat, ns)
                for x in table2:
                    # ---
                    if int(table2[x]["ns"]) == 14:
                        new_tab2.append(x)
                    # ---
                    vaild = True
                    # ---
                    # البحث عن وصلة لغة غير مرغوب بوجودها
                    if without_lang and without_lang != "":
                        no_langs = table2[x].get('langlinks', {}).get(without_lang, '')
                        if no_langs and no_langs != "":
                            vaild = False
                    # ---
                    # البحث عن وصلة لغة مرغوب بوجودها
                    if with_lang and with_lang != "":
                        langs = table2[x].get('langlinks', {}).get(with_lang, '')
                        if langs != "":
                            vaild = True
                        else:
                            vaild = False
                    # ---
                    if vaild:
                        result_table[x] = table2[x]
                    # ---
        new_list = new_tab2
    # ---
    final = time.time()
    delta = int(final - start)
    # ---
    # if "printresult" in sys.argv: printe.output(result_table)
    # ---
    printe.output('<<lightblue>>catdepth.py: find %d pages(%s) in %s:%s, depth:%d in %d seconds' % (len(result_table), str(ns), '', title, depth, delta))
    # ---
    result_tab = list(result_table.keys())
    # ---
    result_tab = [x for x in result_tab if valid_title(x)]
    # ---
    # return result_table
    return result_tab


def GetPageText(title, redirects=False):
    # printe.output( '**GetarPageText: ')
    # ---
    params = {
        "action": "parse",
        # "prop": "wikitext|sections",
        "prop": "wikitext",
        "page": title,
        # "redirects": 1,
        # "normalize": 1,
    }
    # ---
    if redirects:
        params["redirects"] = 1
    # ---
    text = ''
    json1 = post_s(params)
    if json1:
        text = json1.get('parse', {}).get('wikitext', {}).get('*', '')
    else:
        printe.output('no parse in json1:')
        printe.output(json1)
    # ---
    if text == "":
        printe.output(f'page {title} text == "".')
    # ---
    return text


def Get_Newpages(limit="max", namespace="0", rcstart="", user=''):
    # ---
    params = {
        "action": "query",
        "list": "recentchanges",
        # "rcdir": "newer",
        "rcnamespace": namespace,
        "rclimit": limit,
        "rctype": "new",
    }
    # ---
    if rcstart != "":
        params["rcstart"] = rcstart
    if user != "":
        params["rcuser"] = user
    # ---
    json1 = post_s(params)
    # ---
    Main_table = []
    # ---
    if not json1 or json1 == {}:
        return []
    # ---
    newp = json1.get("query", {}).get("recentchanges", {})
    # ---
    ccc = {"type": "new", "ns": 0, "title": "تشارلز مسيون ريمي", "pageid": 7004776, "revid": 41370093, "old_revid": 0, "rcid": 215347464, "timestamp": "2019-12-15T13:14:34Z"}
    # ---
    Main_table = [x["title"] for x in newp]
    # ---
    return Main_table


def Get_page_links(title, namespace="0", limit="max"):
    # ---
    printe.output(f'Get_page_links for title:"{title}", limit:"{limit}",namespace:"{namespace}"')
    # ---
    params = {
        "action": "query",
        "prop": "links",
        "titles": title,
        "plnamespace": namespace,
        "pllimit": limit,
        "converttitles": 1,
    }
    # ---
    # if apfilterredir in [ 'redirects' , 'all' , 'nonredirects' ] : params['apfilterredir'] = apfilterredir
    # ---
    json1 = post_s(params)
    # ---
    Main_table = {
        'links': {},
        'normalized': [],
        'redirects': [],
    }
    # ---
    if json1:
        # ---
        query = json1.get("query", {})
        Main_table['normalized'] = query.get("normalized", [])
        Main_table['redirects'] = query.get("redirects", [])
        # ---
        pages = query.get("pages", {})
        # ---
        for page in pages:
            tab = pages[page]
            for pa in tab.get('links', []):
                Main_table['links'][pa["title"]] = {'ns': pa["ns"], 'title': pa["title"]}
    else:
        printe.output("mdwiki_api.py no json1")
    # ---
    printe.output(f"mdwiki_api.py Get_page_links : find {len(Main_table['links'])} pages.")
    # ---
    return Main_table


def Get_page_links_2(title):
    Main_table = Get_page_links(title)
    lista = Main_table.get('links', {}).keys()
    return lista


def Get_template_pages(title, namespace="*", limit="max"):
    # ---
    printe.output(f'Get_template_pages for template:"{title}", limit:"{limit}",namespace:"{namespace}"')
    # ---
    params = {"action": "query", "prop": "info", "titles": title, "generator": "transcludedin", "gtinamespace": namespace, "gtilimit": limit}
    # ---
    Main_table = []
    gticontinue = 'x'
    # ---
    while gticontinue != '':
        # ---
        if gticontinue != 'x':
            params['gticontinue'] = gticontinue
        # ---
        json1 = post_s(params)
        # ---
        if not json1:
            break
        # ---
        gticontinue = json1.get("continue", {}).get("gticontinue", '')
        # ---
        pages = json1.get("query", {}).get("pages", {})
        # ---
        for _, tab in pages.items():
            Main_table.append(tab["title"])
        # ---
        printe.output(f'len of Main_table:{len(Main_table)}.')
        # ---
    # ---
    printe.output(f"mdwiki_api.py Get_template_pages : find {len(Main_table)} pages.")
    # ---
    return Main_table


def Get_All_pages(start, namespace="0", limit="max", apfilterredir='', limit_all=0):
    # ---
    printe.output(f'Get_All_pages for start:{start}, limit:{limit},namespace:{namespace},apfilterredir:{apfilterredir}')
    # ---
    numb = 0
    # ---
    params = {
        "action": "query",
        "list": "allpages",
        # "apfrom": start,
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
        json1 = post_s(params)
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
    printe.output(f"mdwiki_api.py Get_All_pages : find {len(Main_table)} pages.")
    # ---
    return Main_table


def get_section(title, level):
    printe.output(f'get_section title:"{title}", level:"{level}"')
    # ---
    params = {"action": "parse", "page": title, "prop": "wikitext", "section": level}
    # ---
    json1 = post_s(params)
    # ---
    if not json1 or json1 == {}:
        return ""
    # ---
    text = json1.get("parse", {}).get("wikitext", {}).get("*", '')
    # ---
    return text


def Get_UserContribs(user, limit="max", namespace="*", ucshow=""):
    # ---
    printe.output(f'Get_UserContribs for user:"{user}", limit:"{limit}"')
    # ---
    params = {
        "action": "query",
        "list": "usercontribs",
        "ucdir": "older",
        "ucnamespace": namespace,
        "uclimit": limit,
        "ucuser": user,
        "ucprop": "title"
        # "ucshow": "new"
    }
    # ---
    if ucshow != "":
        params["ucshow"] = ucshow
    # ---
    json1 = post_s(params)
    # ---
    Main_table = []
    # ---
    if json1:
        newp = json1.get("query", {}).get("usercontribs", {})
        # ---
        Main_table = [x["title"] for x in newp]
    # ---
    printe.output(f"mdwiki_api.py Get_Newpages : find {len(Main_table)} pages.")
    # ---
    return Main_table


def Search(value="", lang="", family='', ns="", offset='', srlimit="max", RETURN_dict=False, addparams={}):
    # ---
    Lidy = []
    # ---
    printe.output(f'mdwiki_api.Search for "{value}",ns:{ns}')
    # ---
    if srlimit == "":
        srlimit = "max"
    # ---
    # srlimit = "max"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": value,
        "srnamespace": 0,
        "srlimit": srlimit,
    }
    # ---
    nsvalue = ns
    # ---
    if nsvalue == "":
        for arg in sys.argv:
            arg, _, value = arg.partition(':')
            # ---
            if arg == "-ns":
                nsvalue = value
    # ---
    if addparams != {}:
        for pp in addparams:
            params[pp] = addparams[pp]
    # ---
    if nsvalue != "":
        params["srnamespace"] = nsvalue
    # ---
    if offset != "":
        params["sroffset"] = offset
    # ---
    json1 = post_s(params, addtoken=True)
    if "query" in json1 and "search" in json1['query']:
        for pag in json1['query']['search']:
            tit = pag["title"]
            if RETURN_dict:
                Lidy.append(pag)
            else:
                Lidy.append(tit)
    # ---
    # if Lidy == []:
    printe.output(f'mdwiki_api.Search find "{len(Lidy)}" result. s')
    # ---
    return Lidy


def get_redirect(liste):
    # ---
    redirects = {}
    # ---
    for i in range(0, len(liste), 50):
        titles = liste[i : i + 50]
        # ---
        params = {
            "action": "query",
            "format": "json",
            "titles": '|'.join(titles),
            "redirects": 1,
            # "prop": "templates|langlinks",
            "utf8": 1,
            # "normalize": 1,
        }
        # ---
        json1 = post_s(params)
        # ---
        if json1:
            redd = json1.get("query", {}).get("redirects", [])
            for red in redd:
                redirects[red["from"]] = red["to"]
    # ---
    return redirects


def Find_pages_exists_or_not(liste):
    # ---
    normalized = {}
    table = {}
    # ---
    for i in range(0, len(liste), 50):
        titles = liste[i : i + 50]
        # ---
        params = {
            "action": "query",
            "titles": "|".join(titles),
            # "redirects": 0,
            # "normalize": 1,
        }
        # ---
        json1 = post_s(params)
        # ---
        if not json1 or json1 == {}:
            return table
        # ---
        query = json1.get("query", {})
        normalz = query.get("normalized", {})
        # ---
        for red in normalz:
            normalized[red["to"]] = red["from"]
        # ---
        query_pages = query.get("pages", {})
        # ---
        for _, kk in query_pages.items():
            tit = kk.get("title", "")
            if tit != "":
                tit = normalized.get(tit, tit)
                # ---
                table[tit] = True
                # ---
                if "missing" in kk:
                    table[tit] = False
    # ---
    return table


# ---
# end of mdwiki.py file
# ---
if __name__ == '__main__':
    Get_All_pages('', namespace=14)
# ---
