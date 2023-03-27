#!/usr/bin/python

"""

"""
#
# (C) Ibrahem Qasim, 2022
# 
#
#--- 
#import pywikibot
import re
import json as JJson
import time
import urllib
import codecs
import unicodedata
#import datetime
#from datetime import datetime
#---
import sys
sys.dont_write_bytecode = True
#---
#---
'''
#---
from mdpy import mdwiki_api
# mdwiki_api.post(params)
# mdwiki_api.wordcount(title, srlimit='30')
# mdwiki_api.purge(title)
# mdwiki_api.page_put(NewText, summary, title, time_sleep="", minor="")
# mdwiki_api.page_putWithAsk(oldtext, NewText, summary, title, Ask, minor="")
# mdwiki_api.create_Page(text, summary, title, ask, sleep=0, duplicate4="")
# mdwiki_api.Add_To_Bottom(appendtext, summary, title, ask)
# mdwiki_api.Add_To_Head(prependtext, summary, title, Ask)
# mdwiki_api.move(From, to, reason)
# mdwiki_api.Get_Newpages(limit="max", namespace="0", rcstart="", user='')
# mdwiki_api.Get_UserContribs(user, limit="max", namespace="*", ucshow="")
# mdwiki_api.GetPageText(title)
# mdwiki_api.Get_All_pages(start, limit="max", namespace="*", apfilterredir='')
# mdwiki_api.Search(title, ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# mdwiki_api.import_page(title)
# mdwiki_api.Get_page_links(title, namespace="*", limit="max")
# mdwiki_api.subcatquery(title, depth=0, ns="all", without_lang="", with_lang="", tempyes=[], limit=0)
# mdwiki_api.get_redirect(liste)
# mdwiki_api.
# mdwiki_api.
#---
'''
#---
maxlag = 3 #"3"
ar_lag = { 1 : maxlag }
#---
import requests
#---
from mdpy import user_account_new
#---
username = user_account_new.my_username     #user_account_new.bot_username
password = user_account_new.mdwiki_pass     #user_account_new.bot_password      #user_account_new.my_password
#---
Main_User = { 1: username}
Bot_or_himo = { 1: ""}
if Main_User[1].find("bot") == -1:
    Bot_or_himo[1] = 1
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
    if print_pywikibot[1] :
        pywikibot.output( s )
    else:
        print( s )
#---
def py_input( s ):
    #sa = pywikibot.input( s )
    #---
    if print_pywikibot[1] :
        sa = pywikibot.input( s )
    else:
        outbotnew( s )
        sa = input()
    #---
    return sa
#---
#---
def get_status(req):
    try :
        st = req.status_code
        return st
    except Exception as e:
        outbotnew( 'Traceback (most recent call last):' )
        outbotnew(f'<<lightred>> {__file__} Exception:' + str(e) )
        outbotnew( 'CRITICAL:' )
        st = req.status
        return st
#---
def post( params ):
    #---
    # r4 = SS["ss"].post(SS["url"], data = params )
    # post to API without error handling
    #---
    r4 = False
    try:
        r4 = SS["ss"].post( SS["url"], data = params)
    except Exception as e:
        outbotnew( 'Traceback (most recent call last):' )
        outbotnew(f'<<lightred>> {__file__} Exception:' + str(e) )
        outbotnew( "API: post ss error: %s" % str(e) )
        outbotnew( 'CRITICAL:' )
        if 'Exception' in sys.argv:
            raise Exception(e)
        return {}
    #---
    jsone = {}
    try:
        jsone = r4.json()
    except Exception as e:
        outbotnew( 'Traceback (most recent call last):' )
        outbotnew(f'<<lightred>> {__file__} Exception:' + str(e) )
        outbotnew( r4.text )
        outbotnew( 'CRITICAL:' )
        if 'Exception' in sys.argv:
            raise Exception(e)
        jsone = {}
    #---
    if r4:
        status = get_status(r4)
        if status != 200:
            outbotnew( " mdAPI: post_ss error: %s" % r4.text )
            return {}
    #---
    return jsone
#---
def Log_to_wiki(family = 'mdwiki' , lang = "www" ):
    #---
    #---
    outbotnew( "mdwiki/mdpy/mdwiki_api.py: log to %s.%s.org user:%s" % (lang,family , r2_params['lgname'] )    )
    SS["family"] = family
    SS["lang"] = lang
    SS["url"] = 'https://' + '%s.%s.org/w/api.php' % (lang , family)
    SS["ss"] = requests.Session()
    #---
    r22 = {}
    #if SS:
    try:
        r11 = SS["ss"].get(SS["url"], params=r1_params)
        r11.raise_for_status()
    except Exception as e:
        outbotnew( 'Traceback (most recent call last):' )
        outbotnew(f'<<lightred>> {__file__} Exception:' + str(e) )
        outbotnew( 'CRITICAL:' )
        return False
    r2_params['lgtoken'] = r11.json()['query']['tokens']['logintoken']
    #---
    r22 = post( r2_params )
    if r22:
        if r22['login']['result'] != 'Success':
            outbotnew(r22['login']['reason'])
        else:
            outbotnew('mdwiki_api.py login Success')
    else:
        outbotnew('mdwiki_api.py login error')
        return False
    #---
    # get edit token
    try:
        SS["r33"] = SS["ss"].get(SS["url"], params={
            'format': 'json',
            'action': 'query',
            'meta': 'tokens',
        })
    except Exception as e:
        outbotnew( "mdwiki_api.py: Log_to_wiki error: %s" % e )
        return False
    #---
    SS["url"] = 'https://' + '%s.%s.org/w/api.php' % (lang , family)
    #---
    SS["r3_token"] = SS["r33"].json()['query']['tokens']['csrftoken']
    #---
    login_not_done[1] = False
