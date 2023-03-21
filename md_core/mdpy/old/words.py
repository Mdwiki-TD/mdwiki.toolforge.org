#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

إنشاء قائمة بعدد الكلمات

python3 /data/project/mdwiki/core/pwb.py /data/project/mdwiki/TDpy/words newlist
python3 pwb.py /data/project/mdwiki/TDpy/words newpages 
python3 pwb.py /data/project/mdwiki/TDpy/words listnew

python3 pwb.py /data/project/mdwiki/TDpy/words more400

python3 pwb.py /data/project/mdwiki/TDpy/words less100

"""
#
# (C) Ibrahem Qasim, 2021
#
#
import os
import json
import codecs
import re
import string
import time
import sys
#------
sys_argv = sys.argv or []
#------
import catdepth2
#------
link_regex = re.compile(r'\[\[(.*?)\]\]')
#------
refreg = re.compile(r'(<ref[^>]*>[^<>]+</ref>|<ref[^>]*\/\s*>)')
#------
reg_links_with_allise = re.compile(r'(\[\[[^\]|[<>{}]*)\|(.*?)\]\]')
#------
reg_full_links = re.compile(r'(\[\[(?:[^][|]+)\|*(?:[^][]*(?:\[\[[^][]+\]\][^][]*)*)\]\])')
#------
reg_templates = re.compile(
    r'{{(?:msg:)?(?P<name>[^{\|]+?)'
    r'(?:\|(?P<params>[^{]+?(?:{[^{]+?}[^{]*?)?)?)?}}')
#------
#======
print_pywikibot = { 1 : False }
try:
    import pywikibot
    print_pywikibot[1] = True
except:
    print_pywikibot[1] = False
#======
#------
import mdapi
# mdapi.submitAPI( params )
#------
#======
def outbotnew( s ):
    if s == '' : return '' 
        #pywikibot.output( s )
    if print_pywikibot[1] :
        pywikibot.output( s )
    else:
        print( s )
#======
def get_vaild_links():
    vaild_links = []
    #------
    if 'newpages' in sys_argv:
        outbotnew('Get vaild_links from cat : RTT' )
        tabe = catdepth2.subcatquery2( 'RTT', depth = '3', ns = '0' )
        vaild_links = tabe['list']
    #------
    elif 'oldway' in sys_argv:
        ptext = mdapi.GetPageText( 'WikiProjectMed:List' )
        for m2 in link_regex.finditer(ptext):
            sa = re.compile('\[\[(\:|)(\w{2}|\w{3}|w|en|image|file|category|template)\:', flags = re.IGNORECASE )
            sal = sa.findall(m2.group(0))
            if not sal:
                itemu = m2.group(1).split('|')[0].strip()
                itemu = itemu[0].upper() + itemu[1:]
                vaild_links.append( itemu )
        #------
        outbotnew('Get vaild_links fromlist : WikiProjectMed:List (oldway)' )
        #------
    elif 'listnew' in sys_argv:
        outbotnew('Get vaild_links listnew' )
        ttt = '''Chlamydia
    Postpartum infections
    Mucormycosis
    Alpha-1 antitrypsin deficiency
    Arrhythmia
    Pyoderma gangrenosum
    Transient ischemic attack
    Subacute sclerosing panencephalitis
    Frontotemporal dementia
    Hyperhidrosis
    Giant cell arteritis
    Dicycloverine
    Pheochromocytoma
    Alcoholic liver disease
    Hand, foot, and mouth disease
    Vaginal yeast infection
    Dopamine
    Epispadias
    Colorectal cancer
    Thiamazole
    Chancroid
    Ewing sarcoma
    Attention deficit hyperactivity disorder
    Glibenclamide
    Norepinephrine
    Ehlers–Danlos syndromes
    Pit latrine
    Kidney stone disease
    Myopia
    Chlortalidone
    Valaciclovir
    Cleft lip and cleft palate
    Waardenburg syndrome
    Hepatitis E
    Hiatal hernia
    Clubfoot
    Folate
    Vasopressin
    Clostridioides difficile infection
    Hemolytic–uremic syndrome
    Cerebral venous sinus thrombosis
    Hantavirus hemorrhagic fever with renal syndrome
    Esophageal varices
    Opioid withdrawal
    Travelers' diarrhea
    Carotid artery stenosis
    Lymphogranuloma venereum'''
        vaild_links = [ x.strip() for x in ttt.split('\n') if x.strip() != '' ]
        #------
    elif 'fromlist' in sys_argv:
        vaild_links = mdapi.Get_page_links( 'WikiProjectMed:List' )
        outbotnew('Get vaild_links fromlist : WikiProjectMed:List' )
    else:
        outbotnew('Get vaild_links from cat : RTT' )
        tabe = catdepth2.subcatquery2( 'RTT', depth = '3', ns = '0' )
        vaild_links = tabe['list']
    #======
    for x in vaild_links:
        if x.startswith('Category:') :
            vaild_links.remove(x)
    #======
    outbotnew('len of vaild_links: %d' % len(vaild_links) )
    #======
    return vaild_links
#------
vaild_links = get_vaild_links()
#======
#------
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#------
if not os.path.isdir(project): project = '/mdwiki'
#------
#======
json_file = {}
json_file[0] = project + '/public_html/Translation_Dashboard/Tables/words.json'
#======
old_words = {}
lala = ''
#======
with codecs.open( json_file[0], "r", encoding="utf-8") as listt:
    lala = listt.read()
listt.close()
outbotnew( 'file_name:%s' % json_file[0] )
fa = str(lala)
if fa != '' : old_words = json.loads(fa)
#======
len_old = len(old_words)
#======
words = {}
#======
if not 'new' in sys_argv:
    for xa in old_words :
        if old_words[xa] > 0 : words[xa] = old_words[xa]
#======
if 'newpages' in sys_argv:#vaild_links
    vaild_links2 = vaild_links
    vaild_links = [ t for t in vaild_links2 if (not t in old_words or old_words[t] == 0) ]
    #------
    outbotnew( 'Category-members:%d, New-members:%d' % ( len(vaild_links2), len(vaild_links) ) )
    #------ 
#======
Nore = { 1 : False }
for arg in sys_argv:
    if arg in [ 'new', 'listnew', 'less100', 'more400' ] :
        Nore[1] = True
#====== 
def log():
    with open( json_file[0], 'w') as outfile:
        json.dump( words, outfile, sort_keys = True )
    outfile.close()
    #------
    outbotnew('<<lightgreen>> %d lines to %s' % ( len(words), json_file[0] ) )
    outbotnew('<<lightgreen>> len old words %d' % len_old )
#====== 
def get_lead( x, numb, lenth ):
    #------
    #if old_words.get(x) and not 'new' in sys_argv and not 'listnew' in sys_argv and not 'less100' in sys_argv and not 'more400' in sys_argv: 
    if old_words.get(x) and not Nore[1]: 
        outbotnew('page %d from %d, x:%s' % ( numb, lenth, x ) )
        outbotnew( "<<lightyellow>> page:%s already in old_words:%d" % (x, old_words.get(x, 0)) )
        return ''
    #------
    outbotnew('------------------' )
    outbotnew('page %d from %d, x:%s' % ( numb, lenth, x ) )
    #------
    if x.startswith('Category:') : return ''
    #------
    params = {"action": "parse", "format": "json", "page": x, "prop": "wikitext", "section": "0" }
    json1 = mdapi.submitAPI(params)
    #------
    text = ''
    #------
    if json1 : text = json1.get("parse", {}).get("wikitext", {}).get("*", '')
    #------
    # text = '[[file:dd.jpg|thumb|left|220px|2020 in [[yemen]] sanaa ]]\n' + text
    # text = '[[image:bhn.jpg|right|220px|2020 in [[yemen sanaa]] ]]\n' + text
    #------
    text = re.sub( "\[\[((?:Image|file):[^][|]+)\|([^][]*(\[\[[^][]+\]\][^][]*)*)\]\]", "", text, flags = re.IGNORECASE )
    text = re.sub( "\<\!\-\-.*?\-\-\>", "", text )
    #------
    text = text.replace("'''", "").replace("''", "")
    #------
    #text = text.replace("</ref>", "</ref>\n").replace(">{{cite", ">\n{{cite")
    #------
    text2 = text
    #------
    #outbotnew(text)
    #------
    for m in refreg.finditer(text):
        itemy = m.group()
        text = text.replace(itemy, '')
    #------    
    seen = set()
    #------    
    while reg_templates.search(text) is not None:
        for m in reg_templates.finditer(text):
            pa_item = m.group()
            #------
            if pa_item in seen: continue  # speed up
            seen.add(pa_item)
            #------
            text = text.replace(pa_item, '')
    #------    
    for hhh in reg_links_with_allise.finditer( text ):
        #------
        link = hhh.group()
        alli = hhh.group(2)
        #------
        text = text.replace( link, alli )
    #------
    text = re.sub( "\[\[(.*?)\]\]", "\g<1>", text, flags = re.IGNORECASE )
    text = re.sub( "\<\!\-\-.*?\-\-\>", "", text )
    text = re.sub( "\n+", " ", text )
    text = re.sub( "\s+", " ", text )
    text = re.sub( "\/", " ", text )
    #------
    if print_pywikibot[1] and 'test' in sys_argv : pywikibot.showDiff( text2, text )
    #------
    llen = len(text.split(' '))
    #------
    if old_words.get(x): 
        gg = old_words.get(x) - int(llen)
        if gg < 50 :
            outbotnew( "<<lightred>> new words:%d \t old_words:%d" % ( old_words.get(x, 0), llen ) )
        return ''
    #------
    words[x] = len(text.split(' '))
    #------
    outbotnew('len of %s words:%d, old_words:%s' % ( x, words[x], str(old_words.get(x, 0) ) ) )
    #------
    if numb == 10 or str(numb).endswith('00'):
        log()
#======
def check():
    #------
    word_list = old_words.keys()
    #------
    if 'new' in sys_argv:
        Listo = catdepth2.subcatquery( 'RTT', depth = '3', ns = '0' )
    else:
        Listo = catdepth2.subcatquery2( 'RTT', depth = '3', ns = '0' )
    #------
    Listo = Listo['list']
    #------
    number = 0
    #------
    for x in word_list:
        if not x in Listo:
            number += 1
            outbotnew('<<lightyellow>>a %d "%s"\t\tnot in catlist' % ( number, x ) )
    #------
    outbotnew('<<lightgreen>> len of word_list:%d, len of cat list:%d' % ( len(words), len(Listo) ) )
#======
def mmain():
    numb = 0
    #======
    if 'check' in sys_argv: return check()
    #======
    kkk = { 1 : vaild_links }
    #======
    if not 'new' in sys_argv:
        #kkk = [ x for x in vaild_links if not x in old_words ]
        kkk[1] = []
        for x in vaild_links :
            x2 = x[0].upper() + x[1:]
            #if not x in old_words or 'listnew' in sys_argv:
            kkk[1].append( x2 )
    #======
    if 'less100' in sys_argv:
        #kkk = [ x for x in vaild_links if not x in old_words ]
        kkk[1] = []
        for x in old_words :
            x2 = x[0].upper() + x[1:]
            if old_words[x] < 100 :
                kkk[1].append( x2 )
    #======
    if 'more400' in sys_argv:
        kkk[1] = []
        for x in old_words :
            x2 = x[0].upper() + x[1:]
            if old_words[x] > 400 :
                kkk[1].append( x2 )
    #======
    for x in kkk[1]:
        numb += 1
        #------
        get_lead(x, numb, len(kkk[1]))
        #------
    #======
    log()
#======
if __name__ == '__main__':
    mmain()
#======
