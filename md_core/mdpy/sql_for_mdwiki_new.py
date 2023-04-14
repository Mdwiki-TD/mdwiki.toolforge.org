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
from mdpy import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query, update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# pages = sql_for_mdwiki.get_all_pages()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
#---
'''
#---
can_use_sql_db = { 1 : True }
#---
#---
import MySQLdb
import pymysql
import pkg_resources
#---
py_v = pymysql.__version__
if py_v.endswith('.None'): py_v = py_v[:-len('.None')]
#---
pymysql_version = pkg_resources.parse_version(py_v)
pywikibot.output(f'<<lightyellow>> pymysql_version: {pymysql_version}')
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project):
    project = '/mdwiki'
    # can_use_sql_db[1] = False
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
main_args = {
    'host':     'tools.db.svc.wikimedia.cloud',
    'user':     config.db_username,
    'passwd':   config.db_password,
    'db':       config.db_username + '__mdwiki',
    'charset':  'utf8',
    'use_unicode': True,
}
#---
if 'localhost' in sys.argv or project.find('/mnt/') == -1:
    main_args['host'] = '127.0.0.1'
    main_args['user'] = 'root'
    main_args['passwd']  = 'root11'
    main_args['db']   = 'mdwiki'
#---
def sql_connect_pymysql(query, update=False, Prints=True):
    #---
    pywikibot.output('start sql_connect_pymysql:')
    #---
    args = { x: v for x,v in main_args.items()}
    #---
    user    = args['user']
    passwd  = args['passwd']
    #---
    del args['user']
    del args['passwd']
    del args['use_unicode']
    #---
    credentials = {'user': user, 'password': passwd}
    #---
    params = None
    #---
    # connect to the database server without error
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
        try:
            if update:
                results = cursor.commit()
            else:
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
def sql_connect_MySQLdb(query, update=False, Prints=True):
    #---
    pywikibot.output('start sql_connect_MySQLdb:')
    #---
    # MySQLdb.connect with arrgs
    #---
    arrgs = { x: v for x,v in main_args.items()}
    #---
    # connect to the database server without error
    try:
        cn = MySQLdb.connect(**arrgs)
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return {}
    #---
    cn.set_character_set('utf8')
    cur = cn.cursor()
    #---
    # cur.execute(query)
    # skip sql errors
    try:
        cur.execute(query)
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return {}
    #---
    try:
        if update:
            results = cn.commit()
        else:
            results = cur.fetchall()
        #---
    except Exception as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return {}
    #---
    if Prints and update:
        res = str(results)
        ux = [query.lower().split('values')[0].split('select')[0].strip()]
        pywikibot.output(f"<<lightyellow>>sql_for_mdwiki.py mdwiki_sql result:str({ux}):\n{res}" )
    #---
    cn.close()
    #---
    return results
#---
def mdwiki_sql(query, update=False, Prints=True):
    #---
    if not can_use_sql_db[1] :
        pywikibot.output('no mysql')
        return {}
    #---
    if query == '' :
        pywikibot.output("query == ''")
        return {}
    #---
    if 'newsql' in sys.argv:
        pywikibot.output('<<lightyellow>> newsql::')
        return sql_connect_pymysql( query, update=update, Prints=Prints)
    else:
        pywikibot.output('<<lightyellow>> oldsql::')
        return sql_connect_MySQLdb( query, update=update, Prints=Prints)
    #---
#---
def get_all_qids():
    #---
    mdtitle_to_qid = {}
    #---
    sq = mdwiki_sql(' select DISTINCT title, qid from qids;')
    #---
    for ta in sq: 
        title = Decode_bytes(ta[0])
        qqid = Decode_bytes(ta[1])
        mdtitle_to_qid[title] = qqid
    #---
    return mdtitle_to_qid
#---
def get_all_pages():
    #---
    pages = []
    #---
    for ta in mdwiki_sql(' select DISTINCT title from pages;'): 
        title = Decode_bytes(ta[0])
        pages.append(title)
    #---
    return pages
#---
def add_qid(title, qid):
    qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}';""".format(qid=qid, title = make_cod(title))
    #---
    print(f'add_qid()  title:{title}, qid:{qid}')
    #---
    mdwiki_sql(qua, update=True)
#---
def update_qid(title, qid):
    qua = """UPDATE qids set qid = '{qid}' where title = {title};""".format(qid=qid, title = make_cod(title))
    #---
    print(f'update_qid()  title:{title}, qid:{qid}')
    #---
    mdwiki_sql(qua, update=True)
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
    qids = get_all_qids()
    print(f'len of qids:{len(qids)}')
    #---
    # test_get_all_pages
    pages = get_all_pages()
    print(f'len of pages:{len(pages)}')
    #---
    # test_add_qid
    t = add_qid('test', 'test')
    t = add_qid('test11', '11')
    #---
    # test_update_qid
    t = update_qid('test11', 'xxx')
    #---
#---
if __name__ == '__main__':
    tests()