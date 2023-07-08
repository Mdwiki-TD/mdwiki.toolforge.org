#!/usr/bin/python

"""
بوت قواعد البيانات
#---
from mdpy.bots import wiki_sql
#---
# result = wiki_sql.sql_new(qua, wiki)
#---
"""
#
# (C) Ibrahem Qasim, 2023
#
#
from pywikibot import config
import re
import json
import codecs
import pywikibot
import string
import sys
import urllib
import urllib.request
import urllib.parse
#---
import time as tttime
import datetime
from datetime import datetime
#---
from mdpy import printe
#---
from new_api import sql_qu
can_use_sql_db = sql_qu.can_use_sql_db
# results = sql_qu.make_sql_connect( query, db='', host='', update=False, Return=[], return_dict=False)
#---
def GET_SQL():
    return can_use_sql_db[1]
#---        
content_lang_map = {
    "be-x-old" : "be-tarask",
    "be_x_old" : "be-tarask",
    "bh" : "bho",
    "crh" : "chr-latn",
    "no" : "nb",
    "als"   :   "gsw",
    "bat-smg"   :   "sgs",
    "cbk-zam"   :   "cbk",
    "eml"   :   "egl",
    "fiu-vro"   :   "vro",
    "map-bms"   :   "jv-x-bms",
    "nrm"   :   "nrf",
    "roa-rup"   :   "rup",
    "roa-tara"  :   "nap-x-tara",
    "simple"    :   "en-simple",
    "zh-classical"  :   "lzh",
    "zh-min-nan"    :   "nan",
    "zh-yue"    :   "yue",
}
#---
def make_labsdb_dbs_p(wiki):
    #---
    lang = wiki
    #---
    if lang.endswith('wiki') : lang = lang[:-4]
    #---
    if lang in content_lang_map:
        wiki = content_lang_map[lang]
    #---
    wiki = f"{wiki}wiki"
    dbs = wiki
    #---
    host = "%s.analytics.db.svc.wikimedia.cloud" % wiki
    #---
    dbs_p = dbs + '_p'
    #---
    # _host_    =   config.db_hostname_format.format(wiki)
    # if host != _host_:  pywikibot.output(f'<<lightyellow>>host:{host} != _host:{_host_}')
    #---
    # _dbs_p_   =   config.db_name_format.format(wiki) + '_p'
    # if dbs_p != _dbs_p_:    pywikibot.output(f'dbs_p:{dbs_p} != _dbs_p:{_dbs_p_}')
    #---
    return host, dbs_p
#---
def Make_sql_many_rows(queries, wiki="", printqua=False, return_dict=False):
    #---
    printe.output(f"wiki_sql.py Make_sql_many_rows wiki '{wiki}'")
    #---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    #---
    if printqua or "printsql" in sys.argv:
        printe.output( queries )
    #---
    if not GET_SQL():
        return []
    #---
    start = tttime.time()
    final = tttime.time()
    #---
    rows = sql_qu.make_sql_connect( queries, db=dbs_p, host=host, return_dict=return_dict)
    #---
    final = tttime.time()
    #---
    delta = int(final - start)
    #---
    printe.output(f'wiki_sql.py Make_sql_many_rows len(encats) = "{len(rows)}", in {delta} seconds')
    #---
    return rows
#---
def sql_new(queries, wiki="", printqua=False):
    #---
    printe.output(f"wiki_sql.py Make_sql_many_rows wiki '{wiki}'")
    #---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    #---
    if printqua or "printsql" in sys.argv:
        printe.output( queries )
    #---
    if not GET_SQL():
        return []
    #---
    start = tttime.time()
    final = tttime.time()
    #---
    rows = sql_qu.make_sql_connect( queries, db=dbs_p, host=host, return_dict=True)
    #---
    final = tttime.time()
    #---
    delta = int(final - start)
    #---
    printe.output(f'wiki_sql.py Make_sql_many_rows len(encats) = "{len(rows)}", in {delta} seconds')
    #---
    return rows
#---