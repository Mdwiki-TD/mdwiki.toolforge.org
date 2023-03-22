#!/usr/bin/python

"""

python3 ./core/pwb.py mdpy/P11143

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import codecs
import sys
import os
import json
import time
import py_tools
#---
sys.argv.append('workhimo')
#---
import wikidataapi 
wikidataapi.Log_to_wiki(url="https://www.wikidata.org/w/api.php" )
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
qids_di = sql_for_mdwiki.get_all_qids()
#---
qids = { q : title for title, q in qids_di.items() if q != '' }
#---
query = '''select distinct ?item ?prop where { ?item wdt:P11143 ?prop .}'''
#---
in_wd = {}
#---
wdlist = wikidataapi.sparql_generator_url(query, printq = False, add_date = True)
#---
for wd in wdlist:
    prop = wd['prop']
    #---
    qid = wd['item'].split('/entity/')[1]
    #---
    in_wd[qid] = prop
#---
print(f'len of in_wd: {len(in_wd)}')
#---
newlist = { q: tt for q, tt in qids.items() if q not in in_wd.keys() }
#---
print('len of newlist: ' + str(len(newlist)))
#---
def add_missing():
    #---
    n = 0
    #---
    for q, value in newlist.items():
        n += 1
        print(f'q {n} from {len(newlist)}')
        wikidataapi.Claim_API_str(q, 'P11143', value)
#---
if 'add' in sys.argv:
    add_missing()
#---
merge_qids = {**newlist, **in_wd}
#---
def fix():
    # mdwiki != P11143
    # تصحيح قيم الخاصية التي لا تساوي اسم المقالة
    #---
    for q, wd_value in merge_qids.copy().items():
        md_title = qids.get(q)
        if md_title == wd_value: 
            continue
        #---
        print(f'wd_value:{wd_value} != md_title:{md_title}, qid:{q}')
        #---
        merge_qids[q] = md_title
        #---
        # delete the old
        ae = wikidataapi.Get_claim(q, 'P11143', get_claim_id=True)
        if ae:
            for x in ae:
                value = x['value']
                claimid = x['id']
                if value == wd_value:
                    uxx = wikidataapi.Delete_claim(claimid)
                    if uxx:
                        print(f'True.. Deleted {claimid}')
                    else:
                        print(f'Failed to delete {claimid}')
        #---
        # add the correct claim
        ase = wikidataapi.Claim_API_str(q, 'P11143', md_title)
        if ase:
            print(f'True.. Added P11143:{md_title}')
        else:
            print(f'Failed to add P11143:{md_title}')
#---
if 'fix' in sys.argv:
    fix()
#---
def duplict():
    # ايجاد عناصر ويكي بيانات بها قيمة الخاصية في أكثر من عنصر
    va_tab = {}
    #---
    for q, va in merge_qids.items():
        if not va in va_tab: va_tab[va] = []
        if not q in va_tab[va]: va_tab[va].append(q)
    #---
    check = { value : qs for qs, value in va_tab.items() if len(qs) > 1 }
    #---
    for va, qs in check.items():
        print(f'va:{va}, qs:{qs}')
#---
if 'duplict' in sys.argv:
    duplict()
#---