#---
Log_to_wiki("mdwiki" , lang = "www" )
#---
def outbot(text2):
    text = {}
    #---
    if type(text2) == dict:
        text = text2
    else:
        try:
            text = JJson.loads(text2)
        except:
            outbotnew("error when JJson loads text2")
    #---{'error': {'*': 'See https://mdwiki.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes.', 'info': 'Invalid CSRF token.', 'code': 'badtoken'}}
    #{'error': {'info': 'Invalid CSRF token.', '*': 'See https://mdwiki.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes.', 'code': 'badtoken'}}
    #---
    Invalid = ''
    if type(text.get("error",{})) == dict:
        Invalid = text.get("error",{}).get("info",'')
    #---
    if Invalid == "Invalid CSRF token." : 
        outbotnew('<<lightred>> ** error "Invalid CSRF token.". ')
        outbotnew(text)
        Log_to_wiki("mdwiki" , lang = "www" )
    elif 'maxlag' in text:
        outbotnew('<<lightred>> maxlag: sleep for %d secound.' % 3)
        tabe = text.get("error",{}).get("lag",0)
        lagese = int( tabe )
        if lagese != ar_lag[1]:
            ar_lag[1] = lagese + 1
            slee = ar_lag[1] / 4
            outbotnew('<<lightpurple>> maxlag:%d sleep for %d secound.' % (ar_lag[1] , slee ) )
            time.sleep( slee )
        else:
            outbotnew('<<lightpurple>> lagese == ar_lag[1] (%d)' % ar_lag[1] )
            time.sleep(3)
        #---
    elif 'تأخير البوتات 3 ساعات' in text :
        outbotnew('<<lightred>> ** تأخير البوتات 3 ساعات. ')
        #---
    elif 'error' in text :
        outbotnew('<<lightred>> ** error. ')
        outbotnew(text)
        #---
        if 'code' in text['error']:
            if text['error']['code'] == "articleexists":
                outbotnew('<<lightred>> ** article already created. ')
                return "articleexists"
        else:
            outbotnew(text)
        #---
    elif 'success' in text or 'Success' in text:
        outbotnew('<<lightgreen>> ** true. ' )
    else:
        outbotnew(text2)
#---
def import_history2( FILE_PATH , title ):
    #---
    outbotnew('<<lightpurple>> import_history for page:%s:' % title )
    #---
    namespace = 0
    if title.lower().startswith('user:') : namespace = 2
    #---
    pp = {
        "action": "import",
        "format": "json",
        #"xml": "...",
        "interwikiprefix": "user:",
        "fullhistory": 1,
        "namespace": namespace,
        #"assignknownusers": 1,
        "token": SS["r3_token"],
        "utf8": 1
    }
    #---
    NewList = []
    #---
    if FILE_PATH and type(FILE_PATH) != list:
        NewList.append(FILE_PATH)
    elif FILE_PATH and type(FILE_PATH) == list:
        NewList = FILE_PATH
    #---
    for fff in NewList:
        outbotnew(' file:"%s"' % fff )
        FILE = {'xml':('file.xml', open( fff ))}
        #DATA = R.json()
        #print(DATA)
        r4 = SS["ss"].post(url=SS["url"], files=FILE, data=pp)
        #---
        DATA = r4.json()
        outbotnew( DATA )
        #---
        if 'Success' in r4.text:
            outbotnew('<<lightgreen>> ** true .. . ' )
        #---
        outbot(r4.text)
#---
def import_history( FILE_PATH , title ):
    #---
    outbotnew('<<lightpurple>> import_history for page:%s:' % title )
    #---
    namespace = 0
    if title.lower().startswith('user:') :  namespace = 2
    #---
    pparams = {
        "action": "import",
        "format": "json",
        "interwikisource": "wikipedia",
        "interwikipage": title,
        "token": SS["r3_token"],
        #"summary": "",
        "fullhistory": 1,
        "namespace": namespace ,
        }
    #---
    NewList = []
    #---
    if FILE_PATH and type(FILE_PATH) != list:
        NewList.append(FILE_PATH)
    elif FILE_PATH and type(FILE_PATH) == list:
        NewList = FILE_PATH
    #---
    for fff in NewList:
        outbotnew(' file:"%s"' % fff )
        FILE = {'xml':('file.xml', open(fff))}
        #DATA = R.json()
        #print(DATA)
        #--- 
        try:
            r4 = SS["ss"].post(url=SS["url"], files=FILE, data=pparams)
            #---
            if 'Success' in r4.text:
                outbotnew('<<lightgreen>> ** true .. . ' )
        except Exception as e:
            outbotnew( 'Traceback (most recent call last):' )
            outbotnew(f'<<lightred>> {__file__} Exception:' + str(e) )
            outbotnew( 'CRITICAL:' )
            r4 = {}
        #---
        DATA = r4#.json()
        outbotnew( DATA )
        #---
        #outbot(r4.text)
#---

