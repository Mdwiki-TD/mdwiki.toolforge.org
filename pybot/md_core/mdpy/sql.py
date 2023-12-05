#!/usr/bin/python3
"""
بوت قواعد البيانات

python3 core8/pwb.py mdpy/sql justsql break
python3 core8/pwb.py mdpy/sql justsql
python3 core8/pwb.py mdpy/sql

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re
import os

import sys
import time as tttime
from pymysql.converters import escape_string

from mdpy.bots import add_to_wd

# add_to_wd.add_tab_to_wd(New_Table_by_lang)
# ---
from mdpy.bots import py_tools
from mdpy import printe

# escape_string(string)

# ---
from mdpy.bots import wiki_sql

# wiki_sql.GET_SQL()
# wiki_sql.Make_sql_many_rows( queries , wiki="", printqua = False)
# ---
from mdpy.bots import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
cat_for_pages = {}
from mdpy.others.fixcat import cat_for_pages

# ---
Lang_usr_mdtitle = {}
targets_done = {}
Langs_to_title_and_user = {}
to_update_lang_user_mdtitle = {}
# ---
printsql = {1: False}


def add_to_mdwiki_sql(table):
    # Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    # ---
    for lane, tab in table.items():
        for tt in tab:
            tabe = tab[tt]
            mdtitle = tabe['mdtitle']
            lang = tabe['lang']
            target = tabe['target']
            user = tabe['user']
            pupdate = tabe['pupdate']
            namespace = tabe['namespace']
            # ---
            cat = cat_for_pages.get(mdtitle, '')
            # ---
            mdtit = escape_string(mdtitle)
            user2 = escape_string(user)
            tar = escape_string(target)
            word = 0
            # ---
            if str(namespace) != '0':
                continue
            # ---
            tata = to_update_lang_user_mdtitle.get(lang, {}).get(user, [])
            # ---
            uuu = ''
            # ---
            # date now format like 2023-01-01
            add_date = tttime.strftime("%Y-%m-%d")
            # ---
            update_qua = f'''UPDATE pages SET target='{tar}', pupdate="{pupdate}", add_date="{add_date}" WHERE user='{user2}' AND title='{mdtit}' AND lang="{lang}";'''
            # ---
            insert_qua = f'''
                INSERT INTO pages (title, word, translate_type, cat, lang, date, user, pupdate, target, add_date)
                SELECT '{mdtit}', '{word}', 'lead', '{cat}', '{lang}', '{add_date}', '{user2}', '{pupdate}', '{tar}', '{add_date}'
                WHERE NOT EXISTS (SELECT 1 FROM pages WHERE title='{mdtit}' AND lang='{lang}' AND user='{user2}' );'''
            # ---
            printe.output('______ \\/\\/\\/ _______')
            # find if to update or to insert
            if mdtitle in tata:
                printe.output(f'to update: title:{mdtitle}, user:{user} ')
                uuu = update_qua
            else:
                printe.output(f'to insert: title:{mdtitle}, user:{user} ')
                uuu = insert_qua
            # ---
            printe.output(uuu)
            # ---
            qu = sql_for_mdwiki.mdwiki_sql(uuu, update=True, Prints=False)
            # ---
            printe.output(qu)


# ---
tit_user_lang = {}


def dodo_sql():
    # ---
    lang_o = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        if arg == 'lang' or arg == '-lang':
            lang_o = value
            Langs_to_title_and_user[value] = {}
        # ---
        if arg == 'printsql':
            printsql[1] = True
    # ---
    que = 'select title, user, lang, target from pages '
    # ---
    if lang_o != '':
        que += f' where lang = "{lang_o}"'
    # ---
    que += ' ;'
    # ---
    printe.output(que)
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    len_no_target = 0
    len_done_target = 0
    # ---
    for tab in sq:
        mdtitle = tab['title']
        user = tab['user']
        target = tab['target']
        lang = tab['lang'].lower()
        # ---
        if lang_o != '' and lang != lang_o.strip():
            continue
        # ---
        tul = mdtitle + user + lang
        tit_user_lang[tul] = target
        # ---
        if lang not in Lang_usr_mdtitle:
            Lang_usr_mdtitle[lang] = {}
        if user not in Lang_usr_mdtitle[lang]:
            Lang_usr_mdtitle[lang][user] = []
        # ---
        Lang_usr_mdtitle[lang][user].append(mdtitle)
        # ---
        if lang not in Langs_to_title_and_user:
            Langs_to_title_and_user[lang] = {}
        if lang not in to_update_lang_user_mdtitle:
            to_update_lang_user_mdtitle[lang] = {}
        # ---
        if user not in to_update_lang_user_mdtitle[lang]:
            to_update_lang_user_mdtitle[lang][user] = []
        # ---
        if target == "":
            len_no_target += 1
            # ---
            Langs_to_title_and_user[lang][mdtitle] = user
            # ---
            to_update_lang_user_mdtitle[lang][user].append(mdtitle)
            # ---
        else:
            # ---
            if lang not in targets_done:
                targets_done[lang] = {}
            # ---
            target = target.replace("_", " ")
            target2 = py_tools.ec_de_code(target, 'encode')
            # ---
            lineout = 'done. <<lightgreen>> target:%s for mdtit:%s, user:%s'
            laloly = lineout % (target.ljust(40), mdtitle.ljust(30), user)
            # ---
            # printe.output(laloly)
            # ---
            len_done_target += 1
            # ---
            # targets_done[lang][mdtitle] = { "user" : user , "target" : target }
            # targets_done[lang][mdtitle] = { "user" : user , "target" : target }
            # targets_done[lang][py_tools.ec_de_code(target , 'encode')] = { "user" : user , "target" : target }
            # ---
            targets_done[lang][target] = {"user": user, "target": target}
            targets_done[lang][target2] = {"user": user, "target": target}
    # ---
    printe.output('<<lightyellow>> find %d with target, and %s without in mdwiki database. ' % (len_done_target, len_no_target))
    # ---
    if 'print' in sys.argv:
        printe.output(Langs_to_title_and_user)
    # ---
    tttime.sleep(3)


# ---
query_main_old = '''
    select DISTINCT p.page_title, c.comment_text , a.actor_name , r.rev_timestamp
    from change_tag t
    INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
    INNER JOIN revision r on r.rev_id = t.ct_rev_id
    INNER JOIN actor a ON r.rev_actor = a.actor_id
    inner join comment c on c.comment_id = r.rev_comment_id
    INNER JOIN page p on r.rev_page=p.page_id
    where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
    and r.rev_parent_id = 0
    #AND a.actor_name in ('Mr. Ibrahem')
    AND r.rev_timestamp > 20210101000000
    #and comment_text like "%[[:en:Special:Redirect/revision/%|User:Mr. Ibrahem/%]]%"
    and comment_text like "%User:Mr. Ibrahem/%"
    and p.page_namespace = 0
    #limit 10
'''
# ---
query_main = '''
    select DISTINCT p.page_title,
    SUBSTRING_INDEX(SUBSTRING_INDEX(c.comment_text, 'Ibrahem/', -1), ']]', 1),
    a.actor_name, r.rev_timestamp, p.page_namespace, r.rev_parent_id
    from change_tag t
    INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
    INNER JOIN revision r on r.rev_id = t.ct_rev_id
    INNER JOIN actor a ON r.rev_actor = a.actor_id
    inner join comment c on c.comment_id = r.rev_comment_id
    INNER JOIN page p on r.rev_page=p.page_id
    where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
    #and r.rev_parent_id = 0
    AND r.rev_timestamp > 20210101000000
    and comment_text like "%User:Mr. Ibrahem/%"
    #and p.page_namespace = 0
    group by p.page_title, a.actor_name, c.comment_text
'''


def main():
    # ---
    # ---
    dodo_sql()
    # ---
    New_Table_by_lang = {}
    # ---
    Skip_titles_global = ['جامعة نورث كارولاينا', 'جامعة ولاية كارولينا الشمالية إيه آند تي', 'نيشان راجاميترابورن', 'موميتازون']
    # ---
    Skip_titles = {}
    Skip_titles['Mr. Ibrahem'] = {'targets': ['جامعة نورث كارولاينا', 'جامعة ولاية كارولينا الشمالية إيه آند تي', 'نيشان راجاميترابورن'], 'mdtitles': []}
    Skip_titles['Avicenno'] = {'targets': ['ألم فرجي', 'لقاح المكورة السحائية', 'استئصال اللوزتين'], 'mdtitles': []}
    # ---
    Skip_titles['Subas Chandra Rout'] = {'targets': [], 'mdtitles': ["Wilms' tumor", "Sheehan's syndrome", "Membranous nephropathy"]}
    # ---
    n = 0
    # ---
    sskip = ['zh-yue', 'ceb']
    # ---
    numb_lang = 0
    lnn = len(Langs_to_title_and_user.keys())
    # ---
    # for lange,lal in Langs_to_title_and_user.items():
    for lange in Langs_to_title_and_user:
        # ---
        New_Table_by_lang[lange] = {}
        # ---
        numb_lang += 1
        # ---
        printe.output(' \\/\\/\\/\\/\\/ ')
        printe.output('mdwiki/mdpy/sql.py: %d Lang from %s : "%s"' % (numb_lang, lnn, lange))
        # ---
        result = {}
        # ---
        qua = query_main
        # ---
        if lange == 'ar':
            qua += "\n and p.page_title not in ('جامعة_نورث_كارولاينا','جامعة_ولاية_كارولينا_الشمالية_إيه_آند_تي','نيشان_راجاميترابورن')"
        # ---
        qua += '\n;'
        # ---
        if lange in sskip:
            printe.output(f'skip lang:{lange}')
        else:
            if 'printquery' in sys.argv:
                print(qua)
            result = wiki_sql.Make_sql_many_rows(qua, wiki=str(lange))
        # ---
        if result != {}:
            printe.output(f'sql.py len(result) = "{len( result )}"')
            # ---
            texddt = '\n'
            # ---
            for list in result:
                # ---
                # printe.output( list )
                target = py_tools.Decode_bytes(list[0])
                co_text = py_tools.Decode_bytes(list[1])
                user = py_tools.Decode_bytes(list[2])
                pupdate = py_tools.Decode_bytes(list[3])
                namespace = py_tools.Decode_bytes(list[4])
                rev_parent_id = py_tools.Decode_bytes(list[5])
                # ---
                namespace = str(namespace)
                # ---
                pupdate = pupdate[:8]
                pupdate = re.sub(r'^(\d\d\d\d)(\d\d)(\d\d)$', r'\g<1>-\g<2>-\g<3>', pupdate)
                # ---
                md_title = co_text.replace("_", " ")
                # ---
                target = target.replace("_", " ")
                # ---
                user = user.replace("_", " ")
                # ---
                if target in Skip_titles_global:
                    continue
                if target in Skip_titles.get(user, {}).get('targets', []):
                    continue
                # ---
                if md_title in Skip_titles.get(user, {}).get('mdtitles', []):
                    continue
                # ---
                Taba2 = {"mdtitle": md_title, "target": target, "user": user, "lang": lange, "pupdate": pupdate, "namespace": namespace}
                # ---
                lineout = '<<lightyellow>> target:%s:%s, ns:%s for mdtit:<<lightyellow>>%s, user:<<lightyellow>>%s'
                laloly = lineout % (lange, target.ljust(40), namespace.ljust(3), md_title.ljust(30), user)
                # ---
                tgd = targets_done.get(lange, {})
                # ---
                target2 = py_tools.ec_de_code(target, 'encode')
                # ---
                tul = md_title + user + lange
                tul_target = tit_user_lang.get(tul, '')
                # ---
                cattest = cat_for_pages.get(md_title, '')
                # ---
                if namespace != '0':
                    if 'ns' in sys.argv and tul_target == '' and cattest:
                        printe.output(laloly)
                    continue
                # ---
                # للتأكد من الصفحات غير المنشورة
                if target2 not in tgd and target not in tgd:
                    # ---
                    if tul_target != '':
                        if tul_target == target:
                            printe.output(f'target already in, {target}')
                        else:
                            printe.output(f'puplished target: {tul_target} != target to add: {target}')
                    else:
                        New_Table_by_lang[lange][md_title] = Taba2
                        n += 1
                        printe.output(laloly)
                # ---
        # ---
        add_to_wd.add_tab_to_wd({lange: New_Table_by_lang[lange]})
        # ---
        add_to_mdwiki_sql({lange: New_Table_by_lang[lange]})

    # ---


if __name__ == '__main__':
    main()
# ---
