#!/usr/bin/python3
"""

page views bot

python3 core8/pwb.py mdpy/enwiki_views

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import os
import codecs
import json
import traceback
import pywikibot
import datetime
from datetime import timedelta

# ---
from mdpy.bots import wiki_api
from mdpy import printe

# ---
from mdpy.bots.en_to_md import enwiki_to_mdwiki, mdwiki_to_enwiki

# --
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'


def get_RTT():
    RTT = []
    # ---
    filename = project + '/public_html/Translation_Dashboard/cats_cash/RTT.json'
    # ---
    try:
        textn = codecs.open(filename, "r", encoding="utf-8").read()
    except Exception:
        pywikibot.output('Traceback (most recent call last):')
        pywikibot.output(traceback.format_exc())
        pywikibot.output('CRITICAL:')
        textn = ''
    # ---
    Table = {}
    if textn != '':
        Table = json.loads(textn)
    # ---
    RTT = Table['list']
    # ---
    printe.output(f'len of RTT: {len(RTT)}')
    # ---
    return RTT


def get_RTT2():
    # ---
    RTT = []
    # ---
    sitelinks_file = project + '/public_html/Translation_Dashboard/Tables/sitelinks.json'
    # ---
    print(f'get sitelinks from {sitelinks_file}')
    # ---
    sitelinks_all = json.loads(codecs.open(sitelinks_file, "r", encoding="utf-8").read())
    # ---
    diff = 0
    # ---
    qids = sitelinks_all.get('qids', {})
    # ---
    for qid, tab in qids.items():
        mdtitle = tab['mdtitle']
        en = tab.get('sitelinks', {}).get('en', '')
        if mdtitle != '' and en != '':
            RTT.append(mdtitle)
            if mdtitle != en:
                diff += 1
        else:
            printe.output(f'mdtitle:{mdtitle} or en:{en} == ""')
    # ---
    printe.output(f'len of RTT:{len(RTT)}, len of qids:{len(qids.keys())}, diff:{diff}')
    # ---
    return RTT


def main():
    # ---
    RTT = get_RTT()
    # ---
    en_keys = [mdwiki_to_enwiki.get(cc, cc) for cc in RTT]
    # ---
    en_keys.append('Cisatracurium')
    # ---
    # enviews = wiki_api.get_page_views(en_keys, site='en', days=30)
    # ---
    d_end = datetime.datetime.utcnow() - timedelta(days=1)
    d_start = d_end - timedelta(weeks=4)
    # ---
    d_end = d_end.strftime('%Y%m%d')
    d_start = d_start.strftime('%Y%m%d')
    # ---
    print(f'start get_views_with_rest_v1: lenth: {len(en_keys)}')
    # ---
    enviews = wiki_api.get_views_with_rest_v1('en', en_keys, date_start=d_start, date_end=d_end)
    # ---
    printe.output(f'len of enviews: {len(enviews.keys())}')
    # ---
    no_views = 0
    # ---
    enwiki_pageviews = project + '/public_html/Translation_Dashboard/Tables/enwiki_pageviews.json'
    # ---
    old_views = json.loads(codecs.open(enwiki_pageviews, "r", encoding="utf-8-sig").read())
    # ---
    n_views = {x: z for x, z in old_views.items()}
    # ---
    for k, view in enviews.items():
        if view == 0:
            no_views += 1
            continue
        # ---
        if enwiki_to_mdwiki.get(k):
            k = enwiki_to_mdwiki.get(k)
        # ---
        n_views[k] = view['all']
    # ---
    printe.output(f'no_views:{no_views},\t len of n_views: {len(n_views.keys())}')
    # ---
    with open(enwiki_pageviews, 'w') as outfile:
        json.dump(n_views, outfile, sort_keys=True, indent=4)
    outfile.close()

    # ---
    # add_to_mdwiki_sql(numbers , lange)
    # ---


# ---
if __name__ == '__main__':
    main()
# ---