#---
def Get_cat(enlink, ns, lllang="", tempyes=[], lang_no='', print_url=True ): 
    #---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    #---
    #outbotnew(' Get_cat for %s' % (enlink) )
    #---
    if not enlink.startswith('Category:') :
        enlink = 'Category:' + enlink
    #---
    params = {
        "action": "query",
        "format": "json",
        "utf8": 1,
        
        "generator": "categorymembers",
        "gcmtitle": enlink,
        "gcmprop": "title",
        "gcmtype": "page|subcat",
        "gcmlimit": "max",
        
        "redirects": 1,
        #"prop": "templates",
        #"tllimit": "max",
        
        #"lllang": langcode,
        #"lllimit": "max",
    }
    #---
    #if not "tempapi" in sys_argv :
        #params["prop"] = "templates"
        #params["tllimit"] = "max"
    #---
    if tempyes != []:
        params["prop"] = "templates"
        params["tllimit"] = "max"
        params["tltemplates"] = "|".join( tempyes )
    #---
    if lllang != "" or lang_no :        # مع وصلة لغة معينة
        params["prop"] = params["prop"] + "|langlinks"
        #params["lllang"] = lllang
        params["lllimit"] = "max"
    #---all
    if ns == "0" or ns == "10" :
        params["gcmtype"] = "page"
    elif ns == "14" :
        params["gcmtype"] = "subcat"
    elif ns == "all" :
        params["gcmtype"] = "page|subcat"
    #---
    #outbotnew('<<lightblue>> API_CALLS %d   for %s' % (API_CALLS[1],enlink) )
    #---
    if print_url or "printurl" in sys.argv:
        lis = [ "{}={}".format( x , y ) for x,y in params.items() ]
        url = "api.php?" + "&".join( lis )
        outbotnew(url)
    #----
    continue_p = ''
    continue_v = 'x'
    #---
    table = {}
    #----
    while continue_v != '' : 
        #---
        if continue_v != 'x':
            params[continue_p] = continue_v
        #---
        continue_v = ''
        #---
        api = post( params )
        #---
        if not api: break
        #---
        continue_d = api.get("continue", {})
        for p, v in continue_d.items():
            if p == 'continue' : continue
            continue_v = v
            continue_p = p
        #----
        pages = api.get( "query", {}).get( "pages", {})
        #----
        for category in pages:
            #---
            caca = category
            #---
            if type(pages) == dict: caca = pages[category]
            #---
            cate_title = caca["title"]
            tablese = {}
            #outbotnew("<<lightblue>> cate_title: %s" % cate_title ) 
            #---
            if "ns" in caca:
                tablese['ns'] = caca['ns']
                #outbotnew("<<lightblue>> ns: %s" %   caca['ns']) 
            #---
            if 'templates' in caca:
                tablese['templates'] = [ x['title'] for x in caca['templates'] ]
            #---
            if 'langlinks' in caca:
                tablese['langlinks'] = {}
                for fo in caca['langlinks']:
                    result = fo['*']
                    tablese['langlinks'][fo['lang']] = fo['*']
            #---
            table[cate_title] = tablese
            #---
    #---
    subcats = [ x for x in table if str(table[x]['ns']) == "14" ]
    #---
    outbotnew( '<<lightgreen>> Getcat: find %d subcat:%s' % ( len(subcats) , ",".join(subcats) ) )
    #---
    outbotnew( '<<lightyellow>> cat:%s has:%d pages.' % ( enlink , len(table) ) )
    #---
    return table
#---
def subcatquery( title, depth=0, ns="all", limit=0, test=False, without_lang="", with_lang="", tempyes=[] ): 
    #---
    #---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    #---
    #outbotnew('<<lightyellow>> catdepth.py sub cat query for %s:%s,depth:%d,ns:%s.' % ('',title,depth,ns) )
    #---
    start = time.time()
    final = time.time()
    #---
    if not title.strip().startswith('Category:') : title = 'Category:' + title.strip()
    #---
    tablemember = Get_cat( title, ns, tempyes=tempyes, lang_no=without_lang, lllang=with_lang , print_url=False )
    #---
    result_table = {}
    #---
    for x in tablemember:
        #---
        vaild = True
        #---
        # البحث عن وصلة لغة غير مرغوب بوجودها
        if without_lang and without_lang != "":
            no_langs = tablemember[x].get('langlinks',{}).get(without_lang,'')
            if no_langs and no_langs != "":
                vaild = False
        #---
        # البحث عن وصلة لغة مرغوب بوجودها
        if with_lang and with_lang != "":
            langs = tablemember[x].get('langlinks',{}).get(with_lang,'')
            if langs != "":
                vaild = True
            else:
                vaild = False
        #---
        if vaild:
            result_table[x] = tablemember[x]
    #---
    cat_done = []
    #---
    new_list = [ x for x in tablemember if int(tablemember[x]["ns"]) == 14 ]
    #---
    depth_done = 0
    #--- 
    if type(depth) != int:
        try:
            depth = int(depth)
        except:
            outbotnew('<<lightblue>> type(depth) != int ' )
    #--- 
    while depth > depth_done :#and ( limit > 0 and len(result_table) < limit ):
        depth_done += 1
        new_tab2 = []
        #---
        for cat in new_list:
            #---
            outbotnew('get pages from subcat:%s' % cat )
            #---
            if not cat in cat_done:
                cat_done.append(cat)
                table2 = Get_cat(cat , ns)
                for x in table2:
                    #---
                    if int(table2[x]["ns"]) == 14:
                        new_tab2.append( x )
                    #---
                    vaild = True
                    #---
                    # البحث عن وصلة لغة غير مرغوب بوجودها
                    if without_lang and without_lang != "":
                        no_langs = table2[x].get('langlinks',{}).get(without_lang,'')
                        if no_langs and no_langs != "":
                            vaild = False
                    #---
                    # البحث عن وصلة لغة مرغوب بوجودها
                    if with_lang and with_lang != "":
                        langs = table2[x].get('langlinks',{}).get(with_lang,'')
                        if langs != "":
                            vaild = True
                        else:
                            vaild = False
                    #---
                    if vaild:
                        result_table[x] = table2[x]
                    #---
        new_list = new_tab2
    #---
    final = time.time()
    delta = int(final - start)
    #---
    #if "printresult" in sys_argv: outbotnew(result_table)
    #---
    outbotnew('<<lightblue>>catdepth.py: find %d pages(%s) in %s:%s, depth:%d in %d seconds' % (len(result_table),str(ns),'',title,depth,delta ) )
    #---
    result_tab = list( result_table.keys() )
    #---
    result_tab = [ x for x in result_tab if not ( x.startswith('Category:') or x.startswith('File:') or x.startswith('Template:') or x.startswith('User:') or x.endswith("(disambiguation)") ) ]
    #---
    #return result_table
    return result_tab
