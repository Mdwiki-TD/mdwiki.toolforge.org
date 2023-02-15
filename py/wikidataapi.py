#!/usr/bin/python

"""

بوت للعمل على ويكيبيانات أو ويكيبيديا

""" 
#
# (C) Ibrahem Qasim, 2022
# 
#
#--- 

from warnings import warn
#import pywikibot
import re
import time
import urllib
import json
import codecs
import unicodedata
import sys
from datetime import datetime
#---
menet = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
#---
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
# py_tools.quoteurl(fao)
# py_tools.
# py_tools.
#---
'''
#---
import wikidataapi 
# wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php" )
# wikidataapi.post( params , apiurl = '' )
# wikidataapi.Get_page_qids( sitecode , titles )
# wikidataapi.Get_sitelinks_From_Qid( q )
# wikidataapi.WD_Merge( q1, q2)
# wikidataapi.Labels_API(Qid, label, lang, remove = False)
# wikidataapi.sparql_generator_url(quary, printq = False, add_date = True)
# wikidataapi.wbsearchentities(search, language)
# wikidataapi.
#---
'''
#---
import requests
#---
import user_account_new
#---
username = user_account_new.bot_username     #user_account_new.my_username
password = user_account_new.bot_password     #user_account_new.my_password      #user_account_new.mdwiki_pass
#---
#---
yes_answer = [ "y" , "a" , "" , "Y" , "A", "all"]
#---
SS = {}
r1_params = {
    'format': 'json',
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
}
r2_params = {
    #fz'assert': 'user',
    'format': 'json',
    'action': 'login',
    'lgname': username,
    'lgpassword': password,
}
#---
SS["ss"] = requests.Session()
#---
timesleep = 0
#---
login_not_done = { 1 : True }
#---
print_pywikibot = { 1 : False }
try:
    import pywikibot
    print_pywikibot[1] = True
except:
    print_pywikibot[1] = False
#---
def outbotnew( s ):
    if s == '' : return '' 
        #pywikibot.output( s )
    if print_pywikibot[1] :
        pywikibot.output( s )
    else:
        print( s )
#---
def Log_to_wiki(url = ''):
    #---
    if not login_not_done[1] : return ''
    #---
    outbotnew( "wikidataapi.py: log to %s user:%s" % (url, r2_params['lgname'] )  )
    SS["url"] = url
    SS["ss"] = requests.Session()
    #---
    if SS:
    #try:
        r11 = SS["ss"].get(SS["url"], params=r1_params)
        r11.raise_for_status()
        #except:
            #outbotnew( "wikidataapi.py: Can't log in . ")
        # log in
        r2_params['lgtoken'] = r11.json()['query']['tokens']['logintoken']
        r22 = SS["ss"].post(SS["url"], data= r2_params )
    #except:
    else:
        outbotnew( "wikidataapi.py: Can't log in . ")
        return False
    #---
    if r22.json()['login']['result'] != 'Success':
        outbotnew(r22.json()['login']['reason'])
        #raise RuntimeError(r22.json()['login']['reason'])
    else:
        outbotnew('wikidataapi.py login Success')
    #---
    # get edit token
    SS["r33"] = SS["ss"].get(SS["url"], params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    })
    #---
    SS["url"] = url
    #---
    SS["r3_token"] = SS["r33"].json()['query']['tokens']['csrftoken']
    #---
    #outbotnew( ' r3_token:%s' % SS["r3_token"] )
    #---
    login_not_done[1] = False
    #---
#---
def get_status(req):
    try :
        st = req.status_code
        return st
    except:
        st = req.status
        return st
#---
def post( params , apiurl='', token = True):
    #---
    Log_to_wiki(url = apiurl)
    #---
    # r4 = SS["ss"].post(SS["url"], data = params )
    # post to API without error handling
    #---
    if token :
        params["token"] = SS["r3_token"]
    #---
    params["format"] = "json"
    #---
    jsone = {}
    try:
        r4 = SS["ss"].post( SS["url"] , data = params)
        jsone = r4.json()
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( params )
        pywikibot.output( 'CRITICAL:' )
        return {}
    #---
    status = get_status(r4)
    if status != 200:
        pywikibot.output( "<<lightred>> wikidataapi.py: post error status: %s" % str(status) )
        return {}
    #---
    return jsone
