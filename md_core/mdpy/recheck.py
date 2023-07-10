#!/usr/bin/python

"""
التحقق من ربط المقالات بالعنصر المناسب في ويكي بيانات

python3 pwb.py mdwiki/mdpy/recheck
python3 pwb.py mdpy/recheck

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re
import json
import codecs
import pywikibot
import string
import sys
import os
import time
#---
from mdpy import printe
from mdpy.bots import wiki_sql

# wiki_sql.GET_SQL()
# wiki_sql.Make_sql_many_rows( queries , wiki="", printqua = False)
#---
from mdpy.bots import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query , update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab)
#---
from mdpy.bots import py_tools
from pymysql.converters import escape_string

# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# escape_string(string)
# py_tools.Decode_bytes( x )
#---
from mdpy.bots import wikidataapi
wikidataurl = "https://www.wikidata.org/w/api.php"
#---
from mdpy.bots import wiki_api
#---
targets_done = {}
#---
def dodo_sql():
    #---
    lang_o = ""
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "lang" or arg == "-lang":
            lang_o = value
    #---
    que = ''' select title,user,lang,target from pages #where target = ""'''
    #---
    if lang_o != "":
        que += '\nwhere lang = "%s"' % lang_o
    #---
    que += "\n;"
    #---
    printe.output(que)
    #---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    #---
    len_no_target = 0
    len_done_target = 0
    #---
    for tab in sq:
        title  = tab['title']
        user   = tab['user']
        target = tab['target']
        lang   = tab['lang'].lower()
        #---
        if lang_o != "" and lang != lang_o.strip(): continue
        #---
        len_done_target += 1
        if not lang in targets_done:
            targets_done[lang] = {}
        target = target.replace("_", " ")
        # targets_done[lang][py_tools.ec_de_code(target , 'encode')] = { "user" : user , "target" : target, "mdtitle" : title }
        targets_done[lang][target] = {"user": user, "target": target, "mdtitle": title}
    #---
    printe.output("<<lightyellow>> find %d with target, and %s without "% (len_done_target, len_no_target))
#---
wd_tt = {}
#---
dodo_sql()
#---
def do_it_sql(lange, targets):
    #---
    all_list = py_tools.split_lists_to_numbers(list(targets.keys()), maxnumber=100, out=False)
    #---
    for nu, t_list in all_list.items():
        #---
        ase = [escape_string(t.strip().replace(" ", "_")) for t in t_list if t.strip() != ""]
        #---
        if ase == []:   continue
        #---
        laly = "'" + "', '".join(ase) + "'"
        #---
        query = f"""
            select DISTINCT p.page_title, pp.pp_value
            from page p, page_props pp 
            where p.page_id = pp.pp_page
            and pp.pp_propname='wikibase_item'
            and p.page_namespace = 0
            and p.page_title in ({laly})
            ;"""
        #---
        # printe.output('--------------------')
        #---
        result = wiki_sql.Make_sql_many_rows(query, wiki=str(lange))
        #---
        res_len = len(result)
        #---
        if res_len == len(t_list):
            printe.output("<<lightgreen>> len(result) == len(t_list) 100.")
        #---
        result_n = []
        #---
        if result:
            printe.output('recheck.py len(result) = "{}"'.format(res_len))
            #---
            for liste in result:
                #---
                target = py_tools.Decode_bytes(liste[0])
                pp_value = py_tools.Decode_bytes(liste[1])
                #---
                target = target.replace("_", " ")
                result_n.append(target)
                #---
                md_title = targets.get(target, {}).get("mdtitle", "")
                #---
                wd_tt[target] = {"mdtitle": md_title, "lang": lange, "qid": pp_value}
        #---
        if res_len < len(t_list):
            diff = len(t_list) - res_len
            # printe.output( query )
            itemdiff = [t for t in t_list if t.strip() != "" and t not in result_n]
            len_missing = len(itemdiff)
            if len_missing > 0:
                printe.output("recheck.py %d missing from %d" % (diff, len(t_list)))
                printe.output("recheck.py missing:(%d):%s" % (len_missing, ",".join(itemdiff)))
        #---
#---
def do_it_api(lange, targets):
    #---
    New_targets = list(targets.keys())
    #---
    limits = 100
    #---
    if "tests" in sys.argv and len(New_targets) > 100:
        New_targets = New_targets[:100]
        limits = 25
    #---
    withqid = 0
    noqid = 0
    nomd = 0
    #---
    all_list = py_tools.split_lists_to_numbers(New_targets, maxnumber=limits, out=False)
    #---
    for nu, t_list in all_list.items():
        # get all pages qid
        qids_from_wiki = wiki_api.Get_page_qids(lange, t_list)
        #---
        qids = {}
        for title, tab in qids_from_wiki.items():
            # tab={'isRedirectPage':True,'missing':True,'from':red["from"],'to':red["to"],'title':red["from"],'ns':'','q':''}
            # tab={'missing':True,'q':''}
            #---
            if "tests" in sys.argv:
                print(tab)
            #---
            title2 = title
            #---
            if tab.get("to"):
                print("{} is redirect to {}".format(tab["from"], tab["to"]))
                title2 = tab.get("to")
                qid = qids_from_wiki.get(title2, {}).get("q", "")
                qids[title] = qid
                qids[title2] = qid
            #---
            if tab.get("q", "") != "":
                withqid += 1
                print("{} is qid {}".format(title, tab["q"]))
                qids[title] = tab.get("q", "")
            #---
        #---
        for target in t_list:
            #---
            qid = qids.get(target, "")
            if qid == "":
                noqid += 1
                # printe.output('<<lightred>> %d qid is empty for "%s"' % ( noqid , target ) )
            #---
            md_title = targets.get(target, {}).get("mdtitle", "")
            if md_title == "":
                nomd += 1
                # printe.output( '<<lightred>> %d md_title is empty for "%s"' % ( nomd, target ) )
            #---
            wd_tt[target] = {"mdtitle": md_title, "lang": lange, "qid": qid}
    #---
    printe.output("<<lightyellow>> noqid %d" % noqid)
    printe.output("<<lightyellow>> nomd  %d" % nomd)
    printe.output("<<lightyellow>> withqid %d" % withqid)
    #---
    # return asde
#---
numb_lang = 0
for lange in targets_done:
    #---
    numb_lang += 1
    # printe.output( ' ================================ ')
    # printe.output( 'mdwiki/mdpy/sql.py: %d Lang : "%s"' % (numb_lang,lange) )
    #---
    # if "sql" in sys.argv:
    do_it_sql(lange, targets_done[lange])
    # else:
    # do_it_api(lange,targets_done[lange])
    #---
#---
from mdpy.bots import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---
mdwiki_empty_qids = {}
qids_to_merge = {}
empty_qid_target = []
#---
for target in wd_tt:
    mdtitle = wd_tt[target]["mdtitle"]
    lang = wd_tt[target]["lang"]
    #---
    qid_target = wd_tt[target]["qid"]
    qid_mdwiki = en_to_md.mdtitle_to_qid.get(mdtitle, "")
    #---
    tit2 = en_to_md.enwiki_to_mdwiki.get(mdtitle, "")
    qid_2 = en_to_md.mdtitle_to_qid.get(tit2, "")
    #---
    line22 = "%s:%s:%s" % (lang, target, qid_target)
    #---
    # printe.output( 'recheck: target:%s, lang:%s' % (target,lang) )
    #---
    if qid_mdwiki == "" and qid_2 == "":
        # printe.output( '<<lightred>> qid_mdwiki is empty for mdtitle:%s' % mdtitle )
        mdwiki_empty_qids[mdtitle] = (lang, target, qid_target)
        continue
    #---
    if qid_target == "":
        empty_qid_target.append("%s,qid_mdwiki:%s" % (line22, qid_mdwiki))
        # printe.output( '<<lightred>> qid_target is empty> target:%s' % dsd )
        continue
    #---
    if qid_mdwiki == "" and qid_2 != "":
        mdtitle = tit2
        qid_mdwiki = qid_2
        printe.output(f"<<lightyellow>> mdtitle: ({mdtitle}), tit2: ({tit2})")
        printe.output(f"<<lightyellow>> qid_mdwiki for mdtitle is empty, but qid_2 for tit2 is not empty")
    #---
    if qid_target == qid_mdwiki:
        continue
    #---
    # printe.output( '<<lightred>> qid_target != qid_mdwiki' )
    #---
    qids_to_merge[qid_target] = { "wd_qid": qid_mdwiki, "md_title": mdtitle, "lang": lang }
#---
printe.output('len(qids_to_merge) = "{}"'.format(len(qids_to_merge)))
#---
def work_with_2_qids(oldq, new_q):
    #---
    printe.output("=============================")
    printe.output("start:work_with_2_qids: oldq:%s, new_q:%s" % (oldq, new_q))
    #---
    fas = wikidataapi.Get_sitelinks_From_Qid(oldq)
    # {'sitelinks': {'enwiki': 'User:Mr. Ibrahem/Baricitinib', 'orwiki': 'ବାରିସିଟିନିବ'}, 'q': 'Q112331510'}
    #---
    false_sitelinks = fas.get("sitelinks", {})
    #---
    len_sites = len(false_sitelinks)
    #---
    printe.output("<<lightblue>> len_sites %s" % len_sites)
    #---
    printe.output(false_sitelinks)
    #---
    en = false_sitelinks.get("enwiki", "")
    #---
    if en.startswith("User:Mr. Ibrahem"):
        printe.output("<<lightblue>> remove sitelink %s" % en)
        remove = wikidataapi.post({"action": "wbsetsitelink", "id": oldq, "linksite": "enwiki"}, apiurl=wikidataurl, token=True)
        if "success" in remove:
            len_sites -= 1
            printe.output("<<lightgreen>> **remove sitelink true.")
        else:
            printe.output("<<lightred>> **remove sitelink false.")
            printe.output(remove)
        #---
        remove2 = wikidataapi.Labels_API(oldq, '', 'en', remove=True)
        #---
        if remove2:
            len_sites -= 1
            printe.output("<<lightgreen>> **remove2 label true.")
        else:
            printe.output("<<lightred>> **remove2 label false.")
    #---
    if len_sites == 1 or len_sites == 0:
        printe.output("<<lightblue>> merge qids")
        wikidataapi.WD_Merge(oldq, new_q)
    #---
    printe.output(" work_with_2_qids ends.........")
    printe.output("=============================")
#---
for oldq, tab in qids_to_merge.items():
    new_q = tab["wd_qid"]
    md_title = tab["md_title"]
    printe.output("<<lightblue>> oldq:%s, new_q:%s,md_title:%s" % (oldq, new_q, md_title))
    #---
    work_with_2_qids(oldq, new_q)
    #---
quary = """
SELECT ?q ?qlabel
WHERE {
  ?pid rdfs:label ?qlabel. FILTER((LANG(?qlabel)) = "en"). 
  FILTER (CONTAINS(?qlabel, "User:Mr. Ibrahem")).
}
LIMIT 100
"""
# newtabs = wikidataapi.sparql_generator_url(quary, printq = False, add_date = True)
newtabs = wikidataapi.wbsearchentities("User:Mr. Ibrahem", "en")
#---
numb = 0
#---
printe.output("work with newtabs: ")
printe.output('len(newtabs) = "{}"'.format(len(newtabs)))
#---
for oldqid, tab in newtabs.items():
    #---
    en = tab.get("label", "").replace("User:Mr. Ibrahem/", "")
    #---
    numb += 1
    print("------------------\n{}/{}".format(numb, len(newtabs)))
    print(f"false qid : {oldqid}")
    print(f"en title: {en}")
    #---
    # get qid for en page
    qid2 = en_to_md.mdtitle_to_qid.get(en, "")
    if qid2 == "":
        en2 = en_to_md.enwiki_to_mdwiki.get(en, en)
        qid2 = en_to_md.mdtitle_to_qid.get(en2, "")
    #---
    print(f"qid2: {qid2}")
    #---
    if qid2 == "":
        print("no qid for en page.")
        continue
    #---
    remove = wikidataapi.Labels_API(oldqid, "", "en", remove=True)
    #---
    work_with_2_qids(oldqid, qid2)
#---
printe.output("<<lightblue>> mdwiki_empty_qids:")
to_add = {}
#---
for mdm in mdwiki_empty_qids:
    lang, target, qid_target = mdwiki_empty_qids[mdm]
    printe.output(f"<<lightred>> no qid for md_title:{mdm}> {lang}: {target}, qid: {qid_target}")
    to_add[mdm] = qid_target
#---
printe.output("<<lightblue>> empty_qid_target:")
for lal in empty_qid_target:
    printe.output("<<lightred>> qid_target is empty> target:%s" % lal)
#---
if "addthem" in sys.argv:
    sql_for_mdwiki.add_titles_to_qids(to_add)