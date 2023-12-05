#!/usr/bin/python3
"""

بوت للعمل على ويكيبيانات أو ويكيبيديا

"""
#
# (C) Ibrahem Qasim, 2022
#
#
# ---

import traceback

# import pywikibot
import re
import urllib
import json
import sys

# ---
import pywikibot

# ---
from datetime import datetime

# ---
menet = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
# ---
from mdpy import printe
from mdpy.bots import py_tools

# ---
'''
# ---
from mdpy.bots import wikidataapi
# wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php" )
# wikidataapi.post( params , apiurl = "https://www.wikidata.org/w/api.php" )
# wikidataapi.Get_sitelinks_From_Qid( q )
# wikidataapi.WD_Merge( q1, q2)
# wikidataapi.Labels_API(Qid, label, lang, remove = False)
# wikidataapi.sparql_generator_url(quary, printq = False, add_date = True)
# wikidataapi.wbsearchentities(search, language)
# wikidataapi.Claim_API_qid(qid, property, numeric)
# wikidataapi.Claim_API_str(qid, property, string)
# wikidataapi.
# wikidataapi.
# ---
'''
# ---
import requests

# ---
from mdpy.bots import user_account_new

# ---
username = user_account_new.bot_username  # user_account_new.my_username
password = user_account_new.bot_password  # user_account_new.my_password      #user_account_new.mdwiki_pass
# ---
if 'workhimo' in sys.argv:
    username = user_account_new.my_username
    password = user_account_new.my_password
# ---
yes_answer = ["y", "a", "", "Y", "A", "all"]
# ---
SS = {}
r1_params = {
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
}
r2_params = {
    # fz'assert': 'user',
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
}
# ---
SS["ss"] = requests.Session()
# ---
timesleep = 0
# ---
login_not_done = {1: True}


def Log_to_wiki(url=''):
    # ---
    if not login_not_done[1]:
        return ''
    # ---
    printe.output(f"wikidataapi.py: log to {url} user:{r2_params['lgname']}")
    SS["url"] = url
    SS["ss"] = requests.Session()
    # ---
    if SS:
        # try:
        r11 = SS["ss"].get(SS["url"], params=r1_params)
        r11.raise_for_status()
        # except:
        # printe.output( "wikidataapi.py: Can't log in . ")
        # log in
        r2_params['lgtoken'] = r11.json()['query']['tokens']['logintoken']
        r22 = SS["ss"].post(SS["url"], data=r2_params)
    # except:
    else:
        printe.output("wikidataapi.py: Can't log in . ")
        return False
    # ---
    if r22.json()['login']['result'] != 'Success':
        printe.output(r22.json()['login']['reason'])
        # raise RuntimeError(r22.json()['login']['reason'])
    else:
        printe.output('wikidataapi.py login Success')
    # ---
    # get edit token
    SS["r33"] = SS["ss"].get(
        SS["url"],
        params={
            'format': 'json',
            'action': 'query',
            'meta': 'tokens',
        },
    )
    # ---
    SS["url"] = url
    # ---
    SS["r3_token"] = SS["r33"].json()['query']['tokens']['csrftoken']
    # ---
    # printe.output( ' r3_token:%s' % SS["r3_token"] )
    # ---
    login_not_done[1] = False


def get_status(req):
    try:
        st = req.status_code
        return st
    except BaseException:
        st = req.status
        return st


def post(params, apiurl='', token=True):
    # ---
    Log_to_wiki(url=apiurl)
    # ---
    # r4 = SS["ss"].post(SS["url"], data = params )
    # post to API without error handling
    # ---
    if token:
        params["token"] = SS["r3_token"]
    # ---
    params["format"] = "json"
    # ---
    jsone = {}
    try:
        r4 = SS["ss"].post(SS["url"], data=params)
        jsone = r4.json()
    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output(params)
        pywikibot.output('CRITICAL:')
        return {}
    # ---
    status = get_status(r4)
    if status != 200:
        pywikibot.output(f"<<lightred>> wikidataapi.py: post error status: {str(status)}")
        return {}
    # ---
    return jsone


def post_to_qs(data):
    menet = datetime.now().strftime("%Y-%b-%d %H:%M:%S")
    # ---
    r2 = requests.Session().post(
        'https://quickstatements.toolforge.org/api.php',
        data={
            'format': 'v1',
            'action': 'import',  # create
            # 'type': 'item',
            'compress': 1,
            'submit': 1,
            'batchname': menet,
            'username': "Mr. Ibrahem",
            'token': user_account_new.qs_token,
            'data': data,
        },
    )
    # ---
    if not r2 or r2 == {}:
        return False
    # ---
    print("QS_New_API: " + str(r2.text))
    # ---
    return r2.json()


