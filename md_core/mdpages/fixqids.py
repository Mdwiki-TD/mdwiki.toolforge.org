#!/usr/bin/env python
#   himo
"""
python3 core8/pwb.py mdpy/fixqids

"""
#
# ---
import sys
from mdpy.bots import catdepth2
from mdpy.bots import wikidataapi
from mdpy import printe
from mdpy.bots import sql_for_mdwiki
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
mdlist = sql_for_mdwiki.get_all_qids()
# ---
qs_list = {q: title for title, q in mdlist.items() if q != ''}


def fix_redirects(qs_list):
    # ---
    # python3 core8/pwb.py mdpy/fixqids redirects
    # ---
    printe.output('<<lightyellow>> start fix_redirects()')
    # ---
    new_list = list(qs_list.keys())
    # ---
    numb = 0
    # ---
    reds = wikidataapi.get_redirects(new_list)
    # ---
    printe.output(f'len of redirects: {len(reds)}')
    # ---
    for old_q, new_q in reds.items():
        numb += 1
        # ---
        printe.output(f'<<lightblue>> {numb}, old_q: {old_q}, new_q: {new_q}')
        # ---
        qua = f'update qids set qid = "{new_q}" where qid = "{old_q}"'
        # ---
        if 'fix' in sys.argv:
            # python3 core8/pwb.py mdpy/cashwd redirects fix
            sql_for_mdwiki.mdwiki_sql(qua, update=True)
        else:
            printe.output(qua)
            printe.output('add "fix" to sys.argv to fix them..')


def add_to_qids(mdlist):
    # ---
    printe.output('<<lightyellow>> start add_to_qids()')
    # ---
    all_pages = catdepth2.make_cash_to_cats(return_all_pages=True)
    # ---
    all_pages = [x for x in all_pages[:] if valid_title(x)]
    # ---
    all_in = [x for x in mdlist]
    # ---
    new_list = {title: '' for title in all_pages if title not in all_in}
    # ---
    printe.output(f'len of new_list: {len(new_list)}')
    # ---
    sql_for_mdwiki.add_titles_to_qids(new_list, add_empty_qid=True)


if __name__ == '__main__':
    fix_redirects(qs_list)
    print('_______________d')
    print('_______________d')
    print('_______________d')
    add_to_qids(mdlist)
