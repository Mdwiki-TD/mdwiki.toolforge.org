#!/usr/bin/python3
"""
بوت قواعد البيانات
# ---
from mdpy.bots import wiki_sql
# ---
# result = wiki_sql.sql_new(qua, wiki)
# ---
"""
#
# (C) Ibrahem Qasim, 2023
#
#

import sys

# ---
import time as tttime

# ---
from mdpy import printe

# ---
from new_api import sql_qu

can_use_sql_db = sql_qu.can_use_sql_db
# results = sql_qu.make_sql_connect( query, db='', host='', update=False, Return=[], return_dict=False)


def GET_SQL():
    return can_use_sql_db[1]


def make_labsdb_dbs_p(wiki):  # host, dbs_p = make_labsdb_dbs_p('ar')
    # ---
    if wiki.endswith('wiki'):
        wiki = wiki[:-4]
    # ---
    wiki = wiki.replace("-", "_")
    # ---
    databases = {
        "be-x-old": "be_x_old",
        "be_tarask": "be_x_old",
        "be-tarask": "be_x_old",
    }
    # ---
    wiki = databases.get(wiki, wiki)
    # ---
    wiki = f"{wiki}wiki"
    dbs = wiki
    # ---
    host = f"{wiki}.analytics.db.svc.wikimedia.cloud"
    # ---
    dbs_p = dbs + '_p'
    # ---
    return host, dbs_p


def Make_sql_many_rows(queries, wiki="", printqua=False, return_dict=False):
    # ---
    printe.output(f"wiki_sql.py Make_sql_many_rows wiki '{wiki}'")
    # ---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    if printqua or "printsql" in sys.argv:
        printe.output(queries)
    # ---
    if not GET_SQL():
        return []
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    rows = sql_qu.make_sql_connect(queries, db=dbs_p, host=host, return_dict=return_dict)
    # ---
    final = tttime.time()
    # ---
    delta = int(final - start)
    # ---
    printe.output(f'wiki_sql.py Make_sql_many_rows len(encats) = "{len(rows)}", in {delta} seconds')
    # ---
    return rows


def sql_new(queries, wiki="", printqua=False):
    # ---
    printe.output(f"wiki_sql.py Make_sql_many_rows wiki '{wiki}'")
    # ---
    host, dbs_p = make_labsdb_dbs_p(wiki)
    # ---
    if printqua or "printsql" in sys.argv:
        printe.output(queries)
    # ---
    if not GET_SQL():
        return []
    # ---
    start = tttime.time()
    final = tttime.time()
    # ---
    rows = sql_qu.make_sql_connect(queries, db=dbs_p, host=host, return_dict=True)
    # ---
    final = tttime.time()
    # ---
    delta = int(final - start)
    # ---
    printe.output(f'wiki_sql.py Make_sql_many_rows len(encats) = "{len(rows)}", in {delta} seconds')
    # ---
    return rows


# ---
