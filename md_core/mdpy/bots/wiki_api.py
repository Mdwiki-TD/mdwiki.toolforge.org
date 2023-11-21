#!/usr/bin/python3
"""
# ---
from mdpy.bots import wiki_api
# wiki_api.Get_page_qids(sitecode, titles)
# wiki_api.submitAPI( params, apiurl = 'https://' + 'www.wikidata.org/w/api.php', returnjson = False )
# wiki_api.submitAPI_token( params, apiurl = 'https://' + 'www.wikidata.org/w/api.php', returnjson = False )
# wiki_api.Find_pages_exists_or_not( liste, apiurl = 'https://' + 'or.wikipedia.org/w/api.php' )
# wiki_api.Getpageassessments_from_wikipedia( titles, site="en", find_redirects=False, pasubprojects=0 )
# wiki_api.get_page_views(titles, site='en', days = 30)
# wiki_api.get_views_with_rest_v1(langcode, titles, date_start='20040101', date_end='20300101', printurl=False, printstr=False)
# wiki_api.GetPageText(title, lang, redirects=False)
# wiki_api.get_langlinks(title, lang)
# wiki_api.
# wiki_api.
# ---
"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import traceback
import pywikibot
import sys
from warnings import warn
import urllib
import urllib.request
import urllib.parse
import requests

# ---
from pywikibot.comms import http
import pywikibot.data.api as apit
from mdpy import printe
from mdpy.bots import user_account_new

# ---
SS = {"token": ''}
session = {}
session[1] = requests.Session()
session["url"] = ""
# ---
Url_To_login = {1: '', 'not': True}
# ---
login_done = {1: False}
# ---
# ---

# ---
lgname = user_account_new.bot_username  # user_account_new.my_username
lgpassword = user_account_new.bot_password  # user_account_new.my_password      #user_account_new.mdwiki_pass


def log(api_urle):
    # ---
    if login_done[1] == api_urle or api_urle == '':
        return ''
    # ---
    # api_urle = 'https://' + 'www.wikidata.org/w/api.php'
    Url_To_login[1] = api_urle
    # ---
    session[1] = requests.Session()
    # ---
    # if api_urle != session["url"]: printe.output( "wiki_api.py: log to %s. user:%s" % (api_urle, username)  )
    # ---
    session["url"] = api_urle
    # ---
    # get login token
    r1 = session[1].get(
        api_urle,
        params={
            'format': 'json',
            'action': 'query',
            'meta': 'tokens',
            'type': 'login',
        },
    )
    r1.raise_for_status()
    # log in
    # passe = wd_password
    # ---
    r2 = session[1].post(
        api_urle,
        data={
            'format': 'json',
            'action': 'login',
            'lgname': lgname,
            'lgpassword': lgpassword,
            'lgtoken': r1.json()['query']['tokens']['logintoken'],
        },
    )
    # ---
    if r2.json()['login']['result'] != 'Success':
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(f'<<lightred>> {__file__} log():')
        warn('Exception:' + str(r2.json()), UserWarning)
        pywikibot.output('CRITICAL:')
    else:
        pywikibot.output(f"<<lightgreen>> mdwiki/mdpy/wiki_api.py: log to {api_urle} user:{lgname} Success... ")
    # ---
    # get edit token
    r3 = session[1].get(
        api_urle,
        params={
            'format': 'json',
            'action': 'query',
            'meta': 'tokens',
        },
    )
    # ---
    token = r3.json()['query']['tokens']['csrftoken']
    # ---
    login_done[1] = api_urle
    # ---
    session["token"] = token


def split_list_to_numbers(lise, numbs=100):
    # ---
    titles = {}
    DDone = []
    # ---
    num = 1
    # ---
    numbs2 = numbs - 1
    # ---
    for cc in lise:
        # ---
        if num not in titles:
            titles[num] = []
        # ---
        if len(titles[num]) < numbs:
            if cc not in DDone:
                titles[num].append(cc)
                DDone.append(cc)
                # ---
                if len(titles[num]) > numbs2:
                    num += 1
                # ---
    # ---
    return titles


def submitAPI_token(params, apiurl='', returnjson=False):
    # ---
    log(apiurl)
    # ---
    json1 = {}
    # ---
    params["token"] = session["token"]
    params["format"] = "json"
    # ---
    r4 = session[1].post(session["url"], data=params)
    # ---
    if returnjson:
        return r4
    # ---
    # if r4.text.find('</body></html>') == -1 : printe.output(r4.text)
    # ---
    try:
        json1 = json.loads(r4.text)
    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        return {}
    # ---
    # ---
    return json1


def submitAPI(params, apiurl='', returnjson=False):
    # ---
    log(apiurl)
    # ---
    encode_params = apit.encode_url(params)
    url = f'{apiurl}?{encode_params}'
    # ---
    if "printurl" in sys.argv:
        url2 = url.replace("&format=json", "").replace("?format=json", "?")
        printe.output('printboturl:\t\t' + url2)
    # ---
    json1 = {}
    # ---
    params["format"] = "json"
    # ---
    r4 = session[1].post(session["url"], data=params)
    # ---
    if returnjson:
        return r4
    # ---
    # if r4.text.find('</body></html>') == -1 : printe.output(r4.text)
    # ---
    try:
        json1 = json.loads(r4.text)
    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        return {}
    # ---
    return json1


def Find_pages_exists_or_not(liste, apiurl=''):
    # ---
    params = {
        "action": "query",
        "format": "json",
        "titles": '|'.join(liste),
        # "redirects": 0,
        # "prop": "templates|langlinks",
        "utf8": 1,
        "token": session["token"],
    }
    # ---
    table = {}
    # ---
    json1 = submitAPI(params, apiurl=apiurl)
    # ---
    if json1:
        query_pages = json1.get("query", {}).get("pages", {})
        for page in query_pages:
            kk = query_pages[page]
            faso = ''
            if "title" in kk:
                tit = kk.get("title", "")
                # ---
                if "missing" in kk:
                    table[tit] = False
                else:
                    table[tit] = True
        # ---
    return table


def get_langlinks(title, lang):
    # ---
    params = {
        "action": "query",
        "titles": title,
        "prop": "langlinks",
        "lllimit": "max",  # langlinks
        "formatversion": "2",
    }
    # ---
    ta = submitAPI(params, apiurl='https://' + lang + '.wikipedia.org/w/api.php')
    # ---
    if not ta:
        return {}
    # ---
    langlinks = {ta["lang"]: ta.get("*") or ta.get("title") for ta in ta.get('langlinks', [])}
    # ---
    return langlinks


def Get_page_qids(sitecode, titles, apiurl='', normalize=0):
    # ---
    if sitecode.endswith("wiki"):
        sitecode = sitecode[:-4]
    # ---
    if apiurl == '' and sitecode != "":
        apiurl = "https://" + sitecode + ".wikipedia.org/w/api.php"
    # ---
    if isinstance(titles, str):
        titles = [titles]
    # ---
    Main_table = {}
    # ---
    params = {
        "action": "query",
        "format": "json",
        # "prop": "langlinks|pageprops",
        # "titles": "|".join(titles),
        "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "utf8": 1,
        # "normalize": 1,
    }
    # ---
    if normalize == 1:
        params["normalize"] = 1
    # ---
    for i in range(0, len(titles), 50):
        # ---
        # group = dict(list(liste.items())[i:i+50])
        group = titles[i : i + 50]
        # ---
        params["titles"] = "|".join(group)
        # ---
        json1 = submitAPI(params, apiurl=apiurl)
        # ---
        if json1:
            js_query = json1.get('query', {})
            # ---
            for red in js_query.get('redirects', {}):
                # redirects_table[ red["from"] ] = red["to"]
                Main_table[red["from"]] = {'isRedirectPage': True, 'missing': True, 'from': red["from"], 'to': red["to"], 'title': red["from"], 'ns': '', 'q': ''}
            # ---
            for id in js_query.get('pages', {}):
                kk = js_query['pages'][id]
                faso = ''
                title = ""
                if "title" in kk:
                    title = kk["title"]
                    Main_table[title] = {}
                    if "missing" in kk:
                        Main_table[title]['missing'] = True
                    if "pageprops" in kk and kk["pageprops"].get("wikibase_item", "") != "":
                        Main_table[title]['q'] = kk["pageprops"].get("wikibase_item", "")
    # ---
    return Main_table


def Getpageassessments_from_wikipedia(titles, site="en", find_redirects=False, pasubprojects=0):
    # Tables = { "stub" : False }
    # ---
    if site.strip() == "":
        site = "en"
    # ---
    printe.output(f"Getpageassessments for \"{site}:{len(titles.split('|'))} pages.\"")
    Tables = {
        # "stub" : False ,
    }
    # ---
    params = {
        "action": "query",
        "format": "json",
        # "prop": "pageassessments|redirects",
        "prop": "pageassessments|templates",
        "redirects": 1,
        "titles": titles,
        "utf8": 1,
        "palimit": "max",
        "tlnamespace": "10",
        "tllimit": "max",
        # "pasubprojects": 1,
    }
    # ---
    langcode = "ar"
    # if pasubprojects == 1 : params["pasubprojects"] = 1
    # ---
    json1 = submitAPI(params, apiurl='https://' + site + '.wikipedia.org/w/api.php')
    # ---
    if not json1 or json1 == {}:
        return Tables
    # ---
    query = json1.get("query", {})
    # ---
    for xo, tayo in query.get('pages', {}).items():
        # ---
        if "title" in tayo:
            titley = tayo["title"]
        # ---
        Tables[titley] = tayo
        # ---
        if "missing" in tayo:
            printe.output(f"<<lightred>> page:{titley} is missing")
            Tables[titley] = {'missing': True}
    # ---
    redirects = query.get("redirects", [])
    if find_redirects and redirects:
        for red in redirects:
            if titles == red["from"]:
                Tables[titles] = {"is_redirect": True}
                break
    # ---
    return Tables


def GetPageText(title, lang, redirects=False):
    # printe.output( '**GetarPageText: ')
    # ---
    params = {
        "action": "parse",
        "format": "json",
        # "prop": "wikitext|sections",
        "prop": "wikitext",
        "page": title,
        # "redirects": 1,
        "utf8": 1,
        # "normalize": 1,
    }
    # ---
    if redirects:
        params["redirects"] = 1
    # ---
    text = ''
    json1 = submitAPI(params, apiurl='https://' + lang + '.wikipedia.org/w/api.php')
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


def _get_page_views_(titles, site='en', days=30):
    # ---
    if site.strip() == "":
        site = "en"
    # ---
    if site.endswith("wiki"):
        site = site[:-4]
    # ---
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageviews",
        "titles": titles,
        # "formatversion": "2",
        "redirects": 1,
        "pvipdays": str(days),
    }
    # ---
    maxn = 500 if '500' in sys.argv else 50
    # ---
    List = split_list_to_numbers(titles, numbs=maxn)
    # ---
    Main_table = {}
    # ---
    no_pv = []
    done = 0
    # ---
    for number, titles_1 in List.items():
        if len(titles_1) < 1:
            continue
        # ---
        printe.output('<<lightgreen>> views:%d, done:%d from %d titles.' % (len(Main_table.keys()), done, len(titles)))
        # ---
        params['titles'] = "|".join(titles_1)
        # ---
        json1 = submitAPI(params, apiurl='https://' + site + '.wikipedia.org/w/api.php')
        # ---
        if not json1 or json1 == {}:
            continue
        # ---
        js = json1.get('query', {})
        # ---
        redirects = {}
        # ---
        for red in js.get('redirects', []):
            redirects[red["from"]] = red["to"]
        # ---
        for key in js.get('pages', []):
            # ---
            kk = key
            # ---
            if isinstance(js.get('pages'), dict):
                kk = js['pages'][kk]
            # ---
            # {'pageid': 46133, 'ns': 0, 'title': 'Cardiomyopathy', 'pageviews': {'2022-11-14': 3076, '2022-11-15': 2114, '2022-11-16': 2895, '2022-11-17': 2616, '2022-11-18': 2247, '2022-11-19': 2303, '2022-11-20': 2152, '2022-11-21': 1752, '2022-11-22': 1617, '2022-11-23': 1595, '2022-11-24': 1520, '2022-11-25': 1534, '2022-11-26': 1611, '2022-11-27': 1702, '2022-11-28': 1457, '2022-11-29': 1362, '2022-11-30': 1517, '2022-12-01': 1689, '2022-12-02': 1510, '2022-12-03': 1588, '2022-12-04': 1678, '2022-12-05': 1449, '2022-12-06': 1578, '2022-12-07': 1411, '2022-12-08': 1495, '2022-12-09': 1732, '2022-12-10': 1553, '2022-12-11': 1702, '2022-12-12': 1472, '2022-12-13': 1333}}
            # ---
            title = kk['title']
            # ---
            title2 = redirects.get(title)
            # ---
            if title2:
                printe.output(f'page: {title} redirect to {title2}')
                title = title2
            # ---
            if "missing" in kk:
                Main_table[title] = 0
                continue
            # ---
            if 'pageviews' not in kk:
                no_pv.append(title)
                continue
            # ---
            pageviews = kk.get('pageviews', {})
            # ---
            all_views = 0
            # ---
            for date, views in pageviews.items():
                if isinstance(views, int):
                    all_views += views
            # ---
            Main_table[title] = all_views
        # ---
        done += len(titles_1)
        # ---
    # ---
    len_no_pv = len(no_pv)
    # ---
    printe.output(f'get_page_views: no_pv:{len_no_pv}')
    # ---
    return Main_table, no_pv


def get_page_views(titles, site='en', days=30):
    # ---
    numb = 0
    # ---
    views = {}
    # ---
    to_work = titles
    # ---
    while numb < 6 and to_work != []:
        views1, no_2 = _get_page_views_(to_work, site=site, days=days)
        to_work = no_2
        views = {**views, **views1}
    # ---
    return views


def get_views_with_rest_v1(langcode, titles, date_start='20150701', date_end='20300101', printurl=False, printstr=False, Type=''):
    # ---
    numbers = {}
    # ---
    _Type = 'monthly'
    # ---
    if Type in ["daily", "monthly"]:
        _Type = Type
    # ---
    numb = 0
    # ---
    for page in titles:
        # ---
        numb += 1
        # ---
        # print when numb % 100 == 0
        if numb % 100 == 0:
            print(f'get_views_with_rest_v1: {numb}/{len(titles)}')
        # ---
        if 'limit5' in sys.argv and numb > 5:
            break
        # ---
        pa = urllib.parse.quote(page)
        # ---
        url = 'https:' + '//wikimedia.org/api/rest_v1/metrics/pageviews/per-article/' + langcode + '.wikipedia/all-access/all-agents/' + pa.replace('/', '%2F') + '/' + _Type + '/' + date_start + '00/' + date_end + '00'
        # ---
        if "printurl" in sys.argv or printurl:
            printe.output('printboturl:\t\t' + url)
        # ---
        if printstr:
            printe.output('-------------------')
            printe.output('a %d/%d page:%s' % (numb, len(titles), page))
        # ---
        req = http.fetch(url)
        # req = requests.Session().get( url )
        # ---
        st = req.status_code
        # ---
        if 500 <= st < 600 or st == 404:
            printe.output(f'received {st} status from:')
            printe.output(url)
        # ---
        data = {}
        try:
            data = json.loads(req.text)
        except Exception:
            pywikibot.output('Traceback (most recent call last):')
            pywikibot.output(req.text)
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
        # ---
        if not data or data == {}:
            pywikibot.output(url)
        # ---
        sadasd = [{"project": "ar.wikipedia", "article": "نيلوتينيب", "granularity": "monthly", "timestamp": "2021070100", "access": "all-access", "agent": "all-agents", "views": 77}, {"project": "ar.wikipedia", "article": "نيلوتينيب", "granularity": "monthly", "timestamp": "2021080100", "access": "all-access", "agent": "all-agents", "views": 95}]
        # ---
        number_all = 0
        # ---
        tabl = {}
        # ---
        for x in data.get('items', []):
            # ---
            number_all += x["views"]
            # ---
            month = str(x["timestamp"])[:6]
            year = str(month)[:4]
            # ---
            if year not in tabl:
                tabl[year] = {'all': 0}
            # ---
            tabl[year]['all'] += x["views"]
            tabl[year][month] = x["views"]
            # ---
        # ---
        if number_all > 0:
            numbers[page] = {'all': number_all}
            # ---
            txt = f'all_views:{number_all}'
            # ---
            for year, y_tab in tabl.items():
                if y_tab.get('all', 0) > 0:
                    numbers[page][year] = y_tab
                    txt += f', {year}: {y_tab["all"]}'
            # ---
            if printstr:
                printe.output(txt)
            # ---
    # ---
    return numbers


# ---
if __name__ == '__main__':
    # get_views_with_rest_v1('ar', ['yemen', 'صنعاء'], date_start='20040101', date_end='20300101')
    get_views_with_rest_v1('ar', ['yemen', 'صنعاء'], date_start='20040101', date_end='20300101')
    ux = get_page_views(['yemen', 'صنعاء'], site='ar', days=30)
    printe.output(ux)
# ---
