#!/usr/bin/python3
"""
page views bot

python3 core8/pwb.py mdpy/sqlviews testtest -lang:ar

python3 core8/pwb.py /data/project/mdwiki/mdpy/sqlviews -lang:or

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re
import sys

# ---
from mdpy.bots import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ===
# ---
from mdpy.bots import wiki_api
from pymysql.converters import escape_string

from mdpy import printe

already_in_sql = {}
# ---
Lang_to_targets = {}


def print_test(strr):
    if 'print' in sys.argv or 'nosql' in sys.argv:
        printe.output(strr)


def update_2023(lang, table):
    # ---
    sql_values = already_in_sql.get(lang, {})
    # ---
    for target, tab in table.items():
        # ---
        sq = sql_values.get(target, {})
        # ---
        n_2021 = sq.get('2021', 0)
        n_2022 = sq.get('2022', 0)
        n_2023 = tab.get('2023', {}).get('all', 0)
        # ---
        if sq.get('2023', 0) > n_2023:
            n_2023 = sq.get('2023', 0)
        # ---
        all = n_2021 + n_2022 + n_2023
        # ---
        if sq.get('all', 0) == all and sq.get('2023', 0) == n_2023:
            print_test(f'page:{target} has same views.. skip')
            continue
        # ---
        tar2 = escape_string(target)
        # ---
        qua = f"UPDATE views SET countall = '{all}', count2023 = '{n_2023}' WHERE target = '{tar2}' AND lang = '{lang}'; "
        # ---
        print(qua)
        # ---
        if 'nosql' not in sys.argv:
            qu = sql_for_mdwiki.mdwiki_sql(qua, update=True)
            # ---
            printe.output("<<lightyellow>>sqlviewsm.py mdwiki_sql result:" + str(qu))


def update_in_sql(lang, table):
    # ---
    sql_values = already_in_sql.get(lang, {})
    # ---
    for target, tab in table.items():
        # ---
        sq = sql_values.get(target, {})
        # ---
        all = tab.get('all', 0)
        n_2021 = tab.get('2021', {}).get('all', 0)
        n_2022 = tab.get('2022', {}).get('all', 0)
        n_2023 = tab.get('2023', {}).get('all', 0)
        # ---
        if sq.get('2021', 0) > n_2021:
            n_2021 = sq.get('2021', 0)
        if sq.get('2022', 0) > n_2022:
            n_2022 = sq.get('2022', 0)
        if sq.get('2023', 0) > n_2023:
            n_2023 = sq.get('2023', 0)
        all = n_2021 + n_2022 + n_2023
        # ---
        if sq.get('all', 0) == all and sq.get('2021', 0) == n_2021 and sq.get('2022', 0) == n_2022 and sq.get('2023', 0) == n_2023:
            print_test(f'page:{target} has same views.. skip')
            continue
        # ---
        tar2 = escape_string(target)
        # ---
        qua = f""" UPDATE views SET countall = '{all}', count2021 = '{n_2021}', count2022 = '{n_2022}', count2023 = '{n_2023}'
        WHERE target = '{tar2}' AND lang = '{lang}';
        """
        # ---
        print(qua)
        # ---
        if 'nosql' not in sys.argv:
            qu = sql_for_mdwiki.mdwiki_sql(qua, update=True)
            # ---
            printe.output("<<lightyellow>>sqlviewsm.py mdwiki_sql result:" + str(qu))


def insert_to_sql(lang, table):
    # ---
    to_insert = []
    # ---
    for target, tab in table.items():
        # ---
        all = tab.get('all', 0)
        n_2021 = tab.get('2021', {}).get('all', 0)
        n_2022 = tab.get('2022', {}).get('all', 0)
        n_2023 = tab.get('2023', {}).get('all', 0)
        # ---
        tar2 = escape_string(target)
        # ---
        # qu = f''' ('{tar2}', '{all}', '{n_2021}', '{n_2022}', '{n_2023}', '{lang}') '''
        qu = f'''INSERT INTO views (target, countall, count2021, count2022, count2023, lang)
        select '{tar2}', '{all}', '{n_2021}', '{n_2022}', '{n_2023}', '{lang}'
        WHERE NOT EXISTS (SELECT 1 FROM views WHERE target = '{tar2}' AND lang = '{lang}');
        '''
        # ---
        print('INSERT:')
        # ---
        qu = sql_for_mdwiki.mdwiki_sql(qu, update=True, Prints=True)
        # ---
        # to_insert.append(qu)
    # ---
    if len(to_insert) > 0:
        ins = ",\n".join(to_insert)
        qua = f""" INSERT INTO views (target, countall, count2021, count2022, count2023, lang) VALUES
            {ins}; """
        # ---
        print(qua)
        # ---
        if 'nosql' not in sys.argv:
            qu = sql_for_mdwiki.mdwiki_sql(qua, update=True)
            # ---
            printe.output("<<lightyellow>>sqlviewsm.py mdwiki_sql result:" + str(qu))


def get_targets(lang_o):
    # ---
    uu = ''
    # ---
    if lang_o != '':
        uu = f'and lang = "{lang_o}"'
    # ---
    que = f'''select DISTINCT lang, target, pupdate from pages
    where target != ""
    {uu}
    ;'''
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    for tab in sq:
        lang = tab['lang'].lower()
        target = tab['target']
        pupdate = tab['pupdate']
        # ---
        if '2023' in sys.argv and not pupdate.startswith('2023'):
            pupdate = '2023-01-01'
        # ---
        if target != "":
            if lang not in Lang_to_targets:
                Lang_to_targets[lang] = {}
            Lang_to_targets[lang][target] = pupdate
    # ---
    print(f'<<lightyellow>> find {len(sq)} to work. ')


def get_views_sql(lang_o):
    # ---
    uu = ''
    if lang_o != '':
        uu = f'where lang = "{lang_o}"'
    # ---
    que11 = f'''select DISTINCT target, lang, countall, count2021, count2022, count2023
    from views
    {uu}
    ;
    '''
    # ---
    dad = sql_for_mdwiki.mdwiki_sql(que11, return_dict=True)
    # ---
    for tab in dad:
        target = tab['target']
        lang = tab['lang'].lower()
        countall = tab['countall']
        count2021 = tab['count2021']
        count2022 = tab['count2022']
        count2023 = tab['count2023']
        # ---
        if lang not in already_in_sql:
            already_in_sql[lang] = {}
        # ---
        already_in_sql[lang][target] = {'all': countall, '2021': count2021, '2022': count2022, '2023': count2023}


def main():
    # ---
    print(' _finder: ')
    # ---
    lang_o = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        if arg == 'lang' or arg == '-lang':
            lang_o = value
    # ---
    get_targets(lang_o)
    # ---
    get_views_sql(lang_o)
    # ---
    lang_pupdate_titles = {}
    # ---
    for lang, tit_list in Lang_to_targets.items():
        # ---
        if lang not in lang_pupdate_titles:
            lang_pupdate_titles[lang] = {}
        # ---
        # قوائم حسب تاريخ النشر
        for tit, pupdate in tit_list.items():
            # ---
            if pupdate not in lang_pupdate_titles[lang]:
                lang_pupdate_titles[lang][pupdate] = []
            # ---
            lang_pupdate_titles[lang][pupdate].append(tit)
    # ---
    for lange, tab in lang_pupdate_titles.items():
        # ---
        numbs = {}
        # ---
        for pupdate, title_list in tab.items():
            start = '20210401'
            # ---
            rem = re.match(r'^(?P<y>\d\d\d\d)-(?P<m>\d\d)-(?P<d>\d\d)$', pupdate)
            # ---
            if rem:
                start = rem.group('y') + rem.group('m') + rem.group('d')
            # ---
            lenlist = len(title_list)
            # ---
            printe.output('---')
            printe.output(f'<<lightyellow>> get pageviews for {lenlist} pages, date_start:{start}')
            # ---
            if lenlist < 5:
                printe.output(", ".join(title_list))
            # ---
            numbers = wiki_api.get_views_with_rest_v1(lange, title_list, date_start=start, date_end='20300101', printurl=False, printstr=False, Type='daily')
            # ---
            if 'numbers' in sys.argv and title_list[0] == 'Tacalcitol':
                printe.output(numbers)
            # ---
            numbs = {**numbs, **numbers}
        # ---
        if 'testtest' in sys.argv:
            continue
        # ---
        insert = {}
        update = {}
        # ---
        sql_values = already_in_sql.get(lange, {})
        # ---
        for target, tab in numbs.items():
            # ---
            if sql_values.get(target, {}) != {}:
                update[target] = tab
            else:
                insert[target] = tab
        # ---
        if '2023' in sys.argv:
            update_2023(lange, update)
        else:
            update_in_sql(lange, update)
        # ---
        insert_to_sql(lange, insert)


# ---
if __name__ == '__main__':
    main()
# ---
