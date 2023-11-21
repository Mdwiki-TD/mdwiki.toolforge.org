#!/usr/bin/python3
"""

إيجاد التحويلات واصلاحها

python3 core8/pwb.py mdpy/fixred

"""
#
# (C) Ibrahem Qasim, 2022
#
#
# ---
import re
import sys
from mdpy.bots import mdwiki_api
from mdpy import printe

# ---
NewList = {}


def printtest(s):
    if 'test' in sys.argv:
        print(s)


# ---
redirects_pages = mdwiki_api.Get_All_pages('!', namespace='0', apfilterredir='redirects')
print(f'len of redirects_pages {len(redirects_pages)} ')
# ---
nonredirects = mdwiki_api.Get_All_pages('!', namespace='0', apfilterredir='nonredirects')
# nonredirects = []
printe.output(f'len of nonredirects {len(nonredirects)} ')
# printe.output( str(nonredirects) )
# ---
# fatosha = codecs.open( 'mdwiki/date_before_20200701.txt' , "r", encoding="utf-8").read()
# fatosha = [ x.replace('[[','').split(']]')[0].strip() for x in fatosha.split('\n') ]
# ---
# listo = [ x for x in listo if not x in fatosha ]
# print( dd )
# ---
from_to = {}
normalized = {}
# ---
from mdpy.bots import py_tools


def find_redirects(links):
    # ---
    # titles = [ x for x in links if links[x].get('ns','') == '0' ]
    titles = []
    for x in links:
        if x not in from_to:
            ns = links[x].get('ns', '')
            if str(ns) == '0':
                titles.append(x)
            else:
                printe.output('ns:' + str(ns))
    # ---
    oldlen = len(from_to.items())
    # ---
    normalized_numb = 0
    # ---
    for i in range(0, len(titles), 300):
        group = titles[i : i + 300]
        # ---
        # printe.output(group)
        # ---
        line = "|".join(group)
        # ---
        params = {"action": "query", "format": "json", "prop": "redirects", "titles": line, "redirects": 1, "converttitles": 1, "utf8": 1, "rdlimit": "max"}
        # ---
        jsone = mdwiki_api.post(params)
        # ---
        if jsone:
            # ---
            query = jsone.get("query", {})
            # ---
            # "normalized": [{"from": "tetracyclines","to": "Tetracyclines"}]
            normal = query.get("normalized", [])
            for nor in normal:
                normalized[nor["to"]] = nor["from"]
                normalized_numb += 1
                # printe.output('normalized["%s"] = "%s"' % ( nor["to"] , nor["from"] ) )
            # ---
            # "redirects": [{"from": "Acetylsalicylic acid","to": "Aspirin"}]
            Redirects = query.get("redirects", [])
            for red in Redirects:
                from_to[red["from"]] = red["to"]
                # printe.output('from_to["%s"] = "%s"' % ( red["from"] , red["to"] ) )
            # ---
            # "pages": { "4195": {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]} }
            pages = query.get("pages", {})
            # ---
            for page in pages:
                # tab = {"pageid": 4195,"ns": 0,"title": "Aspirin","redirects": [{"pageid": 4953,"ns": 0,"title": "Acetylsalicylic acid"}]}
                tab = pages[page]
                for pa in tab.get('redirects', []):
                    from_to[pa["title"]] = tab["title"]
                    # printe.output('<<lightyellow>> from_to["%s"] = "%s"' % ( pa["title"] , tab["title"] ) )
            # ---
        else:
            printe.output(" no jsone")
    # ---
    newlen = len(from_to.items())
    nn = int(newlen) - int(oldlen)
    # ---
    printe.output("def find_redirects: find %d lenth" % nn)
    # printe.output( "def find_redirects: find %d for normalized" % normalized_numb )


