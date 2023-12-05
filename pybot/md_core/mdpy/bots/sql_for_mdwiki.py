#!/usr/bin/python3
"""
python3 core8/pwb.py mdpy/sql_for_mdwiki

# ---
from mdpy.bots import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query, update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# pages = sql_for_mdwiki.get_all_pages()
# cats = sql_for_mdwiki.get_db_categories() # title:depth
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
# sql_for_mdwiki.set_title_where_qid(new_title, qid)
# ---

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import sys
import os
from pymysql.converters import escape_string
import pkg_resources
import pymysql.cursors
import pymysql
import traceback
import pywikibot

# ---
from mdpy import printe
from pywikibot import config

# ---
can_use_sql_db = {1: True}
# ---
py_v = pymysql.__version__
if py_v.endswith('.None'):
    py_v = py_v[: -len('.None')]
# ---
pymysql_version = pkg_resources.parse_version(py_v)
print(f'<<lightyellow>> pymysql_version: {pymysql_version}')
# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
db_username = config.db_username
db_password = config.db_password
# ---
if config.db_connect_file is None:
    credentials = {'user': db_username, 'password': db_password}
else:
    credentials = {'read_default_file': config.db_connect_file}
# ---
main_args = {
    'host': 'tools.db.svc.wikimedia.cloud',
    'db': 's54732__mdwiki',
    'charset': 'utf8mb4',
    # 'collation':  'utf8_general_ci',
    'use_unicode': True,
    'autocommit': True,
}
# ---
if 'localhost' in sys.argv or project == '/mdwiki':
    main_args['host'] = '127.0.0.1'
    main_args['db'] = 'mdwiki'
    credentials = {'user': 'root', 'password': 'root11'}


def sql_connect_pymysql(query, return_dict=False):
    # ---
    # print('start sql_connect_pymysql:')
    # ---
    args = {x: v for x, v in main_args.items()}
    # ---
    params = None
    # ---
    # connect to the database server without error
    # ---
    Typee = pymysql.cursors.Cursor
    if return_dict:
        Typee = pymysql.cursors.DictCursor
    # ---
    args['cursorclass'] = Typee
    # ---
    connection = pymysql.connect(**args, **credentials)
    try:
        connection = pymysql.connect(**args, **credentials)

    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        return []
    # ---
    if pymysql_version < pkg_resources.parse_version('1.0.0'):
        from contextlib import closing

        connection = closing(connection)
    # ---
    with connection as conn, conn.cursor() as cursor:
        # ---
        # skip sql errors
        try:
            cursor.execute(query, params)

        except Exception:
            pywikibot.output('Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
            return []
        # ---
        results = []
        # ---
        try:
            results = cursor.fetchall()

        except Exception:
            pywikibot.output('Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
            return []
        # ---
        # yield from cursor
        return results


def mdwiki_sql(query, return_dict=False, **kwargs):
    # ---
    if not can_use_sql_db[1]:
        print('no mysql')
        return {}
    # ---
    if query == '':
        print("query == ''")
        return {}
    # ---
    # print('<<lightyellow>> newsql::')
    return sql_connect_pymysql(query, return_dict=return_dict)


def get_all_qids():
    # ---
    mdtitle_to_qid = {}
    # ---
    sq = mdwiki_sql('select DISTINCT title, qid from qids;', return_dict=True)
    # ---
    for ta in sq:
        mdtitle_to_qid[ta['title']] = ta['qid']
    # ---
    return mdtitle_to_qid


def get_all_pages():
    # ---
    pages = []
    # ---
    for ta in mdwiki_sql('select DISTINCT title from pages;', return_dict=True):
        pages.append(ta['title'])
    # ---
    return pages


def get_db_categories():
    # ---
    cats = {}
    # ---
    for c in mdwiki_sql('select category, depth from categories;', return_dict=True):
        cat = c['category']
        dep = c['depth']
        # ---
        cats[cat] = dep
    # ---
    return cats


def add_qid(title, qid):
    title2 = escape_string(title)
    qua = f"""INSERT INTO qids (title, qid) SELECT '{title2}', '{qid}';"""
    # ---
    printe.output(f'<<yellow>> add_qid()  title:{title}, qid:{qid}')
    # ---
    return mdwiki_sql(qua, return_dict=True)


def set_qid_where_title(title, qid):
    title2 = escape_string(title)
    qua = f"""UPDATE qids set qid = '{qid}' where title = '{title2}';"""
    # ---
    printe.output(f'<<yellow>> set_qid_where_title()  title:{title}, qid:{qid}')
    # ---
    return mdwiki_sql(qua, return_dict=True)


def set_title_where_qid(new_title, qid):
    title2 = escape_string(new_title)
    qua = f"""UPDATE qids set title = '{title2}' where qid = '{qid}';"""
    # ---
    printe.output(f'<<yellow>> set_title_where_qid()  new_title:{new_title}, qid:{qid}')
    # ---
    return mdwiki_sql(qua, return_dict=True)


def add_titles_to_qids(tab, add_empty_qid=False):
    # ---
    new = {}
    # ---
    for title, qid in tab.items():
        # ---
        if title == '':
            print("title == ''")
            continue
        # ---
        if qid == '' and not add_empty_qid:
            print("qid == ''")
            continue
        # ---
        new[title] = qid
    # ---
    all_in = get_all_qids()
    # ---
    for title, qid in new.items():
        if title not in all_in:
            add_qid(title, qid)
            continue
        # ---
        q_in = all_in[title]
        # ---
        if qid != '':
            if q_in == '':
                set_qid_where_title(title, qid)
            else:
                # set_qid_where_title(title, qid)
                printe.output(f'<<yellow>> set_qid_where_title() qid_in:{q_in}, new_qid:{qid}')


def tests():
    # ---
    # test_get_all_qids
    '''
    qua = ' select DISTINCT * from pages where lang ="zh" limit 100;'
    # ---
    qids = sql_connect_pymysql(qua)
    print('sql_connect_pymysql:')
    print(len(qids))
    # ---
    # test_add_qid
    a = add_qid('test', 'test')
    printe.output(f'<<yellow>> add: {a}')
    aa = add_qid('test11', '11')
    printe.output(f'<<yellow>> add: {aa}')
    # ---
    # test_update_qid
    zz = set_qid_where_title('test11', 'xxx')
    printe.output(f'<<yellow>> update: {zz}')
    # ---
    '''
    # return
    # test_get_all_pages
    # pages = mdwiki_sql(' select DISTINCT * from pages limit 10;', return_dict=True)
    pages = get_all_pages()
    printe.output(f'<<yellow>> len of pages:{len(pages)}')
    printe.output(pages)

    # ---


if __name__ == '__main__':
    tests()