def QS_New_API(data2):
    # ---
    CREATE = 'CREATE||'
    for ss in data2.get("sitelinks", {}):
        dd = data2.get("sitelinks", {})
        tit = dd[ss]["title"]
        wik = dd[ss]["site"]
        wik2 = dd[ss]["site"].replace("wiki", "")
        CREATE += f'LAST|S{wik}|"{tit}"||'
        CREATE += f'LAST|L{wik2}|"{tit}"||'
    # ---
    claims = data2.get("claims", {})
    for Claim in claims:
        for P in claims[Claim]:
            value = P['mainsnak']["datavalue"].get("value", {}).get("id", "")
            # value = P["datavalue"].get("value",{}).get("id","")
            if value != "":
                CREATE += f"LAST|{P['mainsnak']['property']}|{value}||"
    # ---
    CREATE = CREATE + "XX"
    CREATE = CREATE.replace("||XX", "")
    # ---
    return post_to_qs(CREATE)


def Get_sitelinks_From_Qid(q):
    params = {
        "action": "wbgetentities",
        "format": "json",
        "props": "sitelinks",
        "ids": q,
        "utf8": 1,
    }
    # ---
    table = {"sitelinks": {}, "q": ""}
    # ---
    json1 = post(params, apiurl="https://www.wikidata.org/w/api.php")
    # ---
    if json1:
        if 'success' in json1 and json1['success'] == 1:
            if 'entities' in json1:
                if "-1" not in json1['entities']:
                    qli = [x for x in json1['entities'].keys()]
                    q2 = qli[0]
                    # ---
                    if q2 in json1['entities']:
                        table['q'] = q2
                        ppe = json1['entities'][q2]
                        # ---
                        if 'sitelinks' in ppe:
                            for site in ppe['sitelinks'].keys():
                                fsai = ppe['sitelinks'][site]
                                table['sitelinks'][fsai['site']] = fsai['title']
                        # ---
        else:
            return {}
    # ---
    return table


def WD_Merge(q1, q2):
    # ---
    q11 = re.sub(r'Q', '', q1)
    q22 = re.sub(r'Q', '', q2)
    # ---
    if q11.isdigit() and q22.isdigit():
        # ---
        if int(q11) > int(q22):
            From = q1
            To = q2
        else:
            From = q2
            To = q1
    else:
        From = q2
        To = q1
    # ---
    printe.output(f'from {From} to {To} ')
    # ---
    params = {
        "action": "wbmergeitems",
        "fromid": From,
        "toid": To,
        "ignoreconflicts": "description",
        "summary": "",
    }
    # ---
    r4 = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
    # ---
    if not r4:
        return False
    # ---
    if 'success' in r4:
        if '"redirected":1' in r4:
            printe.output('<<lightgreen>> ** true .. redirected.')
            return True
        else:
            printe.output('<<lightgreen>> ** true.')
            # ---
            pams2 = {"action": "wbcreateredirect", "from": From, "to": To, "ignoreconflicts": "description", "summary": ""}
            # ---
            r5 = post(pams2, apiurl="https://www.wikidata.org/w/api.php", token=True)
            # ---
            if 'success' in r5:
                printe.output('<<lightgreen>> **createredirect true.')
                return True
            else:
                printe.output('<<lightred>> r5' + str(r5))
    else:
        printe.output('<<lightred>> r4' + str(r4))
        return False


def Labels_API(Qid, label, lang, remove=False):
    # ---
    if Qid == '':
        printe.output("Labels_API Qid == '' ")
        return False
    # ---
    if label == "" and not remove:
        printe.output("Labels_API label == '' and remove = False ")
        return False
    # ---
    # save the edit
    out = f'{Qid} label:"{lang}"@{label}.'
    # ---
    params = {
        "action": "wbsetlabel",
        "id": Qid,
        "language": lang,
        "value": label,
    }
    # ---
    req = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
    # ---
    if req:
        text = str(req)
        if ('using the same description text' in text) and ('associated with language code' in text):
            item2 = re.search(r'(Q\d+)', str(req["error"]['info'])).group(1)
            printe.output('<<lightred>>API: same label item: ' + item2)
            # ---
            # outbot(text, fi = out, NoWait = nowait)
        # ---
        if 'success' in req:
            printe.output('<<lightgreen>> **Labels_API true.')
            return True
        else:
            printe.output('<<lightred>> r5' + str(req))
    # ---
    return False