#---
def import_page( title ) : 
    params = {  
        "action" : "import" , 
        "format" : "json" , 
        "interwikisource":"wikipedia" , 
        "interwikipage":title,
        "fullhistory" : 1 ,
        "assignknownusers" : 1 ,
        "token" :  SS["r3_token"]
        }
    #---
    r4 = post( params )
    #---
    outbot('import_page:' )
    outbot( r4 )
    #---
    return r4
    #---
#---
def wordcount(title, srlimit='30'):
    # srlimit = "30"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": title,
        "srlimit": srlimit,
        "format" : "json" , 
    }
    data = post(params)
    #---
    if data == {}: return 0
    #---
    search = data.get('query', {}).get('search', [])
    #---
    words = 0
    #---
    for pag in search:
        tit = pag["title"]
        count = pag["wordcount"]
        if tit == title: 
            words = count
            break
    #---
    return words
#---
def page_put_new(NewText,summary,title,time_sleep="",family="",lang="",minor="",nocreate=1,tags="",basetimestamp="",returntrue=False,return_newtimestamp=False,return_table=False):
    #---
    outbotnew(' page_put %s:' % title )
    #---
    if minor == "" : 
        minor = Bot_or_himo[1]
    #---#
    #"tags": "تعديل شريط البوابات",
    #---
    pparams = {
        "action": "edit",
        "format": "json",
        #"maxlag": ar_lag[1],
        "title": title,
        "text": NewText,
        "summary": summary,
        #"starttimestamp": starttimestamp,
        "minor": minor,
        #"notminor": 1,
        "bot": 1,
        "nocreate": nocreate,
        "token": SS["r3_token"] ,
    }
    #---
    if sys.argv and "workibrahem" in sys.argv : 
        pparams["summary"] = ""
    #---
    if basetimestamp != "" :
        pparams["basetimestamp"] = basetimestamp
    #---
    if tags != "" :
        pparams["tags"] = tags
    #---
    tts = timesleep
    if time_sleep != "" : tts = time_sleep
    #---
    r4 = post(pparams)
    #---
    Invalid = ''
    if type(r4.get("error",{})) == dict:
        Invalid = r4.get("error",{}).get("info",'')
    #---
    if 'Success' in str(r4):
        outbotnew('<<lightgreen>> ** true .. ' + '[[%s:%s:%s]]   time.sleep(%d) ' % (SS["lang"] , SS["family"] ,title , tts)  )
        outbotnew( 'تم بنجاح... time.sleep(%d) ' % tts)
        time.sleep(tts)
        if return_table:
            return r4
        elif returntrue:
            return True
        elif return_newtimestamp:
            return r4.get('edit',{}).get('newtimestamp','')
    #---
    elif Invalid == "Invalid CSRF token." : 
        outbotnew('<<lightred>> ** error "Invalid CSRF token.". ')
        outbotnew(r4)
        #---
        Log_to_wiki("mdwiki" , lang = "www" )
        #---
        return page_put_new(NewText,summary,title,time_sleep=time_sleep,family=family,lang=lang,minor=minor,nocreate=nocreate,tags=tags,basetimestamp=basetimestamp,returntrue=returntrue,return_newtimestamp=return_newtimestamp)
    #---
    else:
        outbot(r4)
        if returntrue:
            return False
        elif return_table:
            return {}
#---
Save_2020 = { 1 : False }
#---
def page_put(NewText , summary , title, time_sleep="", family="", lang="", minor="", nocreate = 1 , tags="", basetimestamp="", returntrue = False,oldtext = '', diff=True):
    #---
    if not Save_2020[1] and "ask" in sys.argv and not "save" in sys.argv :
        if diff:
            try:
                pywikibot.showDiff(oldtext , NewText)
            except:
                outbotnew( ' -mdwiki cant showDiff' )
        outbotnew(' -Edit summary: %s:' % summary )
        sa = py_input('<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Do you want to accept these changes? ([y]es, [N]o, [a]ll): for page %s:%s.org user:%s'  %(lang,title,r2_params['lgname'] ))
        #---
        if sa == "a":
            outbotnew('<<lightgreen>> ---------------------------------' )
            outbotnew('<<lightgreen>> mdwiki.py save all without asking.' )
            outbotnew('<<lightgreen>> ---------------------------------' )
            Save_2020[1] = True
        #---
        if not sa in yes_answer:
            outbotnew( "wrong answer" )
            return False
    #---
    return page_put_new(NewText , summary , title
        , time_sleep = time_sleep, family = family, lang = lang
        , minor = minor, nocreate = nocreate , tags = tags
        , basetimestamp = basetimestamp , returntrue = returntrue)
