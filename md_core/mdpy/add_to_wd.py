#!/usr/bin/python

"""
بوت فرعي من 
mdpy/sql.py

#---
from mdpy import add_to_wd
# add_to_wd.add_tab_to_wd(New_Table_by_lang)
#---

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re
import codecs
import os
import pywikibot
import string
import sys
#---
from mdpy import py_tools
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
#---
from mdpy import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
from mdpy import wiki_api
from mdpy import printe
#---
from mdpy import mdwiki_api

#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
from mdpy import en_to_md
# en_to_md.mdtitle_to_qid
# en_to_md.enwiki_to_mdwiki
# en_to_md.mdwiki_to_enwiki
#---
from mdpy import orred
#---
'''CREATE TABLE wddone (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    mdtitle VARCHAR(120) NOT NULL,
    target VARCHAR(120) NOT NULL,
    lang VARCHAR(30) NOT NULL,
    user VARCHAR(120) NOT NULL
    )'''
#---
que_wddone = '''
select mdtitle,target,lang,user 
from wddone
;
'''
#---
sq_dd = sql_for_mdwiki.mdwiki_sql(que_wddone, return_dict=True)
#---
wddone_by_u_t = []
wddone_by_u_l_mdt = []
#---
for tab in sq_dd :
    mdtitle = tab['mdtitle']
    target  = tab['target']
    lang    = tab['lang']
    user    = tab['user']
    #---
    wddone_by_u_t.append(tuple([user,target]))
    wddone_by_u_l_mdt.append(tuple([user,lang,mdtitle]))
    #---
from mdpy import wikidataapi
wikidataurl = "https://www.wikidata.org/w/api.php"
#---
def work_with_2_qids(oldq, new_q):
    #---
    printe.output("=============================")
    printe.output("start:work_with_2_qids: oldq:%s, new_q:%s" % (oldq,new_q))
    #---
    fas = wikidataapi.Get_sitelinks_From_Qid( oldq ) 
    #{'sitelinks': {'enwiki': 'User:Mr. Ibrahem/Baricitinib', 'orwiki': 'ବାରିସିଟିନିବ'}, 'q': 'Q112331510'}
    #---
    false_sitelinks = fas.get('sitelinks',{})
    #---
    len_sites = len(false_sitelinks)
    #---
    printe.output( '<<lightblue>> len_sites %s' % len_sites )
    #---
    printe.output( false_sitelinks )
    #---
    en = false_sitelinks.get('enwiki','')
    #---
    if en.startswith('User:Mr. Ibrahem'):
        printe.output( '<<lightblue>> remove sitelink %s' % en )
        remove = wikidataapi.post( {"action":"wbsetsitelink","id":oldq,"linksite":"enwiki"}, apiurl=wikidataurl, token = True)
        if 'success' in remove:
            len_sites -= 1
            printe.output('<<lightgreen>> **remove sitelink true.' )
        else:
            printe.output('<<lightred>> **remove sitelink false.' )
            printe.output( remove )
        #---
        remove2 = wikidataapi.post( {"action": "wbsetlabel","id": oldq,"language": "en","value": ""}, apiurl=wikidataurl, token = True)
        if 'success' in remove2:
            len_sites -= 1
            printe.output('<<lightgreen>> **remove2 label true.' )
        else:
            printe.output('<<lightred>> **remove2 label false.' )
            printe.output( remove2 )
    #---
    if len_sites == 1 or len_sites == 0:
        printe.output( '<<lightblue>> merge qids')
        mer = wikidataapi.WD_Merge( oldq, new_q )
        return mer
    #---
    return False
#---
def add_wd(qid, enlink, lang, target):
    params = {
        "action": "wbsetsitelink",
        "linktitle": target,
        "linksite": lang+'wiki',
        #"title": enlink,
        #"site": 'enwiki',
        "format" : "json",
        "utf8" : 1
    }
    #---
    if qid != "":
        params['id'] = qid
    else:
        params['title'] = enlink
        params['site']  = 'enwiki'
    #---
    ss = wikidataapi.post( params, apiurl=wikidataurl, token = True)
    #---
    printe.output(ss)
    #---
    if ss and "success" in ss : return True
    #---
    # ss = {'error': {'code': 'failed-save', 'info': 'The save has failed.', 'messages': [{'name': 'wikibase-api-failed-save', 'parameters': [], 'html': {'*': 'لم ينجح الحفظ.'}}, {'name': 'wikibase-validator-sitelink-conflict', 'parameters': ['[https://ar.wikipedia.org/wiki/%D8%A5%D9%8A%D9%81%D8%A7%D9%83%D8%A7%D9%81%D8%AA%D9%88%D8%B1 arwiki:إيفاكافتور]', '[[Q113952553|Q113952553]]'], 'html': {'*': 'الوصلة <a class="external text" href="https://ar.wikipedia.org/wiki/%D8%A5%D9%8A%D9%81%D8%A7%D9%83%D8%A7%D9%81%D8%AA%D9%88%D8%B1">arwiki:إيفاكافتور</a> مستخدمة للعنصر <a href="/wiki/Q113952553" title="Q113952553">Q113952553</a>. يمكنك إزالتها من <a href="/wiki/Q113952553" title="Q113952553">Q113952553</a> إن لم تكن مناسبة هناك أو أن تدمج العنصرين إذا كانا عن نفس الموضوع تماماً.'}}], '*': 'See https://www.wikidata.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1402'}
    #---
    if type(ss) != dict: return False
    #---
    error = ss.get('error',{}).get('code',{})
    #---
    if str(ss).find('wikibase-validator-sitelink-conflict') != -1:
        qii = re.match('.*\"\>(Q\d+)\<\/a.*' , str(ss) ) 
        #---
        if qii : 
            qid2 = qii.group(1)
            #---
            if qid == "":
                qids_from_wiki = wiki_api.Get_page_qids( "en", [enlink] )
                #---
                for x,tab in qids_from_wiki.items():
                    qid = tab.get('q','')
                    break
            #---
            uu = work_with_2_qids(qid2, qid)
            return uu
            #---
    #---
    return False
#---
def Add_to_wikidata(mdtitle, lang, target, user):
    #---
    qid    = en_to_md.mdtitle_to_qid.get(mdtitle,"")
    enlink = en_to_md.mdwiki_to_enwiki.get(mdtitle, mdtitle)
    #---
    ss = add_wd(qid, enlink, lang, target)
    #---
    if ss == True :
        #---
        done_qua = """
        INSERT INTO wddone (mdtitle, target, lang, user)
        SELECT {mdtit}, {tar}, '{lang}', {user}
        WHERE NOT EXISTS (SELECT 1
            FROM wddone 
                WHERE mdtitle = {mdtit}
                AND target = {tar}
                AND lang = '{lang}'
                AND user = {user}
                )""".format(
            mdtit = py_tools.make_cod(mdtitle), 
            tar   = py_tools.make_cod(target), 
            lang  = lang, 
            user  = py_tools.make_cod(user)
        )
        printe.output('**************')
        printe.output(done_qua)
        printe.output('**************')
        vfg = sql_for_mdwiki.mdwiki_sql(done_qua, update=True)
    #---
    tat = mdwiki_api.GetPageText(mdtitle)
    #---
    lalas = '[[%s:' % lang
    #---
    line = '[[%s:%s]]' % ( lang,target )
    if tat != '' and tat.find( line ) == -1 and tat.find( lalas ) == -1 : 
        mdwiki_api.Add_To_Bottom( '\n' + line , 'add link to %s' % line , mdtitle , False )
    #---
    if lang == "or":
        orred.create_redirect( target, mdtitle )
#---
def add_tab_to_wd(table):
    #---
    if 'justsql' in sys.argv : return ''
    #---
    for lane, tab in table.items() :
        #---
        number = 0
        #---
        for tt in tab :
            tabe = tab[tt]#{"mdtitle": md_title.replace("'" , "\'") , "target": target, "user":user.replace("'" , "\'"),"lang":lange}
            #---
            mdtitle= tabe['mdtitle']
            lang   = tabe['lang']
            target = tabe['target']
            user   = tabe['user']
            ns     = tabe['namespace']
            #---
            if str(ns) != '0': continue
            #---
            if tuple([user, target]) in wddone_by_u_t : continue
            #---
            if tuple([user, lang, mdtitle]) in wddone_by_u_l_mdt : continue
            #---
            number += 1
            #---
            printe.output( '=========================' )
            printe.output( '<<lightgreen>>p %d/%d: mdtitle:%s,lang:%s,target:%s' % ( number, len(tab), mdtitle, lang, target)  )
            #---
            Add_to_wikidata( mdtitle, lang, target, user)
#---