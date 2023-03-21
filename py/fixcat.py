#!/usr/bin/python

"""
بوت إضافة التصنيف للمقالات بدون تصنيف في قواعد البيانات

python3 pwb.py mdpy/fixcat

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import pywikibot
import sys
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
import mdwiki_api

#---
cat_for_pages = {}
#---
def get_cats_and_pages():
    #---
    sq = sql_for_mdwiki.mdwiki_sql('select category, depth from categories;')
    #---
    catlen = {}
    #---
    RTT_dpl = 0
    #---
    for tab in sq :
        cat     = py_tools.Decode_bytes(tab[0]) 
        depth   = py_tools.Decode_bytes(tab[1])
        #---
        catlen[cat] = 0
        #---
        pages = mdwiki_api.subcatquery(cat, depth=depth, ns="0")
        #---
        for page in pages:
            if page in cat_for_pages :
                if cat != 'RTT':
                    cat_for_pages[page] = cat
                    catlen[cat] += 1
                else:
                    RTT_dpl += 1
            else:
                cat_for_pages[page] = cat
                catlen[cat] += 1
        #---
    #---
    for cat, len in catlen.items():
        pywikibot.output(f'cat: {cat} , len: {len}')
    #---
    pywikibot.output(f'<<lightyellow>> RTT_dpl: {RTT_dpl}')
#---
get_cats_and_pages()
#---
def get_pages_with_no_cat():
    #---
    add_cat = {}
    #---
    ioi = sql_for_mdwiki.mdwiki_sql("select title from pages where cat = '';")
    #---
    for tab in ioi :
        title = py_tools.Decode_bytes(tab[0])
        #---
        cat     = cat_for_pages.get(title, '')
        if cat != '':
            add_cat[title] = cat
        #---
    #---
    for tit, cat in add_cat.items():
        #---
        tit2 = py_tools.make_cod(tit)    
        #---
        quanew = f"""UPDATE pages SET cat = '{cat}' WHERE title = {tit2};"""
        #---
        pywikibot.output('=======================')
        pywikibot.output(quanew)
        #---
        if not 'dont' in sys.argv:
            qu = sql_for_mdwiki.mdwiki_sql(quanew, update = True)
            #---
            pywikibot.output(qu)
#---
if __name__ == '__main__':
    get_pages_with_no_cat()
#---