def replace_links2(text, oldlink, newlink):
    # ---
    oldlink2 = normalized.get(oldlink, oldlink)
    # ---
    while text.find(f'[[{oldlink}]]') != -1 or text.find(f'[[{oldlink}|') != -1 or text.find(f'[[{oldlink2}]]') != -1 or text.find(f'[[{oldlink2}|') != -1:
        # ---
        printe.output(f"text.replace( '[[{oldlink}]]' , '[[{newlink}|{oldlink}]]' )")
        # ---
        text = text.replace(f'[[{oldlink}]]', f'[[{newlink}|{oldlink}]]')
        text = text.replace(f'[[{oldlink}|', f'[[{newlink}|')
        # ---
        text = re.sub(r'\[\[%s(\|\]\])' % oldlink, r'[[%s\g<1>' % newlink, text, flags=re.IGNORECASE)
        # ---
        if oldlink != oldlink2:
            text = re.sub(r'\[\[%s(\|\]\])' % oldlink2, r'[[%s\g<1>' % newlink, text, flags=re.IGNORECASE)
            text = text.replace(f'[[{oldlink2}]]', f'[[{newlink}|{oldlink2}]]')
            text = text.replace(f'[[{oldlink2}|', f'[[{newlink}|')
    # ---
    return text


def treat_page(title):
    """Change all redirects from the current page to actual links."""
    # links = current_page.linkedPages()
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    # links = [ { 'ns' : "0" , 'title' : "title" } ]
    links = mdwiki_api.Get_page_links(title, namespace="0", limit="max")
    # ---
    # "normalized": [{"from": "tetracyclines","to": "Tetracyclines"}]
    normal = links.get("normalized", [])
    printe.output(f'find {len(normal)} normalized..')
    for nor in normal:
        normalized[nor["to"]] = nor["from"]
        printe.output(f"normalized[\"{nor['to']}\"] = \"{nor['from']}\"")
    # ---
    newtext = text
    # i = None
    # ---
    changed = 0
    # ---
    # liinks = [ x.replace(x[0], x[0].upper() , 1) for x in links['links'] ]
    liinks = [str.capitalize(x) for x in links['links']]
    # ---
    find_redirects(links['links'])
    # ---
    # for tt , page in links['links'].items() :
    for tt in links['links']:
        # ---
        page = links['links'][tt]
        tit = page['title']
        tit2 = normalized.get(page['title'], page['title'])
        # ---
        fixed_tit = from_to.get(tit) or from_to.get(tit2)
        # ---
        if fixed_tit:
            # fixed_tit2 = normalized.get( fixed_tit , fixed_tit )
            # ---
            # fix_to = from_to.get( title ) or from_to.get( tit2 )
            # if fixed_tit in nonredirects : or fixed_tit2 in nonredirects :
            # ---
            # if fixed_tit in nonredirects :
            newtext = replace_links2(newtext, tit, fixed_tit)
        # else:
        elif tit not in nonredirects:
            if tit2 != tit:
                printe.output(f'<<lightred>> tit:["{tit}"] and tit:["{tit2}"] not in from_to')
            # else:
            # printe.output('<<lightred>> tit:["%s"] not in from_to' % tit )
            # ---
    # ---
    mdwiki_api.page_put(oldtext=text, newtext=newtext, summary='Fix redirects', title=title, returntrue=False, diff=True)


def main():
    # ---
    ttab = []
    # ---
    # python3 fixred.py
    # python  fixred.py test -page:WikiProjectMed:List ask
    # python  fixred.py test -page:User:Mr._Ibrahem/sandbox
    # python3 fixred.py test -page:Tetracycline_antibiotics
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg == "-page2" or arg == "page2":
            value = py_tools.ec_de_code(value.strip(), 'decode')
            ttab.append(value.strip())
        # ---
        if arg == "-page":
            ttab.append(value)
    # ---
    if ttab == [] or ttab == ['all']:
        ttab = nonredirects
    # ---
    for title in ttab:
        treat_page(title)

    # ---


# ---
if __name__ == '__main__':
    main()
# ---
