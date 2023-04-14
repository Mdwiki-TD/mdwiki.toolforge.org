#!/usr/bin/python
"""

بوت قواعد البيانات

from new_api import sql_qu
can_use_sql_db = sql_qu.can_use_sql_db
results = sql_qu.make_sql_connect( query, db='', host='', update=False, Return=[], return_dict=False)
"""
#
# (C) Ibrahem Qasim, 2023
#
#
from pywikibot import config
import re
import sys
import os
#---
import pywikibot
from warnings import warn
import string
sys.dont_write_bytecode = True
#---
import pymysql
import pymysql.cursors
import pkg_resources
#---
py_v = pymysql.__version__
if py_v.endswith('.None'): py_v = py_v[:-len('.None')]
#---
pymysql_version = pkg_resources.parse_version(py_v)
pywikibot.output(f'<<lightyellow>> pymysql_version: {pymysql_version}')
#---
db_username = config.db_username
db_password = config.db_password
#---
can_use_sql_db  = { 1 : True }
#---
if not os.path.isdir('/mnt/nfs/labstore-secondary-tools-project/'): can_use_sql_db[1] = False
#---
def sql_connect_pymysql( query, db='', host='', update=False, Return=[], return_dict=False):
    #---
    pywikibot.output('start sql_connect_pymysql:')
    #---
    args = {
        'host':     host,
        'user':     db_username,
        'passwd':   db_password,
        'db':       db,
        'charset':  'utf8mb4',
        'use_unicode': True,
    }
    #---
    params = None
    #---
    # connect to the database server without error
    #---
    Typee = pymysql.cursors.Cursor
    if return_dict:
        Typee = pymysql.cursors.DictCursor
    #---
    try:
        connection = pymysql.connect(
            host=args['host'],
            user=args['user'],
            password=args['passwd'],
            db=args['db'],
            charset=args['charset'],
            cursorclass=Typee,
            autocommit=True
            )

    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return Return
    #---
    if pymysql_version < pkg_resources.parse_version('1.0.0'):
        from contextlib import closing
        connection = closing(connection)
    #---
    with connection as conn, conn.cursor() as cursor:
        #---
        # skip sql errors
        try:
            cursor.execute(query, params)

        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return Return
        #---
        results = Return
        #---
        try:
            results = cursor.fetchall()

        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return Return
        #---
        # yield from cursor
        return results
#---
def make_sql_connect( query, db='', host='', update=False, Return=[], return_dict=False):
    #---
    if query == '' : 
        pywikibot.output("query == ''")
        return Return
    #---
    pywikibot.output('<<lightyellow>> newsql::')
    return sql_connect_pymysql( query, db=db, host=host, update=update, Return=Return, return_dict=return_dict)
#---