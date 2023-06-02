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
print(f'<<lightyellow>> pymysql_version: {pymysql_version}')
#---
db_username = config.db_username
db_password = config.db_password
#---
if config.db_connect_file is None:
    credentials = {
        'user': db_username,
        'password': db_password
    }
else:
    credentials = {'read_default_file': config.db_connect_file}
#---
can_use_sql_db  = { 1 : True }
#---
dir1 = '/mnt/nfs/labstore-secondary-tools-project/mdwiki/'
dir2 = '/data/project/mdwiki/'
#---
if not os.path.isdir(dir1) and not os.path.isdir(dir2) : 
    can_use_sql_db[1] = False
#---
def sql_connect_pymysql( query, db='', host='', update=False, Return=[], return_dict=False):
    #---
    print('start sql_connect_pymysql:')
    #---
    Typee = pymysql.cursors.Cursor
    if return_dict:
        Typee = pymysql.cursors.DictCursor
    #---
    args2 = {
        'host':     host,
        'db':       db,
        'charset':  'utf8mb4',
        'cursorclass': Typee,
        'use_unicode': True,
        'autocommit': True,
    }
    #---
    params = None
    #---
    # connect to the database server without error
    #---
    try:
        #connection = pymysql.connect( host=args['host'], user=args['user'], password=args['passwd'], db=args['db'], charset=args['charset'], cursorclass=Typee, autocommit=True )
        
        connection = pymysql.connect(**args2, **credentials)

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
        print("query == ''")
        return Return
    #---
    print('<<lightyellow>> newsql::')
    return sql_connect_pymysql( query, db=db, host=host, update=update, Return=Return, return_dict=return_dict)
#---