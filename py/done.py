#!/usr/bin/python

"""
بوت قواعد البيانات

python3 pwb.py mdpy/sql justsql break
python3 pwb.py mdpy/sql justsql
python3 pwb.py mdpy/sql

"""
#
# (C) Ibrahem Qasim, 2022
#
#
#---
import sql_for_mdwiki
# from sql import *
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
# py_tools.
# py_tools.
# py_tools.
#---
#---
que = '''
select title,user,lang,target
from pages
where target != ""
;'''
#---
sq = sql_for_mdwiki.mdwiki_sql(que)
#---
for tab in sq :
    mdtitle = py_tools.Decode_bytes(tab[0]) 
    user    = py_tools.Decode_bytes(tab[1])
    lang    = py_tools.Decode_bytes(tab[2]).lower()
    target  = py_tools.Decode_bytes(tab[3])
    done_qu= """
INSERT INTO wddone (mdtitle, target, lang, user)
SELECT {mdtit}, {tar}, '{lang}', {user}
WHERE NOT EXISTS (SELECT 1
    FROM wddone 
        WHERE mdtitle = {mdtit}
        AND lang = '{lang}'
        AND user = {user}
            )
    """.format(
    #---
    mdtit=py_tools.make_cod(mdtitle), tar=py_tools.make_cod(target), lang=lang, user=py_tools.make_cod(user))
    #---
    print('**************')
    print(done_qu)
    print('**************')
    #---
    vfg = sql_for_mdwiki.mdwiki_sql(done_qu , update = True)
#---