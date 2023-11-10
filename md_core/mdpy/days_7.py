#!/usr/bin/python3
"""
python3 core8/pwb.py mdpy/days_7

"""
#
# (C) Ibrahem Qasim, 2023
#
#
from mdpy.bots import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# ---
qua = '''
delete from pages
where target = ''
# and DATEDIFF(CURDATE(),date) > 7
# and date < ADDDATE(CURDATE(), INTERVAL -7 DAY)
# and date < DATE_SUB(CURDATE(), INTERVAL 7 DAY)
and date < DATE_SUB(current_timestamp(), INTERVAL 7 DAY)
'''
# ---
print(qua)
# ---
ty = sql_for_mdwiki.mdwiki_sql(qua, update=True)
# ---
print(ty)
# ---