#---
def Get_page_qids( sitecode , titles , apiurl='', normalize = 0 ):
    #---
    if type(titles) == str : titles = [ titles ]
    #---
    params = {
        "action": "query",
        "format": "json",
        #"prop": "langlinks|pageprops",
        # "titles": titles,
        "titles": "|".join(titles),
        "redirects": 1,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "utf8": 1,
        #"normalize": 1,
    }
    #---
    if normalize == 1 :
        params["normalize"] = 1
    #---
    if sitecode.endswith("wiki") :
        sitecode = sitecode[:-4]
    #---
    sitewiki = sitecode + 'wiki'
    #---
    if apiurl == '' and sitecode != "":
        apiurl = "https://" + sitecode + ".wikipedia.org/w/api.php"
    #---
    json1 = post(params, apiurl = apiurl)
    #---
    Main_table = {}
    #---
    if json1:
        js_query = json1.get('query',{})
        #---
        if 'query' in json1:
            #---
            if "redirects" in js_query:
                for red in js_query['redirects']:
                    #redirects_table[ red["from"] ] = red["to"]
                    Main_table[ red["from"] ] = {
                            'isRedirectPage': True,
                            'missing': True,
                            'from' : red["from"],
                            'to' : red["to"],
                            'title' : red["from"],
                            'ns' : '',
                            'q' : '',
                        }
            #---
            if 'pages' in js_query:
                for id in js_query['pages']:
                    kk = js_query['pages'][id]
                    faso = ''
                    title = ""
                    if "title" in kk:
                        title = kk["title"]
                        Main_table[title] = {}
                        if "missing" in kk:
                            Main_table[title]['missing'] = True
                        #if "ns" in kk: table['ns'] = kk["ns"]
                        #if "pageid" in kk: table['pageid'] = kk["pageid"]
                        if "pageprops" in kk and kk["pageprops"].get( "wikibase_item" , "") != "":
                            Main_table[title]['q'] =  kk["pageprops"].get( "wikibase_item" , "")
            #---
            return Main_table
    #---
    return {}
#---
def Get_sitelinks_From_Qid( q ):
    params = {
        "action": "wbgetentities",
        "format": "json",
        "props": "sitelinks",
        "ids": q,
        "utf8": 1,
    }
    #---
    table = { "sitelinks" : {} ,"q" : "" }
    #---
    json1 = post(params, apiurl = "https://www.wikidata.org/w/api.php" )
    #---
    if json1:
        if 'success' in json1 and json1['success'] == 1:
            if 'entities' in json1:
                if not "-1" in json1['entities']:
                    qli = [x for x in json1['entities'].keys() ]
                    q2 = qli[0]
                    #---
                    if q2 in json1['entities']:
                        table['q'] = q2
                        ppe = json1['entities'][q2]
                        #---
                        if 'sitelinks' in ppe:
                            for site in ppe['sitelinks'].keys():
                                fsai = ppe['sitelinks'][site]
                                table['sitelinks'][fsai['site']] = fsai['title']
                        #---
        else:
            return {}
    #---
    return table
#---
def WD_Merge( q1, q2):
    #---
    q11 = re.sub('Q' , '' , q1)
    q22 = re.sub('Q' , '' , q2)
    #---
    if q11.isdigit() and q22.isdigit():
        #---
        if int(q11) > int(q22):
            From = q1
            To = q2
        else:
            From = q2
            To = q1
    else:
        From = q2
        To = q1
    #---
    pywikibot.output('from %s to %s ' % (From , To) )
    #---
    params = {
        "action": "wbmergeitems",
        "fromid": From,
        "toid": To,
        "ignoreconflicts": "description",
        "summary": "",
    }
    #---
    r4 = post(params, apiurl = "https://www.wikidata.org/w/api.php", token = True)
    #---
    if not r4: return False
    #---
    if 'success' in r4:
        if '"redirected":1' in r4:
            pywikibot.output('<<lightgreen>> ** true .. redirected.' )
            return True
        else:
            pywikibot.output('<<lightgreen>> ** true.' )
            #---
            pams2 = {"action": "wbcreateredirect","from": From,"to": To,"ignoreconflicts": "description","summary": ""}
            #---
            r5 = post(pams2, apiurl = "https://www.wikidata.org/w/api.php", token = True)
            #---
            if 'success' in r5:
                pywikibot.output('<<lightgreen>> **createredirect true.' )
                return True
            else:
                pywikibot.output('<<lightred>> r5' + str(r5))
    else:
        pywikibot.output('<<lightred>> r4' + str(r4))
        return False
