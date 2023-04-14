#!/usr/bin/python

"""

تجميع المراجع في الصفحات

python3 pwb.py mdpy/wpref -lang:es ask savetofile
python3 pwb.py mdpy/wpref -lang:or ask -page:ପାଟେଲୋଫିମୋରାଲ_ଯନ୍ତ୍ରଣା_ସିଣ୍ଡ୍ରୋମ
python3 pwb.py mdpy/wpref -lang:or ask -page:ପୋଷ୍ଟିରିଅର_ୟୁରେଥ୍ରାଲ_ଭଲଭ ask
python3 pwb.py mdpy/wpref -lang:or -page:user:Mr._Ibrahem/sandbox ask

python3 pwb.py mdpy/wpref -lang:ro ask


python3 pwb.py mdpy/wpref ask

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re
import json
import codecs
import string
import urllib
import os
import sys
sys.dont_write_bytecode = True
import requests
#---
# newtext = fix_page(text,title, move_dots= move_dot[1], infobox = False)
#---
if 'returnfile' in sys.argv:
    from wpref_text import fix_page
else:
    from warnings import warn
    import pywikibot
    import printe
    #---
    import sql_for_mdwiki
    # sql_for_mdwiki.mdwiki_sql(query , update = False)
    from mdpy.wpref_text import fix_page
#---
SS = { "token" : '' }
session = {}
session[1] = requests.Session()
session["url"] = ""
#---
Url_To_login = { 1 : '' , 'not' : True }
#---
login_done = { 1 : False }
reffixed_file = { 1 : '' }
#---
move_dot = { 1 : False }
expend_infobox = { 1 : False }
#---
project = '/data/project/mdwiki'
#---
if not os.path.isdir(project): project = 'I:/mdwiki'
#---
setting = {}
#---
fixwikirefs = project + '/confs/fixwikirefs.json'
#---
if os.path.isfile(fixwikirefs):
    try:
        setting = json.load(codecs.open(fixwikirefs, "r", encoding="utf-8-sig"))
        # print(setting)
    except Exception as e:
        setting = {}
        # print(f'err:{e} ...')
# else:
    # print(f'fixwikirefs:{fixwikirefs} not file...')
#---
def print_s(s):
    if not 'returnfile' in sys.argv:
        printe.output(s)
#---
def ec_de_code( tt , type ):
    fao = tt
    if type == 'encode' :
        #fao = encode_arabic(tt)
        fao = urllib.parse.quote(tt)
    elif type == 'decode' :
        fao = urllib.parse.unquote(tt)
    return fao
#---
def make_ref_done_list():
    #---
    reffixed_file[1] = project + '/md_core/mdpy/reffixed.csv'
    reffixed = ''
    #---
    try:
        with codecs.open(reffixed_file[1], "r", encoding="utf-8-sig") as mama:
            reffixed = mama.read()
        mama.close()
    except Exception as e:
        if not 'returnfile' in sys.argv:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
    #---
    reffixed_List = [ x.strip() for x in reffixed.split('\n') if x.strip() != '' ]
    #---
    return reffixed_List
#---
reffixed_List = make_ref_done_list()
#---
def log( lang ) :
    #---
    if login_done[1] == lang : return ''
    #---
    api_urle = 'https://%s.wikipedia.org/w/api.php' % lang
    #---
    Url_To_login[1] = api_urle
    #---
    session[1] = requests.Session()
    #---
    #if api_urle != session["url"]: print_s( "himoBOT3.py: log to %s. user:%s" % (api_urle , username)  )
    #---
    session["url"] = api_urle
    session["family"] = 'wikipedia'
    session["lang"] = lang
    #---
    # get login token
    r1 = session[1].get(api_urle, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
    })
    r1.raise_for_status()
    # log in
    #passe = wd_password
    #---
    #if api_urle == en_url:
        #passe = en_password
    #--- 
    #elif api_urle == wd_url:
        #passe = wd_password
    #---
    r2 = session[1].post(api_urle, data={
        'format': 'json',
        'action': 'login',
        'lgname': 'Mr. Ibrahem',
        'lgpassword': 'Mr._Ibrahem@9usrv463ql983qrulnani14t3hqs1g27',
        'lgtoken': r1.json()['query']['tokens']['logintoken'],
    })
    #---
    print_s(r2)
    if r2.json()['login']['result'] != 'Success':
        print_s(r2.json()['login']['reason'])
        #raise RuntimeError(r2.json()['login']['reason'])
    else:
        print_s('wpref.py login Success to %s.wikipedia.org' % lang)
        login_done[1] = lang
    #---
    #if r2.json()['login']['result'] != 'Success': print(r2.json()['login']['reason'])
        #raise RuntimeError(r2.json()['login']['reason'])
    # get edit token
    r3 = session[1].get(api_urle, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
    })
    #---
    token = r3.json()['query']['tokens']['csrftoken']
    #---
    session["token"] = token
#---
def Gettoken():
    return session["token"]
#---
def submitAPI( params, lang='', Type = 'post'):
    #---
    log( lang )
    #---
    json1 = {}
    #---
    if "token" in params and params["token"] == "":
        params["token"] = session["token"]
    #---
    r4_text = ''
    #---
    try:
        if Type == 'post':
            r4 = session[1].post(session["url"], data=params)
        else:
            r4 = session[1].get(session["url"], data=params)
        #---
        r4_text = r4.text
    except Exception as e:
        print_s(f'submitAPI r4 Error {e}')
        return json1
    #---
    if r4_text != '':
        try:
            json1 = json.loads( r4_text )
        except Exception as e:
            print_s(f'submitAPI Error {e}')
            # print_s(r4_text)
            print_s(params)
            return json1
    #---
    return json1
#---
missingtitles = {}
#---
def GetPageText(title, lang='', Print = True):
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
    json1 = submitAPI(params, lang = lang)
    #---
    if not json1 or type(json1) != dict : 
        if Print: 
            print_s('json1 ==:' )
            print_s( json1 )
        return ''
    #---
    if json1 == {}:
        if Print: print_s('json1 == {}' )
        return ''
    #---
    err = json1.get('error', {}).get('code', {})
    # {'error': {'code': 'missingtitle', 'info': "The page you specified doesn't exist.", '*': 'See https://fr.wikipedia.org/w/api.php for API usag Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimed.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1362'}
    #---
    if err == 'missingtitle':
        missingtitles[title] = lang
    #---
    parse = json1.get('parse', {})
    if parse == {}:
        if Print: 
            print_s('parse == {}' )
            print_s(json1)
        return ''
    #---
    text = parse.get('wikitext', {}).get('*','')
    #---
    if text == "" :
        if Print: print_s('page %s text == "".' % title )
    #---
    return text
#---
yes_answer = [ "y" , "a" , "" , "Y" , "A", "all"]
#---
ask_a = { 1 : False }
#---
def page_put(oldtext, NewText, summary, title, lang):
    #---
    if "ask" in sys.argv and not ask_a[1]:
        pywikibot.showDiff(oldtext , NewText)
        #---
        print_s(' -Edit summary: %s:' % summary )
        sa = pywikibot.input('<<lightyellow>>mdwiki/wpref.py: Do you want to accept these changes? ([y]es, [N]o, [a]ll): for page (%s:%s)' % (lang , title))
        #---
        if sa == "a" or sa == "all":
            ask_a[1] = True
            print_s(' <<lightgreen>>mdwiki/wpref.py: All changes accepted.')
            print_s(' <<lightgreen>>mdwiki/wpref.py: All changes accepted.')
        #---
        if not sa in yes_answer:
            print_s( "wrong answer" )
            return False
    #---
    pparams = {
        "action": "edit",
        "format": "json",
        #"maxlag": ar_lag[1],
        "title": title,
        "text": NewText,
        "summary": summary,
        #"starttimestamp": starttimestamp,
        #"minor": minor,
        #"notminor": 1,
        "bot": 1,
        "nocreate": 1,
        "token": session["token"] ,
    }
    #---
    r4 = session[1].post(session["url"], data=pparams)
    #---
    text = ''
    try:
        text = json.loads(r4.text)
    except:
        print_s("error when json loads r4.text")
    #---
    if 'Success' in r4.text:
        print_s('<<lightgreen>> ** true .. ' + '[[%s:%s:%s]]' % (session["lang"] , session["family"] ,title)  )
        return True
    #---
    else:
        print_s(r4.text)
    #---
    if 'savetofile' in sys.argv:
        with codecs.open( project + '/md_core/mdpy/wpref_1.txt' , "w", encoding="utf-8") as ggg:
            ggg.write( NewText )
        ggg.close()
    #---
    return False
#---
def fix_page_here(text, title, langcode):
    newtext = text
    #---
    section_0_text = ''
    #---
    lang_default = setting.get(langcode, {})
    #---
    dots = move_dot[1] 
    if lang_default.get('move_dots', 0) == 1 :  dots = True
    #---
    expend = expend_infobox[1]
    if lang_default.get('expend', 0) == 1 : expend = True
    #---
    adden = False
    if lang_default.get('add_en_lang', 0) == 1 : adden = True
    #---
    newtext = fix_page(newtext, title, move_dots= dots, infobox = expend, section_0 = section_0_text, lang=langcode, add_en_lang=adden)
    #---
    return newtext
#---
def work_one_lang(list, lang):
    #---
    print_s( '<<lightblue>> work on lang: %s.wikipedia......................' % lang )
    #---
    newlist = list
    #---
    if not 'lala' in sys.argv:
        newlist = [ x for x in list if not f"{lang}:{x}" in reffixed_List ]
        dd = int(len(list)) - int(len(newlist))
        print( "already in reffixed_List :%d" % dd )
    #---
    if len(newlist) > 0:
        log( lang )
    #---
    number = 0
    #---
    for title in newlist:
        #---
        lio = '%s:%s' % (lang, title)
        number += 1
        print_s( '<<lightyellow>> %d from %d, page: %s' % (number,len(newlist),lio) )
        #---
        if lio in reffixed_List and not 'lala' in sys.argv:
            print_s( '<<lightred>>\talready in reffixed_List.' )
            continue
        #---
        text = GetPageText(title, lang=lang)
        #---
        if text == '' :
            print_s('\ttext == ""')
            continue
        #---
        newtext = fix_page_here(text, title, lang)
        #---
        donee = False
        #---
        if text != newtext: 
            aa = page_put( text , newtext , 'Fix references, Expend infobox mdwiki.toolforge.org.' , title , lang)
            #---
            if aa :
                donee = True 
        else:
            if 'donee' in sys.argv: donee = True 
        #---
        if donee:
            with codecs.open( reffixed_file[1] , "a", encoding="utf-8") as ggg:
                ggg.write( '\n' + lio )
            ggg.close()
#---
for arg in sys.argv:
    arg, sep, value = arg.partition(':')
    arg = arg[1:] if arg.startswith("-") else arg
    #---
    if arg == 'infobox':    expend_infobox[1] = True
    if arg == 'movedots':   move_dot[1] = True
#---
def maine():
    #---
    page = ''
    lange = ''
    nolange = ''
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        # remove the - from the argument
        arg = arg[1:] if arg.startswith("-") else arg
        #---
        if arg == 'nolang':     nolange = value
        if arg == 'lang':       lange = value
        if arg == 'page':       page = value.replace("_"," ")
    #---
    newtable = {}
    #---
    if page != "" and lange != "":
        newtable[lange] = [page]
    #---
    if page != "" and lange != "" and 'returnfile' in sys.argv:
        #---
        title = ec_de_code( page, 'decode' )
        log( lange )
        text = GetPageText(title, lang=lange, Print = False)
        #---
        if text == '' :
            print('notext')
            return ''
        #---
        newtext = fix_page_here(text, title, lange)
        #---
        if text == newtext: 
            print('no changes')
            return ''
        #---
        if newtext == '' :
            print('notext')
            return ''
        #---
        title2 = title
        title2 = title2.replace(':','-').replace('/','-').replace(' ','_')
        #---
        try:
            filename = project + '/public_html/wprefcash/' + title2 + '.txt'
            with codecs.open( filename , "w", encoding="utf-8") as uy: 
                uy.write( newtext ) 
            uy.close()
            #---
            print(filename)
            #---
        except Exception as e:
            if not 'returnfile' in sys.argv:
                pywikibot.output( 'Traceback (most recent call last):' )
                warn('Exception:' + str(e), UserWarning)
                pywikibot.output( 'CRITICAL:' )
            filename = project + '/public_html/wprefcash/title2.txt'
            with codecs.open( filename, "w", encoding="utf-8") as gf: 
                gf.write( newtext ) 
            gf.close()
            #---
            print(filename)
        #---
        return ''
    #---
    if page == "":
        #---
        que = 'select lang, target from pages where target != "" and lang != "" and lang != "ar";'
        #---
        if nolange != '' : 
            que = que.replace ( 'and lang != ""' , 'and lang != "%s"' % nolange )
        elif lange != '' :
            que = 'select lang, target from pages where target != "" and lang = "%s";' % lange
        #---
        print_s(que)
        #---
        sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
        #---
        for tab in sq :
            lang   = tab['lang']
            target = tab['target']
            #---
            if not lang in newtable : newtable[lang] = []
            if not target in newtable[lang] : newtable[lang].append(target)
    #---
    for lang in newtable:
        work_one_lang( newtable[lang] , lang )
    #---
    if not 'returnfile' in sys.argv:
        print_s( 'find %s pages in missingtitles' % len(missingtitles) )
        for x, lang in missingtitles.items():
            print_s( 'lang: %s, title: %s' % (lang, x) )
    #---
    #---
#---
def tests():
    # python3 pwb.py mdpy/wpref tests
    title = 'Utilizator:Mr._Ibrahem/teste'
    lang = 'ro'
    log( lang )
    #---
    # text = ''''''
    text = GetPageText(title, lang=lang)
    #---
    newtext = fix_page_here(text, title, lang)
    #---
    import pywikibot
    #---
    pywikibot.showDiff( text, newtext )
    #---
#---
if __name__ == '__main__':
    if 'tests' in sys.argv:
        tests()
    else:
        maine()
#---