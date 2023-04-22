#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
"""
python3 ./core/pwb.py mdpy/cashwd

"""
#
# (C) Ibrahem Qasim, 2022
#
#

import json
import codecs
from warnings import warn
from mdpy import printe
import pywikibot
import os
import sys
import datetime
from datetime import datetime
Day_History = datetime.now().strftime("%Y-%m-%d")
#---
sys_argv = sys.argv or []
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
Dashboard_path = project + '/public_html/Translation_Dashboard'
#---
from mdpy import wikidataapi
from mdpy import py_tools
from mdpy import mdwiki_api
#---
from mdpy import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---
from mdpy import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
redirects_qids = {}
mis_qids = []
#---
main_table_sites = {}
#---
missing = {'all' : 0, 'date' : Day_History, 'langs' : {} }
#---
skip_codes = ["commons", "species", "ary", "arz", "meta"]
#---
change_codes = {
    "nb" : "no",
    "bat_smg" : "bat-smg",
    "be_x_old" : "be-tarask",
    "be-x-old" : "be-tarask",
    "cbk_zam" : "cbk-zam",
    "fiu_vro" : "fiu-vro",
    "map_bms" : "map-bms",
    "nds_nl" : "nds-nl",
    "roa_rup" : "roa-rup",
    "zh_classical" : "zh-classical",
    "zh_min_nan" : "zh-min-nan",
    "zh_yue" : "zh-yue",
}
#---
def get_qids_sitelinks( qidslist ):
    #---
    qs_list = list(qidslist.keys())
    #---
    params_wd = {
        "action": "wbgetentities",
        "format": "json",
        #"ids": ,
        "redirects": "yes",
        "props": "sitelinks",
        "utf8": 1
    }
    #---
    TEST = {
        "heads": ["arwiki"],
        "qids": {
            "Q1": { "mdtitle": "test","sitelinks": {"arwiki": "test"}}
        }
    }
    table_d = {"heads" : [], "qids" : {}}
    table_l = {"heads" : [], "qids" : {}}
    #---
    heads = []
    #---
    numb = 0
    #---
    all_entities = {}
    #---
    for i in range(0, len(qs_list), 100):
        #---
        qids = qs_list[i:i+100]
        #---
        params_wd["ids"] = '|'.join( qids )
        #---
        printe.output('<<lightgreen>> done:%d from %d, get sitelinks for %d qids.' % ( len(all_entities), len(qidslist), len(qids) ) )
        #---
        json1 = wikidataapi.post( params_wd , apiurl = 'https://www.wikidata.org/w/api.php' )
        #---
        if json1:
            #---
            entities = json1.get("entities",{})
            #---
            all_entities = {**all_entities, **entities}
        #---
        for qid_1, kk in all_entities.items():
            #---
            numb += 1
            if "missing" in kk:
                #---
                mis_qids.append( kk.get("id") )
                #---
                continue
            #---
            redirects = kk.get("redirects",{})
            if redirects: #"redirects": {"from": "Q113489270","to": "Q22792051"}
                redirects_qids[redirects.get("from")] = redirects.get("to")
            #---
            qid = kk.get("id",'')
            #---
            if qid != '' and not qid in table_d["qids"]:
                table_d["qids"][qid] = {"mdtitle" : '', "sitelinks" : {}}
                table_l["qids"][qid] = {"mdtitle" : '', "sitelinks" : []}
            #---
            mdwiki_title = qidslist.get(qid,'')
            if mdwiki_title != '':
                table_d["qids"][qid]["mdtitle"] = mdwiki_title
                table_l["qids"][qid]["mdtitle"] = mdwiki_title
            #---
            sitelinks = {}
            #---
            #"abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
            #---
            for _, tab in kk.get("sitelinks", {}).items():
                #---
                title = tab.get("title",'')
                site = tab.get("site",'')
                #---
                if site in skip_codes or site[:-4] in skip_codes: continue
                #---
                if title == '' or not site.endswith("wiki"):    continue
                #---
                site = site[:-4]
                #---
                site = change_codes.get(site) or site
                #---
                if not site in heads:  heads.append( site )
                #---
                if not site in main_table_sites: main_table_sites[site] = []
                #---
                # add mdwiki title to cash_exists/wiki.json table
                #---
                if mdwiki_title != '' and not mdwiki_title in main_table_sites[site]:
                    main_table_sites[site].append( mdwiki_title )
                #---
                sitelinks[site] = title
            #---
            table_d["qids"][qid]["sitelinks"] = sitelinks
            table_l["qids"][qid]["sitelinks"] = list( sitelinks.keys() )
            #---
    #---
    table_d["heads"] = heads
    table_l["heads"] = heads
    #---
    return table_d, table_l