#---
def Labels_API(Qid, label, lang, remove = False):
    #---
    if Qid == '':
        pywikibot.output( "Labels_API Qid == '' " )
        return False
    #---
    if label == "" and not remove:
        pywikibot.output( "Labels_API label == '' and remove = False " )
        return False
    #---
    # save the edit
    out = '%s label:"%s"@%s.' % ( Qid , lang , label )
    #---
    params = {
        "action": "wbsetlabel",
        "id": Qid,
        "language": lang,
        "value": label,
    }
    #---
    req = post(params, apiurl = "https://www.wikidata.org/w/api.php", token = True)
    #---
    if req:
        text = str(req)
        if ('using the same description text' in text) and ('associated with language code' in text):
            item2 = re.search('(Q\d+)', str(req["error"]['info'])).group(1)
            pywikibot.output('<<lightred>>API: same label item: ' + item2 )
            #---
            #outbot(text, fi = out, NoWait = nowait)
        #---
        if 'success' in req:
            pywikibot.output('<<lightgreen>> **Labels_API true.' )
        else:
            pywikibot.output('<<lightred>> r5' + str(req))
    else:
        return False
#---
def open_url(url, return_json = False):
    #---
    result = {} and return_json or ""
    #---
    # get the url
    req = False
    try:
        req = urllib.request.urlopen(url)
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
    #---
    if not req:
        pywikibot.output( ' open_url no req ' )
        return result
    #---
    html = ""
    try:
        html = req.read().strip().decode('utf-8')
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return result 
    #---
    jsontab = {}
    try:
        jsontab = json.loads(html)
    except Exception as e:
        pywikibot.output( ' open_url: Exception %s ' % e )
        return result 
    #---
    return jsontab
#---
def sparql_generator_url(quary, printq = False, add_date = True):
    #---
    if add_date:
        quary = quary + '\n#' + str(menet)
    #---
    if printq == True:  pywikibot.output(quary)
    #---
    fao = py_tools.quoteurl(quary)
    #---
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=' + fao
    #---
    json1 = open_url(url, return_json = False)
    #---
    if json1 and 'head' in json1:
        var = [x for x in json1['head']['vars']]
        var.sort()
    #---
    qlist = []
    if json1:
        if 'results' in json1:
            results = json1['results']
            if 'bindings' in results:
                for result in json1['results']['bindings']:
                    s = {}
                    #for se in result: s[se] = result[se]['value']
                    for vv in var:
                        if vv in result:
                            s[vv] = result[vv]['value']
                        else:
                            s[vv] = ''
                    qlist.append(s)
    #---
    pywikibot.output('#sparql_generator_url:<<lightgreen>> %d items found. %s' % ( len(qlist) , menet))
    return qlist
#---
def wbsearchentities(search, language):
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": search,
        "language": language,
        "strictlanguage": 1,
        "type": "item",
        "utf8": 1
    }
    #---
    req = post(params, apiurl = "https://www.wikidata.org/w/api.php")
    #---
    if not req or req == {}:
        pywikibot.output( ' wbsearchentities no req ' )
        return False
    #---
    if not 'success' in req:
        pywikibot.output('<<lightred>> wbsearchentities: ' + str(req))
        return False
    #---
    table = {}
    #---
    if 'search' in req: 
        search = req['search'] # list
        for s in search:
            ss = {"id": "Q111587429","title": "Q111587429","pageid": 106531075,
            "display": { "label": { "value": "User:Mr. Ibrahem/Sodium nitrite (medical use)", "language": "en" } },
            "repository": "wikidata", 
            "url": "//www.wikidata.org/wiki/Q111587429",
            "concepturi": "http://www.wikidata.org/entity/Q111587429",
            "label": "User:Mr. Ibrahem/Sodium nitrite (medical use)",
            "match": {
                "type": "label",
                "language": "en",
                "text": "User:Mr. Ibrahem/Sodium nitrite (medical use)"
            }}
            #---
            id = s['id']
            table[id] = {}
            #---
            if s.get("display",{}).get("label",{}).get("value",'') != '':
                table[id]['label'] = s['display']['label']['value']
                table[id]['lang'] = s['display']['label']['language']
            elif s.get("match",{}).get("type",'') == 'label':
                table[id]['label'] = s['match']['text']
                table[id]['lang'] = s['match']['language']
            else:
                table[id] = s
            #---
    #---
    return table
#---
#---
if __name__ == '__main__':
    Log_to_wiki(url="https://www.wikidata.org/w/api.php")
#---
#---