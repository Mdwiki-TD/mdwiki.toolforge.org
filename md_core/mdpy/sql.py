#!/usr/bin/python

"""
بوت قواعد البيانات

python3 pwb.py mdpy/sql justsql break
python3 pwb.py mdpy/sql justsql
python3 pwb.py mdpy/sql

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
import time as tttime
#---
import add_to_wd
# add_to_wd.add_tab_to_wd(New_Table_by_lang)
#---
import py_tools
# py_tools.split_lists_to_numbers( lise , maxnumber = 100 )
# py_tools.ec_de_code( tt , type )
# py_tools.make_cod(string)
# py_tools.Decode_bytes(x)
#---
import wiki_sql
# wiki_sql.GET_SQL()
# wiki_sql.Make_sql_many_rows( queries , wiki="", printqua = False)
#---
import sql_for_mdwiki
# sql_for_mdwiki.mdwiki_sql(query , update = False)
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
cat_for_pages = {}
from fixcat import cat_for_pages
#---
Lang_usr_mdtitle = {}
targets_done = {}
Langs_to_title_and_user = {}
to_update_lang_user_mdtitle = {}
#---
printsql = { 1 : False }
#---
def add_to_mdwiki_sql(table):
    #Taba2 = {"mdtitle": md_title , "target": target, "user":user,"lang":lange,"pupdate":pupdate}
    #---
    for lane, tab in table.items() :
        for tt in tab :
            tabe    = tab[tt]
            mdtitle = tabe['mdtitle']
            lang    = tabe['lang']
            target  = tabe['target']
            user    = tabe['user']
            pupdate = tabe['pupdate']
            namespace      = tabe['namespace']
            #---
            cat     = cat_for_pages.get(mdtitle, '')
            #---
            mdtit   = py_tools.make_cod(mdtitle)
            user2   = py_tools.make_cod(user)
            tar     = py_tools.make_cod(target)
            word    = 0
            #---
            if str(namespace) != '0': continue
            #---
            tata = to_update_lang_user_mdtitle.get(lang, {}).get(user, [])
            #---
            uuu = '';
            #---
            update_qua = f'''
    UPDATE pages SET target = {tar}, pupdate = "{pupdate}" WHERE user = {user2} AND title = {mdtit} AND lang = "{lang}";''';
            #---
            insert_qua = f'''
    INSERT INTO pages (title, word, translate_type, cat, lang, date, user, pupdate, target)
    SELECT {mdtit}, '{word}', 'lead', '{cat}', '{lang}', '', {user2}, '{pupdate}', {tar}
    WHERE NOT EXISTS (SELECT 1 FROM pages WHERE title = {mdtit} AND lang = '{lang}' AND user = {user2} );''';
            #---
            pywikibot.output('______ \\/\\/\\/ _______')
            # find if to update or to insert
            if mdtitle in tata:
                pywikibot.output(f'to update: title:{mdtitle}, user:{user} ')
                uuu = update_qua
            else:
                pywikibot.output(f'to insert: title:{mdtitle}, user:{user} ')
                uuu = insert_qua
            #---
            pywikibot.output(uuu)
            #---
            qu = sql_for_mdwiki.mdwiki_sql(uuu, update = True, Prints = False)
            #---
            pywikibot.output(qu)
#---
tit_user_lang = {}
#---
def dodo_sql():
    #---
    lang_o = ''
    #---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        if arg == 'lang' or arg == '-lang':
            lang_o = value
            Langs_to_title_and_user[value] = {}
        #---
        if arg == 'printsql':
            printsql[1] = True
    #---
    que = 'select title, user, lang, target from pages '
    #---
    if lang_o != '' : que += ' where lang = "%s"' % lang_o
    #---
    que += ' ;'
    #---
    pywikibot.output( que )
    #---
    sq = sql_for_mdwiki.mdwiki_sql(que)
    #---
    len_no_target = 0
    len_done_target = 0
    #---
    for tab in sq :
        mdtitle = py_tools.Decode_bytes(tab[0]) 
        user    = py_tools.Decode_bytes(tab[1])
        #---
        target  = py_tools.Decode_bytes(tab[3])
        #---
        lang  = py_tools.Decode_bytes(tab[2]).lower()
        #---
        if lang_o != '' and lang != lang_o.strip() : continue
        #---
        tul = mdtitle + user + lang
        tit_user_lang[tul] = target
        #---
        if not lang in Lang_usr_mdtitle       : Lang_usr_mdtitle[lang] = {}
        if not user in Lang_usr_mdtitle[lang] : Lang_usr_mdtitle[lang][user] = []
        #---
        Lang_usr_mdtitle[lang][user].append(mdtitle)
        #---
        if not lang in Langs_to_title_and_user      : Langs_to_title_and_user[lang] = {}
        if not lang in to_update_lang_user_mdtitle  : to_update_lang_user_mdtitle[lang] = {}
        #---
        if not user in to_update_lang_user_mdtitle[lang]  : to_update_lang_user_mdtitle[lang][user] = []
        #---
        if target == "":
            len_no_target += 1
            #---
            Langs_to_title_and_user[lang][mdtitle] = user
            #---
            to_update_lang_user_mdtitle[lang][user].append(mdtitle)
            #---
        else:
            #---
            if not lang in targets_done : targets_done[lang] = {}
            #---
            target  = target.replace("_" , " ")
            target2 = py_tools.ec_de_code(target, 'encode')
            #---
            lineout = 'done. <<lightgreen>> target:%s for mdtit:%s, user:%s'
            laloly = lineout % ( target.ljust(40), mdtitle.ljust(30), user)
            #---
            # pywikibot.output(laloly)
            #---
            len_done_target += 1
            #---
            # targets_done[lang][mdtitle] = { "user" : user , "target" : target }
            # targets_done[lang][mdtitle] = { "user" : user , "target" : target }
            #targets_done[lang][py_tools.ec_de_code(target , 'encode')] = { "user" : user , "target" : target }
            #---
            targets_done[lang][target] = { "user" : user , "target" : target }
            targets_done[lang][target2] = { "user" : user , "target" : target }
    #---
    pywikibot.output( '<<lightyellow>> find %d with target, and %s without in mdwiki database. ' % ( len_done_target , len_no_target ) )
    #---
    if 'print' in sys.argv: pywikibot.output(Langs_to_title_and_user)
    #---
    tttime.sleep(3)
#---
query_main_old = '''#use arwiki_p;
select DISTINCT p.page_title, c.comment_text , a.actor_name , r.rev_timestamp
from change_tag t
INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
INNER JOIN revision r on r.rev_id = t.ct_rev_id
INNER JOIN actor a ON r.rev_actor = a.actor_id
inner join comment c on c.comment_id = r.rev_comment_id
INNER JOIN page p on r.rev_page=p.page_id
where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
and r.rev_parent_id = 0
#AND a.actor_name in ('Mr. Ibrahem')
AND r.rev_timestamp > 20210101000000
#and comment_text like "%[[:en:Special:Redirect/revision/%|User:Mr. Ibrahem/%]]%"
and comment_text like "%User:Mr. Ibrahem/%"
and p.page_namespace = 0
#limit 10
'''
#---
query_main = '''#use arwiki_p;
select DISTINCT p.page_title, c.comment_text, a.actor_name, r.rev_timestamp, p.page_namespace
from change_tag t
INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
INNER JOIN revision r on r.rev_id = t.ct_rev_id
INNER JOIN actor a ON r.rev_actor = a.actor_id
inner join comment c on c.comment_id = r.rev_comment_id
INNER JOIN page p on r.rev_page=p.page_id
where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
and r.rev_parent_id = 0
AND r.rev_timestamp > 20210101000000
and comment_text like "%User:Mr. Ibrahem/%"
#and p.page_namespace = 0
'''
#---
def main():
    #---
    # pywikibot.output( '<<lightred>> sql . MySQLdb_finder: ' )
    #---
    dodo_sql()
    #---
    New_Table_by_lang = {}
    #---
    Skip_titles_global = ['جامعة نورث كارولاينا','جامعة ولاية كارولينا الشمالية إيه آند تي','نيشان راجاميترابورن']
    #---
    Skip_titles = {}
    Skip_titles['Mr. Ibrahem'] = { 'targets' : ['جامعة نورث كارولاينا','جامعة ولاية كارولينا الشمالية إيه آند تي','نيشان راجاميترابورن'] , 'mdtitles' : [] }
    Skip_titles['Avicenno'] =  { 'targets' : ['ألم فرجي','لقاح المكورة السحائية'], 'mdtitles' : [] }
    #---
    Skip_titles['Subas Chandra Rout'] =  { 'targets' : [], 'mdtitles' : ["Wilms' tumor" , "Sheehan's syndrome", "Membranous nephropathy"] }
    #---
    n = 0
    #---
    sskip = [ 'zh-yue' , 'ceb' ]
    #---
    numb_lang = 0
    lnn = len(Langs_to_title_and_user.keys())
    #---
    # for lange,lal in Langs_to_title_and_user.items():
    for lange in Langs_to_title_and_user:
        #---
        New_Table_by_lang[lange] = {}
        #---
        numb_lang += 1
        #---
        pywikibot.output( ' \\/\\/\\/\\/\\/ ')
        pywikibot.output( 'mdwiki/mdpy/sql.py: %d Lang from %s : "%s"' % (numb_lang, lnn, lange) )
        #---
        result = {}
        #---
        qua = query_main
        #---
        if lange == 'ar' : qua += "\n and p.page_title not in ('جامعة_نورث_كارولاينا','جامعة_ولاية_كارولينا_الشمالية_إيه_آند_تي','نيشان_راجاميترابورن')"
        #---
        qua += '\n;'
        #---
        if lange in sskip :
            pywikibot.output( 'skip lang:%s' % lange)
        else:
            if 'printquery' in sys.argv: print(qua)
            result = wiki_sql.Make_sql_many_rows( qua, wiki = str(lange))
        #---
        if result != {}:
            pywikibot.output( 'sql.py len(result) = "{}"'.format( len( result ) ) )
            #---
            texddt = '\n'
            #--- 
            for list in result:
                #---
                #pywikibot.output( list )
                target   = py_tools.Decode_bytes(list[0]) 
                co_text  = py_tools.Decode_bytes(list[1])
                user     = py_tools.Decode_bytes(list[2])
                pupdate  = py_tools.Decode_bytes(list[3])
                namespace= py_tools.Decode_bytes(list[4])
                #---
                namespace = str(namespace)
                #---
                pupdate  = pupdate[:8]
                pupdate  = re.sub('^(\d\d\d\d)(\d\d)(\d\d)$' , '\g<1>-\g<2>-\g<3>' , pupdate )
                #---
                md_title = co_text.split('User:Mr. Ibrahem/')[1].split(']]')[0].replace("_" , " ")#.replace("'" , "\'")
                #---
                target = target.replace("_" , " ")#.replace("'" , "\'")
                #---
                user = user.replace("_" , " ")#.replace("'" , "\'")
                #---
                if target in Skip_titles_global: continue
                if target in Skip_titles.get(user,{}).get('targets',[]): continue
                #---
                if md_title in Skip_titles.get(user,{}).get('mdtitles',[]): continue
                #---
                Taba2 = {
                    "mdtitle": md_title , 
                    "target": target, 
                    "user":user, 
                    "lang":lange, 
                    "pupdate":pupdate, 
                    "namespace":namespace
                }
                #---
                lineout = '<<lightyellow>> target:%s:%s, ns:%s for mdtit:<<lightyellow>>%s, user:<<lightyellow>>%s'
                laloly = lineout % ( lange, target.ljust(40), namespace.ljust(3), md_title.ljust(30), user)
                #---
                tgd = targets_done.get(lange,{})
                #---
                target2 = py_tools.ec_de_code(target, 'encode')
                #---
                tul = md_title + user + lange
                tul_target = tit_user_lang.get(tul, '')
                #---
                cattest = cat_for_pages.get(md_title, '')
                #---
                if namespace != '0' :
                    if 'ns' in sys.argv and tul_target == '' and cattest:
                        pywikibot.output( laloly )
                    continue
                #---
                # للتأكد من الصفحات غير المنشورة
                if not target2 in tgd and not target in tgd:
                    #---
                    if tul_target != '':
                        if tul_target == target:
                            pywikibot.output(f'target already in, {target}')
                        else:
                            pywikibot.output(f'puplished target: {tul_target} != target to add: {target}')
                    else:
                        New_Table_by_lang[lange][md_title] = Taba2
                        n += 1
                        pywikibot.output( laloly )
                #---
    #---
    add_to_wd.add_tab_to_wd(New_Table_by_lang)
    #---
    add_to_mdwiki_sql(New_Table_by_lang)
    #wpref.make_ref_change(New_Table_by_lang)# if newtext.find('[[Category:Translated from MDWiki') == -1 : newtext = newtext + '\n[[Category:Translated from MDWiki]]'
    #---
if __name__ == '__main__':
    main()
#---