def get_redirects(liste):
    # ---
    redirects = {}
    # ---
    for i in range(0, len(liste), 50):
        # ---
        # group = dict(list(liste.items())[i:i+50])
        group = liste[i : i + 50]
        params = {
            "action": "query",
            "format": "json",
            "titles": '|'.join(group),
            "redirects": 1,
            "utf8": 1,
        }
        # ---
        json1 = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
        # ---
        if json1:
            redd = json1.get("query", {}).get("redirects", [])
            for red in redd:
                redirects[red["from"]] = red["to"]
            # ---
    return redirects


# ---
'''
def Sitelink_API(Qid, title, wiki):
    # ---
    if wiki.endswith("wiki") : wiki = wiki[:-4]
    # ---
    wiki = f"{wiki}wiki"
    # ---
    print(' **Sitelink_API: Qid:"%s" %s:%s, lag:"%s"' % (Qid, wiki, title, FFa_lag[1]) )
    # ---
    if Qid.strip() == "":
        printe.output('<<lightred>> **Sitelink_API: False: Qid == "" %s:%s.' % (wiki, title) )
        return False
    # ---
    paramse = {
        "action": "wbsetsitelink",
        "id": Qid,
        "linktitle": title,
        "linksite": wiki,
    }
    # ---
    out = 'Added link to "%s" [%s]:"%s"' % ( Qid, wiki, title)
    # ---
    r4 = post(paramse, apiurl = "https://www.wikidata.org/w/api.php", token = True)
    # ---
    if not r4 or r4 == {}: return False
    # ---
    if 'success' in str(r4).lower():
        printe.output( '<<lightgreen>> true ' + out )
        return True
    # ---
    return False


def Remove_Sitelink(Qid, wiki):
    # ---
    if wiki.endswith("wiki") : wiki = wiki[:-4]
    # ---
    wiki = f"{wiki}wiki"
    # ---
    out = 'remove "%s" link from "%s"' % ( wiki , Qid)
    # ---
    params ={ "action": "wbsetsitelink", "id": Qid, "linksite": wiki}
    # ---
    r4 = post(params, apiurl = "https://www.wikidata.org/w/api.php", token = True)
    # ---
    if not r4 or r4 == {}: return False
    # ---
    if 'success' in str(r4).lower():
        printe.output( '<<lightgreen>> true ' + out )
        return True
    # ---
    return False
'''


def Claim_API_str(qid, property, string):
    # ---
    printe.output(f'<<lightyellow>> Claim_API_str: add claim to qid: {qid}, [{property}:{string}]')
    # ---
    if string == '' or qid == '' or property == '':
        return ''
    # ---
    params = {"action": "wbcreateclaim", "entity": qid, "snaktype": "value", "property": property, "value": json.JSONEncoder().encode(string)}
    # ---
    req = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
    # ---
    if not req or req == {}:
        printe.output(f'req:str({req})')
        return False
    # ---
    if 'success' in req:
        printe.output('<<lightgreen>> **Claim_API true.')
        return True
    else:
        printe.output('<<lightred>> req' + str(req))
    # ---
    return False


def Delete_claim(claimid):
    # ---
    params = {"action": "wbremoveclaims", "claim": claimid}
    # ---
    req = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
    # ---
    if not req or req == {}:
        printe.output(f'req:str({req})')
        return False
    # ---
    if 'success' in req:
        printe.output('<<lightgreen>> **Claim_API true.')
        return True
    else:
        printe.output('<<lightred>> req' + str(req))
    # ---
    return False


def Claim_API_qid(qid, property, numeric):
    # ---
    printe.output(f'<<lightyellow>> Claim_API_qid: add claim to qid: {qid}, [{property}:{numeric}]')
    # ---
    #  remove Q from numeric
    if 'Q' in numeric:
        numeric = numeric.replace('Q', '')
    # ---
    if numeric == '' or qid == '' or property == '':
        return ''
    # ---
    params = {
        "action": "wbcreateclaim",
        "entity": qid,
        "snaktype": "value",
        "property": property,
        "value": "{\"entity-type\":\"item\",\"numeric-id\":" + numeric + "}",
    }
    # ---
    req = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
    # ---
    if not req or req == {}:
        printe.output(f'req:str({req})')
        return False
    # ---
    if 'success' in req:
        printe.output('<<lightgreen>> **Claim_API true.')
        return True
    else:
        printe.output('<<lightred>> req' + str(req))
    # ---
    return False


