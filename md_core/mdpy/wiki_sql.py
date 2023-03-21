#!/usr/bin/python

"""
بوت قواعد البيانات

    $content_lang_map = array(
        'als' => 'gsw',
        'bat-smg' => 'sgs',
        'be-x-old' => 'be-tarask',
        'bh' => 'bho',
        'crh' => 'chr-latn',
        'fiu-vro' => 'vro',
        'no' => 'nb',
        'roa-rup' => 'rup',
        'simple' => 'en',
        'zh-classical' => 'lzh',
        'zh-min-nan' => 'nan',
        'zh-yue' => 'yue',
    );
"""
#
# (C) Ibrahem Qasim, 2022
#
#
from pywikibot import config
import re
import json
import codecs
from warnings import warn
import pywikibot
import string
import sys
import urllib
import urllib.request
import urllib.parse
#---
import time as tttime
import datetime
from datetime import datetime#, date, time
#---
TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")

#---
can_use_sql_db  = { 1 : False }
SQL_Ready  = False
#---
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
#---
#---
try:
    import MySQLdb
    SQL_Ready = True
    can_use_sql_db[1] = True
except Exception as e:
    pywikibot.output('<<lightred>> mdwiki/mdpy/wiki_sql.py errors when import MySQLdb ')
    pywikibot.output('<<lightred>> %s ' % e)
#---
'''
#---
import wiki_sql
# wiki_sql.GET_SQL()
# wiki_sql.Make_sql_many_rows( queries , wiki="", printqua = False)
#---
'''
#---
def GET_SQL():
    return can_use_sql_db[1]
#---
def Make_sql_many_rows( queries , wiki="", printqua = False):
    rows = []
    #---
    pywikibot.output( "wiki_sql.py Make_sql_many_rows wiki '%s'" % wiki )
    #---
    if printqua or "printsql" in sys.argv:
        pywikibot.output( queries )
    #---
    if not GET_SQL():
        pywikibot.output( 'sql.GET_SQL() == False' )
        return rows
    #---
    start = tttime.time()
    final = tttime.time()
    #delta = int(final - start)
    #pywikibot.output( 'wiki_sql.py Make_sql len(encats) = "{}", in {} seconds'.format( len( encats ) , delta)  )
    #---
    repa = {
        "zh-yuewiki" : "yuewiki",
        "zh-yue" : "yue",
        }
    #---
    if wiki in repa : wiki = repa[wiki]
    #---
    dbs = ''
    #if wiki == "arwiki" : dbs = ar_site.dbName()
    #---
    if wiki == "wikidata" : 
        wiki = "wikidatawiki"
        dbs = "wikidatawiki"
    else:
        dbs = wiki
    #---
    db_user = config.db_username
    dpas    = config.db_password
    #---
    labsdb = "%s.analytics.db.svc.wikimedia.cloud" % wiki
    #---
    TTime = datetime.now().strftime("%Y-%b-%d  %H:%M:%S")
    #---
    dbs_p = dbs + '_p'
    #---
    # pywikibot.output( '<<lightred>> wiki_sql.py <<lightyellow>>labsdb:"%s" , db:"%s" , db_user:"%s" %s' % (labsdb , dbs_p , db_user , TTime) )
    #---
    if SQL_Ready:
        #---
        # MySQLdb.connect with arrgs
        arrgs = {
            'host': labsdb,
            'user': db_user,
            'passwd': dpas,
            'db': dbs_p,
        }
        #---
        # connect to the database server without error
        try:
            cn = MySQLdb.connect(**arrgs)
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return rows
        #---
        cn.set_character_set('utf8')
        cur = cn.cursor()
        #---
        # cur.execute(queries)
        # skip sql errors
        try:
            cur.execute(queries)
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( queries )
            pywikibot.output( 'CRITICAL:' )
            return rows
        #---
        en_results = cur.fetchall()
        cn.close()
        # -----------------
        final = tttime.time()
        # -----------------end of sql--------------------------------------------
        for raw in en_results:
            #if type(raw) == bytes:
                #raw = raw.decode("utf-8")
            raw2 = raw
            if type(raw2) == list or type(raw2) == tuple :
                raw = [ py_tools.Decode_bytes(x) for x in raw2 ]
            rows.append(raw)
    # -----------------
    else:
        pywikibot.output("no SQL_Ready" )
    # -----------------
    delta = int(final - start)
    pywikibot.output( 'wiki_sql.py Make_sql_many_rows len(encats) = "{}", in {} seconds'.format( len( rows ) , delta)  )
    # -----------------
    return rows
#---
