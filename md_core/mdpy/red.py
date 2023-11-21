#!/usr/bin/python3
"""

نسخ التحويلات من الإنجليزية إلى mdwiki

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import sys
import codecs
import requests

# ---
from new_api.mdwiki_page import MainPage, NEW_API
from mdpy import printe
from mdpy.bots import py_tools
from mdpy.bots import mdwiki_api
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
Session = requests.Session()
# ---
offset = {1: 0}
# ---
to_make = {}
# ---
for arg in sys.argv:
    arg, _, value = arg.partition(':')
    # ---
    if (arg.lower() == 'offset' or arg.lower() == '-offset') and value.isdigit():
        offset[1] = int(value)
# ---
# from export import * # export_en_history( title )
# ---
api_new = NEW_API('www', family='mdwiki')
api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# pages   = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)


def get_red(title):
    # ---
    params = {
        "action": "query",
        "format": "json",
        "prop": "redirects",
        "titles": title,
        "utf8": 1,
        "rdprop": "title",
        # "rdprop": "pageid|title",
        "rdlimit": "max",
    }
    # ---
    # result = { "batchcomplete": "", "query": { "pages": { "1369": { "pageid": 1369, "ns": 0, "title": "اليمن", "redirects": [ { "ns": 0, "title": "جمهورية يمنية" } ] } } }, "limits": { "redirects": 500 } }
    # ---
    lista = []
    # ---
    r22 = Session.post('https://' + 'en.wikipedia.org/w/api.php', data=params)
    json1 = r22.json()
    # ---
    pages = json1.get('query', {}).get('pages', {})
    # ---szs
    for x in pages:
        title = pages[x].get('title', '')
        redirectsn = pages[x].get('redirects', [])
        printe.output(redirectsn)
        if pages[x]["title"] == title:
            for io in redirectsn:
                if io["ns"] != 0:
                    continue
                # ---
                if io["title"] not in lista:
                    lista.append(io["title"])
    # ---
    return lista


def work(title, num, lenth, From=''):
    # ---
    printe.output('-------------------------------------------\n*<<lightyellow>> >%d/%d title:"%s".' % (num, lenth, title))
    # ---
    if num < offset[1]:
        return ""
    # ---
    page = MainPage(title, 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        printe.output(f" page:{title} not exists in mdwiki.")
        return ""
    # ---
    redirects = get_red(title)
    # ---
    printe.output(redirects)
    # ---
    text = f'#redirect [[{title}]]'
    sus = f'Redirected page to [[{title}]]'
    # ---
    ing = mdwiki_api.Find_pages_exists_or_not(redirects)
    # ---
    num = 0
    for tit, o in ing.items():
        num += 1
        if o:
            printe.output("page n:%d, title:'%s' already in mdwiki.org.." % (num, tit))
            continue
        # ---
        if not valid_title(tit):
            continue
        # ---
        mdwiki_api.create_Page(text, sus, tit, False, family="mdwiki", sleep=1)


def main():
    printe.output('*<<lightred>> > main:')
    # ---
    # python3 red.py -page:Allopurinol
    # python3 red.py -page:Activated_charcoal_\(medication\)
    # python3 red.py -newpages:10
    # python red.py -newpages:1000
    # python red.py -newpages:20000
    # ---
    page2 = ''
    From = '0'
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        arg = arg.lower()
        # ---
        if arg == "-from":
            From = py_tools.ec_de_code(value, 'decode')
        # ---
        if arg == "-page2" or arg == "page2":
            page2 = py_tools.ec_de_code(value, 'decode')
    # ---
    if page2 != '' and From != '':
        work(page2, 0, 1, From=From)
    # ---
    user = ''
    user_limit = '3000'
    # ---
    searchlist = {
        "drug": "insource:/https\\:\\/\\/druginfo\\.nlm\\.nih\\.gov\\/drugportal\\/name\\/lactulose/",
    }
    # ---
    limite = 'max'
    starts = ''
    # ---
    pages = []
    # ---
    namespaces = '0'
    newpages = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        arg = arg.lower()
        # ---
        if arg == "-limit" or arg == "limit":
            limite = value
        # ---
        if arg == "-userlimit" or arg == "userlimit":
            user_limit = value
        # ---
        if arg == "-page" or arg == "page":
            pages.append(value)
        # ---
        if arg == "-page2" or arg == "page2":
            value = py_tools.ec_de_code(value, 'decode')
            pages.append(value)
        # ---
        if arg == 'newpages' or arg == '-newpages':
            newpages = value
        # ---
        # python red.py -ns:0 -usercontribs:Edoderoobot
        # python red.py -ns:0 -usercontribs:Ghuron
        if arg == "-user" or arg == "-usercontribs":
            user = value
        # ---
        # python red.py -start:!
        if arg == 'start' or arg == '-start':
            starts = value
        # ---
        if arg == "-ns":
            namespaces = value
        # ---
        # python red.py -file:mdwiki/list.txt
        # python3 red.py -file:mdwiki/list.txt
        if arg == "-file":
            # ---
            # if value == 'redirectlist.txt' :
            # value = '/data/project/mdwiki/public_html/redirectlist.txt'
            # ---
            text2 = codecs.open(value, 'r', 'utf8')
            text = text2.read()
            for x in text.split("\n"):
                pages.append(x.strip())
        # ---
        # python red.py -ns:0 search:drug
        if arg == 'search':
            if value in searchlist:
                value = searchlist[value]
            # ---
            ccc = api_new.Search(value=value, ns="0", srlimit="max")
            for x in ccc:
                pages.append(x)
        # ---
    # ---
    start_done = starts
    okay = True
    # ---
    if starts == 'all':
        while okay == True:
            # ---
            if starts == start_done:
                okay = False
            # ---
            # python red.py -start:all
            #
            # ---
            list = api_new.Get_All_pages(start='', namespace=namespaces, limit=limite)
            start_done = starts
            num = 0
            for page in list:
                num += 1
                work(page, num, len(list))
                # ---
                starts = page
    # ---
    if starts != '':
        listen = api_new.Get_All_pages(start=starts, namespace=namespaces, limit=limite)
        num = 0
        for page in listen:
            num += 1
            work(page, num, len(listen))
            # ---
    # ---
    list = []
    # ---
    if newpages != "":
        list = api_new.Get_Newpages(limit=newpages, namespace=namespaces)
    elif user != "":
        list = mdwiki_api.Get_UserContribs(user, limit=user_limit, namespace=namespaces, ucshow="new")
    elif pages != []:
        list = pages
    # ---
    num = 0
    for page in list:
        num += 1
        work(page, num, len(list))
    # ---
    # '''
    # ---
    if starts == 'all':
        while okay == True:
            # ---
            if starts == start_done:
                okay = False
            # ---
            # python red.py -start:all
            #
            # ---
            list = api_new.Get_All_pages(start='', namespace=namespaces, limit=limite)
            start_done = starts
            num = 0
            for page in list:
                num += 1
                work(page, num, len(list))
                # ---
                starts = page
    # ---
    elif starts != '':
        # while start_done != starts :
        while okay == True:
            # ---
            if starts == start_done:
                okay = False
            # ---
            # python red.py -start:! -limit:3
            #
            # ---
            list = api_new.Get_All_pages(start=starts, namespace=namespaces, limit=limite)
            start_done = starts
            num = 0
            for page in list:
                num += 1
                work(page, num, len(list))
                # ---
                starts = page


if __name__ == "__main__":
    main()
