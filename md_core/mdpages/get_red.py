#!/usr/bin/env python
#   himo
"""
اصلاح التحويلات في قواعد البيانات

python3 core8/pwb.py mdpy/get_red

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import os
from datetime import datetime

# ---
from mdpy import printe
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import mdwiki_api

# ---
mdwiki_to_qid = sql_for_mdwiki.get_all_qids()
# ---
Day_History = datetime.now().strftime("%Y-%m-%d")
# ---
# sql_for_mdwiki.mdwiki_sql(query, update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# pages = sql_for_mdwiki.get_all_pages()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'


def get_pages():
    # ---
    table = {}
    # ---
    titles = list(mdwiki_to_qid.keys())
    # ---
    done = 0
    # ---
    len_grup = 100
    # ---
    for i in range(0, len(titles), len_grup):
        group = titles[i : i + len_grup]
        # ---
        done += len(group)
        # ---
        asa = mdwiki_api.get_redirect(group)
        # ---
        print(f'work on {len_grup} pagees, done: {done}/{len(titles)}.')
        # ---
        table = {**table, **asa}
        # ---
    # ---
    print(f'len of table {len(table)} ')
    # ---
    tat = ''
    # ---
    rep = 0
    remo = 0
    # ---
    to_add = {}
    to_del = []
    # ---
    for old_title, new_title in table.items():
        ll = f'"old_title: {old_title}" to: "{new_title}",\n'
        # ---
        # replace_titles(old_title, new_title)
        # ---
        new_title_qid = mdwiki_to_qid.get(new_title, False)
        old_title_qid = mdwiki_to_qid.get(old_title, False)
        # ---
        if old_title_qid:
            if not new_title_qid:
                # استبدال
                rep += 1
                # ---
                printe.output('<<lightyellow>>' + ll.strip())
                # ---
                sql_for_mdwiki.set_title_where_qid(new_title, old_title_qid)
                # ---
                to_del.append(old_title)
                to_add[new_title] = old_title_qid
                # ---
                tat += ll
                # ---
            elif new_title_qid == old_title_qid:
                remo += 1
                to_del.append(old_title)
    # ---
    printe.output('===================')
    if tat != '':
        printe.output('<<lightred>> redirects: ')
        printe.output(tat)
        printe.output('===================')
    # ---
    printe.output('replace %d pages. ' % rep)
    printe.output('remove %d pages. ' % remo)
    # ---
    if len(to_del) > 0:
        printe.output(f'delete {len(to_del)} pages. ')
        printe.output(to_del)
    # ---
    if len(to_add) > 0:
        printe.output(f'add {len(to_add)} pages. ')
        printe.output(to_add)
        sql_for_mdwiki.add_titles_to_qids(to_add)
        # ---


# ---
if __name__ == '__main__':
    get_pages()
# ---
