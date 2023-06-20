#!/usr/bin/python
"""
python3 pwb.py mdpy/sql_for_mdwiki
"""
#
# (C) Ibrahem Qasim, 2023
#
#
from pywikibot import config
from warnings import warn
import pywikibot
import sys
import os
#--- 
'''
#---
from mdpy.bots import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query, update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# pages = sql_for_mdwiki.get_all_pages()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
#---
'''
#---
can_use_sql_db = { 1 : True }
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
project = '/data/project/mdwiki/'
#---
if not os.path.isdir(project):  project = '/mdwiki'
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
main_args = {
    'host':     'tools.db.svc.wikimedia.cloud',
    'db':       's54732__mdwiki',
    'charset':  'utf8mb4',
    'use_unicode': True,
    'autocommit': True
    }
#---
if 'localhost' in sys.argv or project == '/mdwiki':
    main_args['host'] = '127.0.0.1'
    main_args['db']   = 'mdwiki'
    credentials = {'user': 'root','password': 'root11'}
#---
def sql_connect_pymysql(query, return_dict=False):
    #---
    print('start sql_connect_pymysql:')
    #---
    args = { x: v for x,v in main_args.items()}
    #---
    params = None
    #---
    # connect to the database server without error
    #---
    Typee = pymysql.cursors.Cursor
    if return_dict:
        Typee = pymysql.cursors.DictCursor
    #---
    args['cursorclass'] = Typee
    #---
    try:
        connection = pymysql.connect(**args, **credentials)

    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return []
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
            return []
        #---
        results = []
        #---
        try:
            results = cursor.fetchall()

        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return []
        #---
        # yield from cursor
        return results
#---
def make_cod(string):
    lie = "'%s'" % string
    #---
    if string.find("'") != -1 : lie = '"%s"' % string
    #---
    return lie
#---
def Decode_bytes(x):
    if type(x) == bytes:    x = x.decode("utf-8")
    return x
#---
def mdwiki_sql(query, return_dict=False, **kwargs):
    #---
    if not can_use_sql_db[1] :
        print('no mysql')
        return {}
    #---
    if query == '' :
        print("query == ''")
        return {}
    #---
    print('<<lightyellow>> newsql::')
    return sql_connect_pymysql( query, return_dict=return_dict)
    #---
#---
def get_all_qids():
    #---
    mdtitle_to_qid = {}
    #---
    sq = mdwiki_sql(' select DISTINCT title, qid from qids;', return_dict=True)
    #---
    for ta in sq: 
        mdtitle_to_qid[ta['title']] = ta['qid']
    #---
    return mdtitle_to_qid
#---
def get_all_pages():
    #---
    pages = []
    #---
    for ta in mdwiki_sql(' select DISTINCT title from pages;', return_dict=True): 
        pages.append(ta['title'])
    #---
    return pages
#---
def add_qid(title, qid):
    qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}';""".format(qid=qid, title = make_cod(title))
    #---
    print(f'add_qid()  title:{title}, qid:{qid}')
    #---
    return mdwiki_sql(qua, return_dict=True)
#---
def update_qid(title, qid):
    qua = """UPDATE qids set qid = '{qid}' where title = {title};""".format(qid=qid, title = make_cod(title))
    #---
    print(f'update_qid()  title:{title}, qid:{qid}')
    #---
    return mdwiki_sql(qua, return_dict=True)
#---
def add_titles_to_qids(tab, add_empty_qid=False):
    #---
    new = {}
    #---
    for title, qid in tab.items():
        #---
        if title == '': 
            print("title == ''")
            continue
        #---
        if qid == '' and not add_empty_qid: 
            print("qid == ''")
            continue
        #---
        new[title] = qid
    #---
    all_in = get_all_qids()
    #---
    for title, qid in new.items():
        if not title in all_in:
            add_qid(title, qid)
            continue
        #---
        q_in = all_in[title]
        #---
        if qid != '':
            if q_in == '':
                update_qid(title, qid)
            else:
                # update_qid(title, qid)
                print(f'update_qid()  qid_in:{q_in}, new_qid:{qid}')
        #---
    #---
#---
def tests():
    #---
    # test_get_all_qids
    qua = ' select DISTINCT * from pages where lang ="zh" limit 100;'
    #---
    qids = sql_connect_pymysql(qua)
    print('sql_connect_pymysql:')
    print(len(qids))
    #---
    # test_add_qid
    a = add_qid('test', 'test')
    print(f'add: {a}')
    aa = add_qid('test11', '11')
    print(f'add: {aa}')
    #---
    # test_update_qid
    zz = update_qid('test11', 'xxx')
    print(f'update: {zz}')
    #---
    # return
    # test_get_all_pages
    # pages = mdwiki_sql(' select DISTINCT * from pages limit 10;', return_dict=True)
    pages = get_all_pages()
    print(f'len of pages:{len(pages)}')
    print(pages)
    #---
#---
if __name__ == '__main__':
    tests()