#---
def GetPageText(title , redirects = False):
    #outbotnew( '**GetarPageText: ')
    #---
    params = {
        "action": "parse",
        "format": "json",
        #"prop": "wikitext|sections",
        "prop": "wikitext",
        "page": title,
        #"redirects": 1,
        "utf8": 1,
        #"normalize": 1,
    }
    #---
    if redirects:   params["redirects"] = 1
    #---
    text = ''
    json1 = post( params )
    if json1: 
        text = json1.get('parse',{}).get('wikitext',{}).get('*','')
    else:
        outbotnew('no parse in json1:' )
        outbotnew(json1)
    #---
    if text == "" :
        outbotnew('page %s text == "".' % title )
    #---
    return text
#---
def Get_Newpages(limit="max", namespace="0", rcstart="", user=''):
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
    json1 = post( params )
    #---
    Main_table = []
    #---
    if not json1 or json1 == {} : return []
    #---
    newp = json1.get( "query" , {} ).get( "recentchanges" , {} )
    #---
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
    #---
    Main_table = [ x[ "title" ] for x in newp ]
    #---
    return Main_table
#---
def Get_page_links( title , namespace = "0" , limit = "max" ):
    #---
    outbotnew( 'Get_page_links for title:"%s", limit:"%s",namespace:"%s"' % ( title , limit , namespace ) )
    #---
    params = {
        "action": "query",
        "format": "json",
        "prop": "links",
        "titles": title,
        "plnamespace": namespace,
        "pllimit": limit,
        "converttitles": 1,
        "utf8": 1,
        "bot": 1,
    }
    #---
    #if apfilterredir in [ 'redirects' , 'all' , 'nonredirects' ] : params['apfilterredir'] = apfilterredir
    #---
    json1 = post( params )
    #---
    Main_table = {'links' : {} , 'normalized' : [] , 'redirects' : [] , }
    #---
    if json1:
        #---
        query = json1.get( "query" , {} )
        Main_table['normalized'] = query.get( "normalized" , [] )
        Main_table['redirects'] = query.get( "redirects" , [] )
        #---
        pages = query.get( "pages" , {} )
        #---
        for page in pages:
            tab = pages[page]
            for pa in tab.get('links',[]):
                Main_table['links'][pa[ "title" ]] = { 'ns' : pa[ "ns" ] , 'title' : pa[ "title" ] }
    else:
        outbotnew( "mdwiki_api.py no json1" )
    #---
    outbotnew( "mdwiki_api.py Get_page_links : find %d pages." % len(Main_table['links']) )
    #---
    return Main_table
#---
def Get_page_links_2(title):
    Main_table = Get_page_links(title)
    lista = Main_table.get('links', {}).keys()
    return lista    
#---
def Get_template_pages( title, namespace = "*", limit = "max" ):
    #---
    outbotnew( 'Get_template_pages for template:"%s", limit:"%s",namespace:"%s"' % ( title, limit, namespace ) )
    #---
    params = {
        "action": "query",
        "format": "json",
        "prop": "info",
        "titles": title,
        "generator": "transcludedin",
        "gtinamespace": namespace,
        "gtilimit": limit
        }
    #---
    Main_table = []
    gticontinue = 'x'
    #---
    while gticontinue != '' : 
        #---
        if gticontinue != 'x':
            params['gticontinue'] = gticontinue
        #---
        json1 = post( params )
        #---
        if not json1: break
        #---
        gticontinue = json1.get("continue", {}).get("gticontinue", '')
        #---
        pages = json1.get( "query",{}).get( "pages" , {} )
        #---
        for _, tab in pages.items():
            Main_table.append( tab[ "title" ] )
        #---
        outbotnew('len of Main_table:%d.' % (len(Main_table)) )
        #---
    #---
    outbotnew( "mdwiki_api.py Get_template_pages : find %d pages." % len(Main_table) )
    #---
    return Main_table
#---
def Get_All_pages_A( start , namespace = "0" , limit = "max" , apfilterredir='',apcontinue='' ):
    #---
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        #"apfrom": start,
        "apnamespace": namespace,
        "aplimit": limit,
        "apfilterredir": "nonredirects",
        "utf8": 1,
        "bot": 1,
    }
    #---
    if apfilterredir in [ 'redirects' , 'all' , 'nonredirects' ]  : params['apfilterredir'] = apfilterredir
    #---
    if start != '' : params['apfrom'] = start
    #---
    if apcontinue != '' : params['apcontinue'] = apcontinue
    #---
    json1 = post( params )
    #---
    if json1 : 
        newss = json1.get( "query" , {} ).get( "allpages" , {} )
        outbotnew( "<<lightpurple>> --- Get_All_pages_A : find %d pages." % len(newss) )
    #---
    return json1
