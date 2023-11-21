#!/usr/bin/python3
"""

إنشاء قائمة بعدد المراجع

python3 core8/pwb.py /data/project/mdwiki/mdpy/countref less100

python3 core8/pwb.py mdpy/countref newpages

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import json
import codecs
import re
import os
import sys
from mdpy.bots import sql_for_mdwiki
from TDpynew import ref
from mdpy.bots import mdwiki_api
from mdpy import printe
from mdpy.bots import catdepth2

# ---
project = '/data/project/mdwiki/'
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
all_ref = {}
lead_ref = {}
vaild_links = {1: []}
list_ma = {1: []}
# ---
file_all = project + '/public_html/Translation_Dashboard/Tables/all_refcount.json'
file_lead = project + '/public_html/Translation_Dashboard/Tables/lead_refcount.json'
# ---
a = {}
# ---
a = json.loads(codecs.open(file_all, "r", encoding="utf-8").read())
# ---
all_ref = {x: ref for x, ref in a.items() if ref > 0}
# ---
la = {}
# ---
la = json.loads(codecs.open(file_lead, "r", encoding="utf-8").read())
# ---
lead_ref = {x: ref for x, ref in la.items() if ref > 0}
# ---
# list for titles in both all_ref and lead_ref
list_fu = list(set(all_ref.keys()) & set(lead_ref.keys()))
# ---
# remove duplicates from list
list_fu = list(set(list_fu))
list_ma[1] = [x for x in list_fu if (x in all_ref and x in lead_ref)]


def count_ref_from_text(text, get_short=False):
    # ---
    short_ref = re.compile(r'<ref\s*name\s*\=\s*(?P<name>[^>]*)\s*\/\s*>', re.IGNORECASE | re.DOTALL)
    # ---
    ref_list = []
    # ---
    # count = 0
    # ---
    if get_short:
        for m in short_ref.finditer(text):
            name = m.group('name')
            if name.strip() != '':
                if name.strip() not in ref_list:
                    ref_list.append(name.strip())
    # ---
    # refreg = re.compile(r'(<ref[^>]*>[^<>]+</ref>|<ref[^>]*\/\s*>)')
    refreg = re.compile(r'(?i)<ref(?P<name>[^>/]*)>(?P<content>.*?)</ref>', re.IGNORECASE | re.DOTALL)
    # ---
    for m in refreg.finditer(text):
        # content = m.group('content')
        # if content.strip() != '' : if not content.strip() in ref_list : ref_list.append(content.strip())
        # ---
        name = m.group('name')
        content = m.group('content')
        # ---
        if name.strip() != '':
            if name.strip() not in ref_list:
                ref_list.append(name.strip())
        elif content.strip() != '':
            if content.strip() not in ref_list:
                ref_list.append(content.strip())
            # count += 1
    # ---
    count = len(ref_list)
    # ---
    return count


def count_refs(title):
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    text2 = ref.fix_ref(text, text)
    # ---
    all_c = count_ref_from_text(text2)
    all_ref[title] = all_c
    # ---
    leadtext = text2.split('==')[0]
    lead_c = count_ref_from_text(leadtext, get_short=True)
    # ---
    lead_ref[title] = lead_c
    # ---
    printe.output('<<lightgreen>> all:%d \t lead:%d' % (all_c, lead_c))


def logaa(file, table):
    with open(file, 'w') as outfile:
        json.dump(table, outfile, sort_keys=True, indent=4)
    outfile.close()
    # ---
    printe.output(f'<<lightgreen>> {len(table)} lines to {file}')


def from_sql():
    # ---
    que = '''select title, word from pages;'''
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    titles2 = [q['title'] for q in sq]
    # ---
    titles = [x for x in titles2 if x not in list_ma[1]]
    # ---
    printe.output(f'<<lightyellow>> sql: find {len(titles2)} titles, {len(titles)} to work. ')
    return titles


def get_links():
    tabe = catdepth2.subcatquery2('RTT', depth='1', ns='0')
    lale = tabe['list']
    # ---
    if 'sql' in sys.argv:
        lale = from_sql()
    # ---
    if 'newpages' in sys.argv:
        lale = [x for x in lale if (x not in list_ma[1])]
    # ---
    return lale


def mai():
    # ---
    numb = 0
    # ---
    vaild_links[1] = get_links()
    # ---
    limit = 10000
    if 'limit100' in sys.argv:
        limit = 100
    # ---
    # python pwb.py mdwiki/public_html/Translation_Dashboard/countref test1 local -title:Testosterone_\(medication\)
    # python3 core8/pwb.py /data/project/mdwiki/mdpy/countref test1 -title:Testosterone_\(medication\)
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg == "-title":
            vaild_links[1].append(value.replace('_', ' '))
        # ---
    # ---
    for x in vaild_links[1]:
        # ---
        numb += 1
        # ---
        if numb >= limit:
            break
        # ---
        printe.output(' p %d from %d: for %s:' % (numb, len(vaild_links[1]), x))
        # ---
        count_refs(x)
        # ---
        if numb == 10 or str(numb).endswith('00'):
            logaa(file_lead, lead_ref)
            logaa(file_all, all_ref)
        # ---
    # ---
    logaa(file_lead, lead_ref)
    logaa(file_all, all_ref)


if __name__ == '__main__':
    mai()
