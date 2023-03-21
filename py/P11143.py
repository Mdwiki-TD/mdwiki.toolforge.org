#!/usr/bin/python

"""

python3 pwb.py mdpy/P11143

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import codecs
import sys
import os
import json
import time
import py_tools
#---
import sql_for_mdwiki
#---
qids = {}
for qq in sql_for_mdwiki.mdwiki_sql('select DISTINCT qid, title from qids;'): 
    q   = py_tools.Decode_bytes(qq[0])
    title = py_tools.Decode_bytes(qq[1]).replace('_', ' ')
    qids[q] = title
#---
sys.argv.append('workhimo')
#---
import wikidataapi 
wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php" )
# wikidataapi.post( params , apiurl = '' )
# wikidataapi.Get_page_qids( sitecode , titles )
# wikidataapi.Get_sitelinks_From_Qid( q )
# wikidataapi.WD_Merge( q1, q2)
# wikidataapi.Labels_API(Qid, label, lang, remove = False)
# wikidataapi.sparql_generator_url(quary, printq = False, add_date = True)
# wikidataapi.wbsearchentities(search, language)
# wikidataapi.
#---
query = '''
#  query to get items has property P11143 in wikidata
select distinct ?item where { ?item wdt:P11143 ?prop .} '''
#---
in_wd = []
#---
wdlist = wikidataapi.sparql_generator_url(query, printq = False, add_date = True)
#---
for wd in wdlist:
    q = wd['item'].split('/entity/')[1]
    in_wd.append(q)
#---
newlist = [ x for x in qids.keys() if x not in in_wd ]
#---
print('len of newlist: ' + str(len(newlist)))
#---
n = 0
#---
for q in newlist:
    n += 1
    print(f'q {n} from {len(newlist)}')
    wikidataapi.Claim_API_str(q, 'P11143', qids[q])
    # break
#---