#---
def Get_All_pages( start , namespace = "0" , limit = "max" , apfilterredir='', limit_all = 0 ):
    #---
    outbotnew( 'Get_All_pages for start:"%s", limit:"%s",namespace:"%s",apfilterredir:"%s"' % ( start , limit , namespace , apfilterredir ) )
    #---
    json1 = Get_All_pages_A( start , namespace = namespace , limit = limit , apfilterredir = apfilterredir )
    #---
    Main_table = []
    #---
    Apcontinue = ''
    #---
    if json1:
        Apcontinue = json1.get( "continue" , {} ).get( "apcontinue" , '' )
        newp = json1.get( "query" , {} ).get( "allpages" , {} )
        #---
        Main_table = [ x[ "title" ] for x in newp ]
    else:
        outbotnew( "mdwiki_api.py no json1" )
    #---
    Apcontinue2 = { 1 : Apcontinue }
    numb = 0
    #---
    while Apcontinue2[1] != '' : 
        #---
        numb += 1
        #---
        outbotnew( 'Get_All_pages_A %d, Apcontinue2[1]:"%s"..' % ( numb , Apcontinue2[1] ) )
        #---
        json2 = Get_All_pages_A( start , namespace = namespace , limit = limit , apfilterredir = apfilterredir , apcontinue = Apcontinue2[1] )
        #---
        if json2:
            Apcontinue2[1] = json2.get( "continue" , {} ).get( "apcontinue" , '' )
            #---
            newp = json2.get( "query" , {} ).get( "allpages" , {} )
            #---
            for x in newp : 
                if not x[ "title" ] in Main_table : 
                    Main_table.append( x[ "title" ] )
            #---
            outbotnew( "len of Main_table %d." % len(Main_table) )
            #---
        else:
            outbotnew( "mdwiki_api.py no json1" )
        #---
        if limit_all > 0 and len(Main_table) > limit_all : 
            Apcontinue2[1] = '' 
            outbotnew( "<<lightgreen>> limit_all > len(Main_table) " )
            break
        #---
    #---
    if numb > 0 and Apcontinue2[1] == '' : 
        outbotnew( "<<lightgreen>> Apcontinue2[1] == '' " )
    #---
    outbotnew( "mdwiki_api.py Get_All_pages : find %d pages." % len(Main_table) )
    #---
    return Main_table
#---
def Get_UserContribs( user , limit="max", namespace = "*" , ucshow = "" ):
    #---
    outbotnew('Get_UserContribs for user:"%s", limit:"%s"' % ( user , limit ) )
    #---
    params = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucdir": "older",
        "ucnamespace": namespace,
        "uclimit": limit,
        "ucuser": user,
        "utf8": 1,
        "bot": 1,
        "ucprop": "title"
        #"ucshow": "new"
    }
    #---
    if ucshow != "":
        params["ucshow"] = ucshow
    #---
    json1 = post( params )
    #---
    Main_table = []
    #---
    if json1:
        newp = json1.get( "query" , {} ).get( "usercontribs" , {} )
        #---
        Main_table = [ x[ "title" ] for x in newp ]
    #---
    outbotnew( "mdwiki_api.py Get_Newpages : find %d pages." % len(Main_table) )
    #---
    return Main_table
#---
def Search( valu , lang="", family='', ns="", offset='', srlimit = "max" , RETURN_dict = False , addparams = {} ):
    #---
    Lidy = []
    #---
    outbotnew( 'mdwiki_api.Search for "%s",ns:%s' % (valu,ns) )
    #---
    if srlimit == "":
        srlimit = "max"
    #---
    #srlimit = "max"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "utf8": 1,
        "srsearch": valu,
        "srnamespace": 0,
        "srlimit": srlimit,
        #"token": SS["r3_token"]
    }
    #---
    nsvalue = ns
    #---
    if nsvalue == "" :
        for arg in sys.argv:
            arg, sep, value = arg.partition(':')
            #---
            if arg == "-ns" : 
                nsvalue = value
    #---
    if addparams != {} :
        for pp in addparams:
            params[pp] = addparams[pp]
    #---
    if nsvalue != "" :
        params["srnamespace"] = nsvalue
    #---
    if offset != "" :
        params["sroffset"] = offset
    #---
    json1 = post( params )
    if "query" in json1 and "search" in json1['query']:
        for pag in json1['query']['search']:
            tit = pag["title"]
            if RETURN_dict:
                Lidy.append( pag )
            else:
                Lidy.append( tit )
    #---
    #if Lidy == []:  
    outbotnew( 'mdwiki_api.Search find "%d" result. s' % len(Lidy) )
    #---
    return Lidy
#--- 
def Add_To_Bottom2(aptext , summary , title, poss="", family="", minor = "" ):
    if title.strip() != "" : 
        outbotnew('** Add_To_Bottom2 .. ' + '[[' + title + ']] ' )
        #pywikibot.showDiff("" , aptext)
        #---
        Paramso = {
            "action": "edit",
            "format": "json",
            #"maxlag": ar_lag[1],
            "title": title,
            #"appendtext": "\n" + aptext,
            "summary": summary,
            "bot": Bot_or_himo[1],
            "notminor": 1,
            "nocreate": 1,
            #"token": r3.json()['query']['tokens']['csrftoken'],
            "utf8": 1
        }
        #---
        if poss == "Head" : 
            Paramso["prependtext"] = aptext.strip() + "\n"
        else:
            Paramso["appendtext"] = "\n" + aptext.strip()
        #---
        if sys.argv and "workibrahem" in sys.argv : 
            Paramso["summary"] = ""
        #---
        Paramso["token"] = SS["r3_token"]
        r4 = post(Paramso)
        #---
        if 'Success' in r4:
            outbotnew('<<lightgreen>>** true .. %s : [[%s]] '    % (SS["family"] , title) )
            outbotnew( 'تم بنجاح... time.sleep(%d) ' % timesleep)
            #time.sleep(timesleep)
        else:
            outbot(r4)
    else:
        outbotnew('** Add_To_Bottom2 ..  title == ""' )
#---
def Add_To_Head(prependtext , summary , title, Ask, minor = "" ):
    if title.strip() != "" : 
        #---
        outbotnew(' Add_To_Head for Page %s:' % title )
        #outbotnew(prependtext)
        faso = False
        if Ask or "ask" in sys.argv and not "save" in sys.argv:
        #if Ask:
            #pywikibot.showDiff( "" , prependtext )
            sa = py_input('<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Add_To_Head of page "%s" ? ([y]es, [N]o):'  % title)
            if sa in yes_answer:
                faso = True
                Add_To_Bottom2(prependtext , summary , title, poss = "Head", minor = minor )
            else:
                outbotnew( "wrong answer" )
            return sa
        else:
            faso = True
            Add_To_Bottom2(prependtext , summary , title , poss = "Head", minor = minor )
        #---
    else:
        outbotnew('** Add_To_Head ..  title == ""' )
