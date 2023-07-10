#!/usr/bin/python

"""
بوت قواعد البيانات

python3 core8/pwb.py mdpy/wddone

"""
#
# (C) Ibrahem Qasim, 2022
#
#
#---
from mdpy.bots import sql_for_mdwiki
from pymysql.converters import escape_string

#---
from mdpy.bots import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# escape_string(string)
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
    #---
    mdtit=escape_string(mdtitle)
    tar=escape_string(target)
    user=escape_string(user)
    #---
    done_qu = f"""
        INSERT INTO wddone (mdtitle, target, lang, user)
        SELECT '{mdtit}', '{tar}', '{lang}', '{user}'
        WHERE NOT EXISTS (SELECT 1
            FROM wddone 
                WHERE mdtitle = '{mdtit}'
                AND lang = '{lang}'
                AND user = '{user}'
            )
    """
    #---
    print('**************')
    print(done_qu)
    print('**************')
    #---
    vfg = sql_for_mdwiki.mdwiki_sql(done_qu , update = True)
#---