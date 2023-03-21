#!/usr/bin/python
"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
from pywikibot import config
from warnings import warn
import pywikibot
import sys
import os
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
# py_tools.quoteurl(fao)
#---
'''
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
'''
#---
can_use_sql_db = { 1 : False }
#---
try:
    import MySQLdb
    can_use_sql_db[1] = True
except Exception as e:
    pywikibot.output('<<lightred>> mdwiki/sql_for_mdwiki.py errors when import MySQLdb')
    pywikibot.output('<<lightred>> %s' % e )
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
def Decode_bytes(x):
    if type(x) == bytes:    x = x.decode("utf-8")
    return x
#---
def make_sql_connect_new(query , update = False, Prints = True):
    #---
    if Prints: pywikibot.output('start mdwiki_sql:')
    #---
    if query == '' : 
        pywikibot.output("query == ''")
        return {}
    #---
    user    = config.db_username
    passwd  = config.db_password
    #---
    args = {}
    args['host'] = 'tools.db.svc.wikimedia.cloud'
    args['db']   = config.db_username + '__mdwiki'
    args['charset'] = "utf8"
    #---
    if 'localhost' in sys.argv or project.find('/mnt/') == -1:
        #---
        args['host'] = '127.0.0.1'
        args['db']   = 'mdwiki'
        #---
        user = 'root'
        passwd  = 'root11'
    #---
    credentials = {'user': user, 'password': passwd}
    #---
    params = None
    #---
    # connect to the database server without error
    try:
        connection = pymysql.connect(**args, **credentials)
    except MySQLdb.Error as e:
        pywikibot.output( 'Traceback (most recent call last):' )
        warn('Exception:' + str(e), UserWarning)
        pywikibot.output( 'CRITICAL:' )
        return Return
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
        except MySQLdb.Error as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception: MySQLdb.Error', UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return Return
        except MemoryError :
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception: MemoryError', UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return Return
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return Return
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
            return Return
        #---
        # yield from cursor
        return results
#---
def mdwiki_sql(query , update = False, Prints = True):
    #---
    if 'newsql' in sys.argv:
        pywikibot.output('<<lightyellow>> newsql::')
        return make_sql_connect_new( query, update=update, Prints=Prints)
    #---
    if Prints: pywikibot.output('start mdwiki_sql:')
    #---
    if not can_use_sql_db[1] : 
        pywikibot.output('no mysql')
        return {}
    #---
    if query == '' : 
        pywikibot.output("query == ''")
        return {}
    #---
    # MySQLdb.connect with arrgs
    arrgs = {
        'host': 'tools.db.svc.wikimedia.cloud',
        'user': config.db_username,
        'passwd': config.db_password,
        'db': config.db_username + '__mdwiki',
        'charset': 'utf8',
        'use_unicode': True,
    }
    #---
    if 'localhost' in sys.argv or project.find('/mnt/') == -1:
        arrgs['host'] = '127.0.0.1'
        arrgs['user'] = 'root'
        arrgs['passwd']  = 'root11'
        arrgs['db']   = 'mdwiki'
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
    if 'te220' in sys.argv:
        if update:
           results = cn.commit()
        else:
           results = cur.fetchall()
    else:
        #---
        try:
            if update:
               results = cn.commit()
            else:
               results = cur.fetchall()
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            return {}
    #---
    if Prints and update:
        res = str(results)
        ux = query.lower().split('values')[0].split('select')[0].strip()
        pywikibot.output(f"<<lightyellow>>sql_for_mdwiki.py mdwiki_sql result:{ux}:\n{res}" )
    #---
    cn.close()
    #---
    return results
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
        if qqid != '':
            mdtitle_to_qid[title] = qqid
    #---
    return mdtitle_to_qid
#---
def add_qid(title, qid):
    qua = """INSERT INTO qids (title, qid) SELECT {title}, '{qid}';""".format(qid=qid, title = py_tools.make_cod(title))
    #---
    print(f'add_qid()  title:{title}, qid:{qid}')
    #---
    mdwiki_sql(qua, update=True)
#---
def update_qid(title, qid):
    qua = """UPDATE qids set qid = '{qid}' where title = {title};""".format(qid=qid, title = py_tools.make_cod(title))
    #---
    print(f'update_qid()  title:{title}, qid:{qid}')
    #---
    mdwiki_sql(qua, update=True)
#---
def add_titles_to_qids(tab):
    #---
    new = {}
    #---
    for title, qid in tab.items():
        #---
        if qid == '' or title == '': 
            print("qid == '' or title == ''")
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
        if title != all_in[title]:
            update_qid(title, qid)
            continue
        #---
    #---
#---