#---
def Add_To_Bottom(appendtext , summary , title, Ask , family="", minor = "" ):
    if title.strip() != "" : 
        #---
        outbotnew(' Add_To_Bottom for Page %s:' % title )
        outbotnew( appendtext)
        faso = False
        if Ask or "ask" in sys.argv and not "save" in sys.argv:
        #if Ask:
            sa = py_input('<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Add_To_Bottom of page "%s" ? ([y]es, [N]o):' % title)
            if sa in yes_answer:
                faso = True
                Add_To_Bottom2(appendtext , summary , title, family = family, minor = minor )
            else:
                outbotnew( "wrong answer" )
            return sa
        else:
            faso = True
            Add_To_Bottom2(appendtext , summary , title, family = family, minor = minor )
        #---
    else:
        outbotnew('** Add_To_Bottom ..  title == ""' )
#---
Save_2040 = { 1 : False }
#---
def create_Page(text , summary , title , ask, sleep=0, family="", duplicate4="", minor = "", printtext=True ):
    outbotnew(' create Page %s:' % title )
    time_sleep = timesleep
    #---
    if title.startswith("نقاش القالب:") and  title.endswith("/ملعب"):
        outbotnew( ' skip make talk to sandboxes..' )
        return False
    #---
    if sleep != False:
        time_sleep = sleep
    #---
    params = {
        "action": "edit",
        "format": "json",
        #"maxlag": ar_lag[1],
        "title": title,
        "text": text,
        "summary": summary,
        "bot": Bot_or_himo[1],
        "notminor": 1,
        "createonly": 1,
        "token": SS["r3_token"] ,
        "utf8": 1
    }
    #---
    if sys.argv and "workibrahem" in sys.argv : 
        params["summary"] = "+"
    #---
    sa = {"error":{"code":"articleexists","info":"The article you tried to create has been created already.","*":"See https://ar.wikipedia.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/mailman/listinfo/mediawiki-api-announce&gt; for notice of API deprecations and breaking changes."},"servedby":"mw1284"}
    Faco = False
    #---
    if not Save_2040[1] and ( ask or "ask" in sys.argv and not "save" in sys.argv ) :
    #if ask or "ask" in sys.argv and not "save" in sys.argv:
    #if ask:
        #pywikibot.showDiff("" , text)
        if printtext:
            outbotnew( "<<lightgreen>> " + text)
        outbotnew( " summary: " + summary)
        sa = py_input('<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: create %s:"%s" page ? ([y]es, [N]o):user:%s' % (family,title,r2_params['lgname']))
        if sa.strip() in yes_answer:
            #---
            if sa.strip() == "a":
                outbotnew('<<lightgreen>> ---------------------------------------------' )
                outbotnew('<<lightgreen>> mdwiki.py create_Page save all without asking.' )
                outbotnew('<<lightgreen>> ---------------------------------------------' )
                Save_2040[1] = True
            #---
            r4 = post(params)
            Faco = True
        else:
            outbotnew( "wrong answer" )
            return False
    else:
        r4 = post(params)
        Faco = True
    #---a
    if Faco:
        #---
        if 'Success' in r4 :
            outbotnew('<<lightgreen>>** true ..  %s : [[%s]] '    % (SS["family"] , title) )
            outbotnew( 'تم بنجاح... time.sleep(%d) ' % time_sleep)
            time.sleep(time_sleep)
            return True
        elif 'error' in r4 :
            if 'code' in r4['error']:
                if r4['error']['code'] == "articleexists":
                    outbotnew("error when create_Page")
            outbot(r4)
        else:
            outbotnew( "create_Page: outbot(r4.text)" )
            outbot(r4)
            return False
    #---a
    outbotnew( "<<lightred>> end of create_Page def return False title:(%s)" % title )
    outbotnew(r4)
    #---a
    return False
#---
def page_putWithAsk(oldtext,NewText,summary,title,Ask,lang="",family="",minor="",tags="",nocreate=1,basetimestamp="",returntrue=False):
    #---
    outbotnew(' page_put %s:' % title )
    #---
    if "nosave" in sys.argv:
        try:
            pywikibot.showDiff(oldtext , NewText)
        except:
            outbotnew( ' -mdwiki cant showDiff' )
        return False
    #---
    if sys.argv and "workibrahem" in sys.argv : 
        summary = ''
    #if oldtext != NewText or summary :
    if oldtext != NewText :
        #if Ask:
        if not Save_2020[1] and ( Ask or "ask" in sys.argv ) and not "save" in sys.argv :
            #---
            if not "nodiff" in sys.argv:
                try:
                    pywikibot.showDiff(oldtext , NewText)
                except:
                    outbotnew( ' -mdwiki cant showDiff' )
            #---
            outbotnew(' -Edit summary: %s:' % summary )
            sa = py_input('<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Do you want to accept these changes? ([y]es, [N]o, [a]ll): for page %s:%s user:%s'  %(lang,title,r2_params['lgname'] ))
            #---
            if sa == "a":
                outbotnew('<<lightgreen>> ---------------------------------' )
                outbotnew('<<lightgreen>> mdwiki.py save all without asking.' )
                outbotnew('<<lightgreen>> ---------------------------------' )
                Save_2020[1] = True
            #---
            if sa in yes_answer:
                return page_put_new(NewText , summary , title, family = family, lang = lang, minor = minor, nocreate = nocreate,tags=tags , basetimestamp = basetimestamp, returntrue = returntrue)
            else:
                outbotnew( ' mdwiki/mdpy/mdwiki_api.py: wrong answer' )
            #return sa
        else:
            outbotnew(' -Edit summary: %s:' % summary )
            return page_put_new(NewText , summary , title, family = family, lang = lang, minor = minor, nocreate = nocreate,tags=tags , basetimestamp = basetimestamp, returntrue = returntrue)
    else:
        outbotnew('No changes in "%s"' % title)
        outbotnew( '<<lightyellow>> mdwiki/mdpy/mdwiki_api.py: No changes were needed on "%s:%s".'     % (family , title))
        return 'No changes'
    #---
    return False