def open_url(url, return_json=False):
    # ---
    result = {} and return_json or ""
    # ---
    # get the url
    req = False
    try:
        req = urllib.request.urlopen(url)
    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
    # ---
    if not req:
        printe.output(' open_url no req ')
        return result
    # ---
    html = ""
    try:
        html = req.read().strip().decode('utf-8')
    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        return result
    # ---
    jsontab = {}
    try:
        jsontab = json.loads(html)
    except Exception as e:
        pywikibot.output(f' open_url: Exception {e} ')
        return result
    # ---
    return jsontab


def sparql_generator_url(quary, printq=False, add_date=True):
    # ---
    if add_date:
        quary = quary + '\n#' + str(menet)
    # ---
    if printq == True:
        printe.output(quary)
    # ---
    fao = py_tools.quoteurl(quary)
    # ---
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=' + fao
    # ---
    json1 = open_url(url, return_json=False)
    # ---
    if json1 and 'head' in json1:
        var = sorted([x for x in json1['head']['vars']])
    # ---
    qlist = []
    if json1:
        if 'results' in json1:
            results = json1['results']
            if 'bindings' in results:
                for result in json1['results']['bindings']:
                    s = {}
                    # for se in result: s[se] = result[se]['value']
                    for vv in var:
                        if vv in result:
                            s[vv] = result[vv]['value']
                        else:
                            s[vv] = ''
                    qlist.append(s)
    # ---
    printe.output(f'#sparql_generator_url:<<lightgreen>> {len(qlist)} items found. {menet}')
    return qlist


def wbsearchentities(search, language):
    params = {"action": "wbsearchentities", "format": "json", "search": search, "language": language, "strictlanguage": 1, "type": "item", "utf8": 1}
    # ---
    req = post(params, apiurl="https://www.wikidata.org/w/api.php")
    # ---
    if not req or req == {}:
        printe.output(' wbsearchentities no req ')
        return False
    # ---
    if 'success' not in req:
        printe.output('<<lightred>> wbsearchentities: ' + str(req))
        return False
    # ---
    table = {}
    # ---
    if 'search' in req:
        search = req['search']  # list
        for s in search:
            ss = {
                "id": "Q111587429",
                "title": "Q111587429",
                "pageid": 106531075,
                "display": {"label": {"value": "User:Mr. Ibrahem/Sodium nitrite (medical use)", "language": "en"}},
                "repository": "wikidata",
                "url": "//www.wikidata.org/wiki/Q111587429",
                "concepturi": "http://www.wikidata.org/entity/Q111587429",
                "label": "User:Mr. Ibrahem/Sodium nitrite (medical use)",
                "match": {"type": "label", "language": "en", "text": "User:Mr. Ibrahem/Sodium nitrite (medical use)"},
            }
            # ---
            id = s['id']
            table[id] = {}
            # ---
            if s.get("display", {}).get("label", {}).get("value", '') != '':
                table[id]['label'] = s['display']['label']['value']
                table[id]['lang'] = s['display']['label']['language']
            elif s.get("match", {}).get("type", '') == 'label':
                table[id]['label'] = s['match']['text']
                table[id]['lang'] = s['match']['language']
            else:
                table[id] = s
            # ---
    # ---
    return table


def Get_claim(q, property, get_claim_id=False):
    # ---
    params = {
        "action": "wbgetclaims",
        "entity": q,
        "property": property,
    }
    # ---
    json1 = post(params, apiurl="https://www.wikidata.org/w/api.php", token=True)
    # ---
    listo = []
    # ---
    if not json1 or json1 == {}:
        return []
    # ---
    claims_p = json1.get('claims', {}).get(property, {})
    # ---
    for claims in claims_p:
        claim_id = claims.get('id', '')
        datavalue = claims.get('mainsnak', {}).get('datavalue', {})
        Type = datavalue.get("type", False)
        value = datavalue.get("value", "")
        # ---
        if isinstance(value, dict):
            if value.get("id", False):
                value = value.get("id")
        # ---
        if get_claim_id:
            listo.append({"id": claim_id, "value": value})
        else:
            listo.append(value)
    # ---
    return listo


# ---
if __name__ == '__main__':
    Log_to_wiki(url="https://www.wikidata.org/w/api.php")
# ---
# ---
