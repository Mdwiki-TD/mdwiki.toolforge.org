#!/usr/bin/python
"""
python3 pwb.py mdpy/days_7

"""
#
# (C) Ibrahem Qasim, 2023
#
#
from mdpy import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
qua = 'delete from pages where target = '' and date < ADDDATE(CURDATE(), INTERVAL -7 DAY)'
#---
print(qua)
#---
ty = sql_for_mdwiki.mdwiki_sql(qua, update=True)
#---
print(ty)
#---