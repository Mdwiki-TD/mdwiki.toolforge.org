#!/usr/bin/env python
# -*- coding: utf-8  -*-
#   himo
"""
python3 pwb.py mdpy/cashwd

"""
#
# (C) Ibrahem Qasim, 2022
#
#

import json
import codecs
from warnings import warn
import pywikibot
import os
import sys
import datetime
from datetime import datetime
Day_History = datetime.now().strftime("%Y-%m-%d")
#---
sys_argv = sys.argv or []
#---
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
#---
#---
import wikidataapi 
# wikidataapi.Log_to_wiki("mdwiki" , lang = "www" )
# wikidataapi.post( params )
#---
import py_tools

# py_tools.
#---
import mdwiki_api

















#---
import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---
#---
redirects_qids = {}
mis_qids = []
#---
main_table_sites = {}
#---
missing = {'all' : 0, 'date' : Day_History, 'langs' : {} }
#---
def get_qids_sitelinks( qidslist ):
    #---
    splits = py_tools.split_lists_to_numbers( list( qidslist.keys() ), maxnumber = 100 )
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
    for _, qids in splits.items():
        #---
        params_wd["ids"] = '|'.join( qids )
        #---
        pywikibot.output('<<lightgreen>> done:%d from %d, get sitelinks for %d qids.' % ( len(all_entities),len(list( qidslist.keys() )), len(qids) ) )
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
            ma = kk.get("missing")
            if ma:
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
            for _, tab in kk.get("sitelinks",{}).items():
                #---
                title = tab.get("title",'')
                site = tab.get("site",'')
                #---
                if title == '' or not site.endswith("wiki"):
                    continue
                #---
                site = site[:-4]
                #---
                if not site in heads:  heads.append( site )
                #---
                if not site in main_table_sites: main_table_sites[site] = []
                # add mdwiki title to cash_exists/wiki.json table
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
    pywikibot.output('<<lightgreen>> cash_wd' )
    #---
    mdwiki_pages = mdwiki_api.subcatquery('RTT', depth='3', ns='all')
    #---
    titles = []
    for dd in mdwiki_pages:
        if not dd.startswith("User:") and not dd.startswith("Category:") :
            titles.append(dd)
    #---
    pywikibot.output('<<lightgreen>> len of mdwiki_api.subcatquery:RTT:%d.' % len(titles) )
    #---
    # qids_list = [ en_to_md.mdtitle_to_qid[x] for x in titles if x in en_to_md.mdtitle_to_qid ]
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
    with open( project + '/public_html/Translation_Dashboard/Tables/sitelinks.json' , 'w') as hjh:
        json.dump( lists, hjh )
    hjh.close()
    #---
    with open( project + '/public_html/Translation_Dashboard/Tables/sitelinks_list.json' , 'w') as hjh:
        json.dump( table_l, hjh, ensure_ascii=False, indent=4 )
    hjh.close()
    #---
    table_to_log = { "redirects": redirects_qids, "missing": mis_qids }
    with open( project + '/public_html/Translation_Dashboard/Tables/qid_redirects_missing.json' , 'w') as llk:
        json.dump( table_to_log, llk )
    llk.close()
    # copy it to file2
    file2 = project + '/qid_redirects_missing.json'
    #---
    with open( file2 , 'w') as llk:
        json.dump( table_to_log, llk )
    llk.close()
    #---
    for site, liste in main_table_sites.items():
        pywikibot.output('<<lightblue>> main_table_sites:%s, len:%d.' % (site, len(liste)) )
        #---
        # remove duplicates
        liste = list(set(liste))
        #---
        leeen = int(len(titles)) - int(len( liste ))
        missing['langs'][site] = { 'missing' : leeen, 'exists' : len( liste ) }
        #---
        json_file = '/public_html/Translation_Dashboard/cash_exists/%s.json' % site
        #---
        # dump liste to json_file
        try:
            with codecs.open( project + json_file, 'w', encoding="utf-8") as yuy: 
                json.dump( liste, yuy, ensure_ascii=False, indent=4 )
            yuy.close()
            pywikibot.output('<<lightgreenn>>dump to cash_exists/%s.json done..' % site )
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
    with open( project + '/public_html/Translation_Dashboard/Tables/noqids.json' , 'w') as tyt:
        json.dump( noqids, tyt )
    tyt.close()
    #---
    noqids1 = [ x for x in noqids if not x in en_to_md.other_qids_json ]
    #---
    pywikibot.output("xxxxxxxx\n noqids1:" )
    numb = 0
    for f in noqids1:
        numb += 1
        pywikibot.output('<<lightblue>> %d mdtitle:%s not in mdwiki_to_qid.' % (numb, f.ljust(40)) )
    #---
    pywikibot.output("xxxxxxxx\n noqids2:" )
    numb = 0
    noqids2 = [ x for x in noqids if x in en_to_md.other_qids_json ]
    for f in noqids2:
        numb += 1
        pywikibot.output('<<lightyellow>> %d mdtitle:%s empty in other_qids_json.' % (numb, f.ljust(40)) )
    #---
    # redirects_qids
    # mis_qids
    #---
    for old_q, new_q in redirects_qids.items():
        pywikibot.output('<<lightblue>> redirects_qids:%s -> %s.' % (old_q.ljust(15), new_q) )
    #---
    for qd in mis_qids:
        pywikibot.output('<<lightblue>> missing_qids:%s.' % qd )
    #--- 
    pywikibot.output(' len of noqids1:         %d' % len(noqids1) )
    pywikibot.output(' len of noqids2:         %d' % len(noqids2) )
    pywikibot.output(' len of redirects_qids:  %d' % len(redirects_qids.keys()) )
    pywikibot.output(' len of missing_qids:    %d' % len(mis_qids) )
    #---
    with open( project + '/public_html/Translation_Dashboard/Tables/missing.json', 'w') as hhg:
        json.dump(missing, hhg)
        pywikibot.output(' log to missing.json true.... ' )
    hhg.close()
    #---
#---
if __name__ == '__main__':
    cash_wd()
#---