#---
def cash_wd():
    #---
    printe.output('<<lightgreen>> cash_wd' )
    #---
    mdwiki_pages = mdwiki_api.subcatquery('RTT', depth='3', ns='all')
    #---
    titles = []
    for dd in mdwiki_pages:
        if not dd.startswith("User:") and not dd.startswith("Category:") :
            titles.append(dd)
    #---
    printe.output('<<lightgreen>> len of mdwiki_api.subcatquery:RTT:%d.' % len(titles) )
    #---
    qids_list = {}
    #---
    missing['all'] = len(titles)
    #---
    for x in titles:
        #---
        qid = en_to_md.mdtitle_to_qid.get(x, '')
        #---
        if qid != '': qids_list[qid] = x
    #---
    lists, table_l = get_qids_sitelinks( qids_list )
    #---
    json.dump( lists, open( Dashboard_path + '/Tables/sitelinks.json' , 'w') )
    #---
    # json.dump( table_l, open( Dashboard_path + '/Tables/sitelinks_list.json' , 'w'), ensure_ascii=False, indent=4 )
    #---
    # table_to_log = { "redirects": redirects_qids, "missing": mis_qids }
    #---
    # json.dump( table_to_log, open( Dashboard_path + '/Tables/qid_redirects_missing.json' , 'w') )
    #---
    for site, liste in main_table_sites.items():
        # printe.output('<<lightblue>> main_table_sites:%s, len:%d.' % (site, len(liste)) )
        #---
        # remove duplicates
        liste = list(set(liste))
        #---
        leeen = int(len(titles)) - int(len( liste ))
        missing['langs'][site] = { 'missing' : leeen, 'exists' : len( liste ) }
        #---
        json_file = f'{Dashboard_path}/cash_exists/{site}.json'
        #---
        if not os.path.exists( json_file ):
            printe.output(f'.... <<lightred>> file:"{site}.json not exists ....')
        #---
        # dump liste to json_file
        try:
            json.dump( liste, codecs.open( json_file, 'w', encoding="utf-8"), ensure_ascii=False, indent=4 )
            printe.output('<<lightgreenn>>dump to cash_exists/%s.json done..' % site )
        except Exception as e:
            pywikibot.output( 'Traceback (most recent call last):' )
            warn('Exception:' + str(e), UserWarning)
            pywikibot.output( 'CRITICAL:' )
            continue
    #---
    #email_address = "ibrahem.al-radaei@outlook.com"
    # send aleart email to email_address
    #---
    noqids = [ x for x in titles if not x in en_to_md.mdtitle_to_qid ]
    noqids.sort()
    #---
    json.dump( noqids, open( Dashboard_path + '/Tables/noqids.json' , 'w') )
    #---
    noqids1 = [ x for x in noqids if not x in en_to_md.other_qids_json ]
    #---
    printe.output("xxxxxxxx\n noqids1:" )
    numb = 0
    for f in noqids1:
        numb += 1
        printe.output('<<lightblue>> %d mdtitle:%s not in mdwiki_to_qid.' % (numb, f.ljust(40)) )
    #---
    printe.output("xxxxxxxx\n noqids2:" )
    numb = 0
    noqids2 = [ x for x in noqids if x in en_to_md.other_qids_json ]
    for f in noqids2:
        numb += 1
        printe.output('<<lightyellow>> %d mdtitle:%s empty in other_qids_json.' % (numb, f.ljust(40)) )
    #---
    # redirects_qids
    # mis_qids
    #---
    for old_q, new_q in redirects_qids.items():
        printe.output('<<lightblue>> redirects_qids:%s -> %s.' % (old_q.ljust(15), new_q) )
    #---
    for qd in mis_qids:
        printe.output('<<lightblue>> missing_qids:%s.' % qd )
    #--- 
    printe.output(' len of noqids1:         %d' % len(noqids1) )
    printe.output(' len of noqids2:         %d' % len(noqids2) )
    printe.output(' len of redirects_qids:  %d' % len(redirects_qids.keys()) )
    printe.output(' len of missing_qids:    %d' % len(mis_qids) )
    #---
    json.dump(missing, open( Dashboard_path + '/Tables/missing.json', 'w'))
    printe.output(' log to missing.json true.... ' )
    #---
#---
if __name__ == '__main__':
    cash_wd()
#---