#---
def move(From , to , reason , lang = 'ar'  , nosleep = False ):
    #---
    outbotnew('<<lightyellow>> ** move .. [[%s:%s]] to [[%s]] ' % (lang , From , to) )
    Params = {
        "action": "move",
        "format": "json",
        #"maxlag": ar_lag[1],
        "from": From,
        "to": to,
        "movetalk": 1,
        #"reason": reason,
        #"bot": Bot_or_himo[1],
        "token": SS["r3_token"],
        "utf8": 1
    }
    #---
    outbotnew(' -Edit reason: %s:' % reason )
    #---
    if From == to:
        outbotnew('<<lightred>>** From == to %s ' % to )
        return False
    #---
    JustMove = True
    #---
    if not Save_2020[1] and "ask" in sys.argv :
        sa = py_input('<<lightyellow>>mdwiki/mdpy/mdwiki_api.py: Do you move page:[[%s:%s]] to [[%s]]? ([y]es, [N]o, [a]ll): user:%s' % (lang,From,to,r2_params['lgname'] ))
        #---
        if sa == "a":
            outbotnew('<<lightgreen>> ---------------------------------' )
            outbotnew('<<lightgreen>> mdwiki.py move all without asking.' )
            outbotnew('<<lightgreen>> ---------------------------------' )
            Save_2020[1] = True
        #---
        if not sa in yes_answer:
            JustMove = False
            outbotnew( ' mdwiki/mdpy/mdwiki_api.py: wrong answer' )
        #return sa
    #---
    if JustMove:
        r4 = post(Params)
        #---
        if 'Success' in r4.text or "redirectcreated" in r4.text:
            outbotnew('<<lightgreen>>** true .. ' + '[[' + to + ']] ' )
            outbotnew( 'تم بنجاح... time.sleep(%d) ' % 7 )
            if nosleep :
                time.sleep(7)
            return True
        elif "Please wait some time and try again" in r4.text or "ratelimited" in r4.text:
            outbotnew(r4.text)
            if nosleep :
                time.sleep(7)
            return move(From , to , reason , lang = lang )
        elif "Please choose another name." in r4.text:
            outbotnew(r4.text)
            return "Please choose another name."
        else:
            return outbot(r4.text)
            #outbotnew(r4.text)
    return False
#---
def Find_pages_exists_or_not( liste ) :
    #---
    params = {
        "action": "query",
        "format": "json",
        "titles": '|'.join( liste ),
        #"redirects": 0,
        #"prop": "templates|langlinks",
        "utf8": 1,
        #"normalize": 1,
    }
    #---
    table = {}
    #---
    json1 = post(params)
    #---
    if json1:
        query_pages = json1.get("query",{}).get("pages",{})
        for page in query_pages:
            kk = query_pages[page]
            faso = ''
            if "title" in kk:
                tit = kk.get("title","")
                #---
                if "missing" in kk:
                    table[tit] = False
                else:
                    table[tit] = True
        #---
    return table
#---
def get_redirect( liste ) :
    #---
    params = {
        "action": "query",
        "format": "json",
        "titles": '|'.join( liste ),
        "redirects": 1,
        #"prop": "templates|langlinks",
        "utf8": 1,
        #"normalize": 1,
    }
    #---
    redirects = {}
    #---
    table = {}
    #---
    json1 = post(params)
    #---
    if json1:
        redd = json1.get("query",{}).get("redirects", [])
        for red in redd:
            redirects[ red["from"] ] = red["to"]
        #---
    return redirects
#---
# end of mdwiki.py file
#---
#---
#if __name__ == '__main__':
    #Find_pages_exists_or_not( [] )
    #Add_To_Head(texto , "بوت: أضاف [[قالب:بلد قرن]]" , "تصنيف:القرن_1_في_الدين", True
    #for cat in OPOPO:
    #move(cat , OPOPO[cat] , "بوت: نقل تصنيف خاطئ")
    #wordcount( "كاتب_(توضيح)" )
    #Get_revisions("اليمن")
    #page_put('Q4115189' , 'P360' ,'Q805', 'P20' , '')
    #Claim_API_With_Quall('Q4115189' , 'P360' ,'Q805', '' , 'P20')
    #Claim_API_With_Quall('Q4115189' , 'P360' ,'Q805', 'P1659' , 'P19')
    #Claim_API_With_Quall('Q4115189' , 'P461' ,'Q32662576', 'P1013' , 'Q21012س909')
    #Merge('Q32660735' , 'Q18340037' )
    #Mergehistory('Q9217925' , 'Q32648455' )
    #Des_API( 'Q31301007', 'تل في ألمانيا' , 'ar' )
#---