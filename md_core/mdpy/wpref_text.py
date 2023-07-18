#!/usr/bin/python

"""
from wpref_text import fix_page
# fix_page(text, title)
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import os
import sys
sys.dont_write_bytecode = True
#---
if 'returnfile' in sys.argv:
    from bots.Duplicatenew2 import DuplicateReferences
    from bots import txtlib2
    from wp_ref_bots.fix_pt_months import pt_months
else:
    from mdpy.bots.Duplicatenew2 import DuplicateReferences
    from mdpy.bots import txtlib2
    from mdpy.wp_ref_bots.fix_pt_months import pt_months
#---
printa = { 1 : False}
#---
def printn(s):
    if printa[1] or 'returnfile' not in sys.argv:
        print(s)
#---
def add_lang_en(text, lang=''):
    #---
    printn('add_lang_en:')
    #---
    # Match references
    REFS = re.compile( r'(?is)(?P<pap><ref[^>\/]*>)(?P<ref>.*?<\/ref>)')
    #---
    for Match in REFS.finditer(text):
        pap = Match.group('pap')
        ref = Match.group('ref')
        #---
        if not ref.strip(): continue
        #---
        if re.sub(r'\|\s*language\s*\=\s*\w+', '', ref) != ref : continue
        #---
        ref2 = re.sub(r'(\|\s*language\s*\=\s*)(\|\}\})', '\g<1>en\g<2>', ref)
        #---
        if ref2 == ref:
            ref2 = ref.replace('}}</ref>', '|language=en}}</ref>')
        #---
        if ref2 != ref:
            text = text.replace( pap + ref, pap + ref2 )
    #---
    return text
#---
def remove_False_code(text):
    #---
    if 'newcite' not in sys.argv:
        return text
    #---
    # }}<cite class="citation journal cs1" data-ve-ignore="true" id="CITEREFSmithLopezSilberman2020">Smith, N; Lopez, RA; Silberman, M (January 2020). "Distributive Shock". [[PMID (identifier)|PMID]]&nbsp;[//pubmed.ncbi.nlm.nih.gov/29261964 29261964].</cite><span data-ve-ignore="true"> </span><span class="cs1-hidden-error citation-comment" data-ve-ignore="true"><code class="cs1-code"><nowiki>{{</nowiki>[[Template:cite journal|cite journal]]<nowiki>}}</nowiki></code>: </span><span class="cs1-hidden-error citation-comment" data-ve-ignore="true">Cite journal requires <code class="cs1-code">&#124;journal=</code> ([[Help:CS1 errors#missing_periodical|help]])</span></ref>
    #---
    # Match references
    REFS = re.compile( r'(?is)(?P<pap><ref[^>\/]*>)(?P<ref>.*?<\/ref>)')
    #---
    for Match in REFS.finditer(text):
        pap = Match.group('pap')
        ref = Match.group('ref')
        if not ref.strip():
            #pywikibot.output( "\tno ref" )
            continue
        #---
        # find html code like <cite></cite> and all span code after it
        # find and get html code like <cite></cite>
        if not re.search( r'(?is)<cite[^>]*>', ref ):
            #pywikibot.output( "\tno cite" )
            continue
        #---
        # find and get html code like <cite></cite>
        ref2 = ref
        if ref.find('<span ') != -1:
            ref2 = re.sub( r'(\s*<span[^>]*>.*?<\/span>+?)</ref>','</ref>', ref2 )
        ref2 = re.sub( r'<cite[^>]*>.*?<\/cite>','', ref2 )
        #---
        if ref2 != ref and ref2.strip() != '</ref>':
            text = text.replace( pap + ref, pap + ref2 )
    #---
    return text
#---
def move_dots_text(newtext, lang=''):
    #---
    dot = '(\.|\,)'
    #---
    if lang == 'zh':    dot = '(。)'
    #---
    regline = r'((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)'
    #---
    newtext = re.sub(dot + r'\s*' + regline, '\g<2>\g<1>', newtext)
    #---
    return newtext
#---
def Expend_Infobox(text, title, section_0):
    #---
    newtext = text
    #---
    if section_0 == '':
        if newtext.find('==') != -1:
            section_0 = newtext.split('==')[0]
        else:
            tagg = "'''%s'''1" % title
            if newtext.find(tagg) != -1:
                section_0 = newtext.split(tagg)[0]
            else:
                section_0 = newtext
                printn('section_0 = newtext')
    #---
    title2 = re.escape(title)
    #---
    newtext   = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, "}\n\n\g<1>", newtext)
    section_0 = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, "}\n\n\g<1>", section_0)
    #---
    tempse_by_u = {}
    tempse = {}
    #---
    ingr = txtlib2.extract_templates_and_params(section_0)
    u = 0
    for temp in ingr: 
        u += 1
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        if len(params) > 4  and section_0.find( f'>{template}' ) == -1:
            tempse_by_u[u] = temp
            #---
            tempse[u] = len(template)
            #---
            printn(namestrip)
    #---
    main_temp = {}
    #---
    if len(tempse_by_u) == 1 :
        for x in tempse_by_u:
            main_temp = tempse_by_u[x]
    else:
        PP = [ [y1, u1] for u1, y1 in tempse.items() ]
        PP.sort( reverse = True )
        #---
        for y2, u2 in PP:
            printn(f'len: {y2}, u2: {u2}')
            main_temp = tempse_by_u[u2]
            break
    #---
    # work in main_temp:
    if main_temp != {}:
        main_temp_text = main_temp.get('item', '')
        #---
        new_temp = main_temp_text
        #---
        for param in main_temp['params']:
            # new_temp = re.sub(r'\s*(\|\s*%s\s*\=)' % param, '\n\g<1>', new_temp)
            newparam = '| %s=' % param.ljust(16)
            new_temp = re.sub(r'\s*(\|\s*%s\s*\=)' % param, '\n' + newparam, new_temp)
        #---
        new_temp = re.sub(r'\s*\}\}\s*$', '\n}}', new_temp)
        #---
        newtext = newtext.replace(main_temp_text, new_temp)
        newtext = newtext.replace(new_temp + "'''", new_temp + "\n'''")
    #---
    return newtext
#---
def fix_page(newtext, title, move_dots= False, infobox = False, section_0 ='', lang='', add_en_lang=False):
    #---
    printn(f'fix page: {title}, move_dots:{move_dots}, expend_infobox:{infobox}')
    #---
    if infobox:
        newtext = Expend_Infobox(newtext, title, section_0)
    #---
    newtext = remove_False_code(newtext)
    #---
    newtext = DuplicateReferences(newtext)
    #---
    if move_dots: newtext = move_dots_text(newtext, lang=lang)
    #---
    if add_en_lang: newtext = add_lang_en(newtext, lang=lang)
    if lang == 'pt': newtext = pt_months(newtext)
    #---
    return newtext
#---
# python pwb.py mdpy/wpref_text
#---
def testee():
    printa[1] = True
    text = """{{Infocaseta Tratament medical|Name=Demența cu corpi Lewy|Image=Lewy body in the substantia nigra from a person with Parkinson's disease.jpg|caption=[[Microfotografie|Imagine microscopică]] a unui [[corp Lewy]] (săgeată) într-un neuron al [[substanței negre]]; bară de scalare=20 microni (0,02 mm)|field=[[Neurologie]], [[psihiatrie]]|complications=|prevention=|treatment=|medication=[[Inhibitori ai acetilcolinesterazei]] precum [[donepezil]] și [[rivastigmină]];<ref name=Taylor2020Cognitive> Taylor JP ''et al.'' (2020), sec. "Cognitive impairment".</ref> [[melatonină]]<ref name=Taylor2020Sleep> Taylor JP ''et al.'' (2020), sec. "Sleep disturbances" ("Nocturnal sleep disturbances" and "Excessive Daytime Sleepiness" combined on final publication).</ref>|frequency=Aproximativ 0,4% din persoanele cu vârste de peste 65 de ani<ref name= Levin201662> Levin J ''et al.'' (2016), p. 62.</ref>|deaths=}}'''Demența cu corpi Lewy''' ('''DLB''') este un tip de [[demență]] însoțit de modificări ale somnului, comportamentului, [[Cogniție|gândirii]], mișcării și [[Sistem nervos vegetativ|funcțiilor involuntare ale organismului]].<ref name="Taylor2020">{{Citat revistă|dată=February 2020|titlu=New evidence on the management of Lewy body dementia|journal=Lancet Neurol|volum=19|număr=2|pagini=157–69|pmid=31519472|pmc=7017451|doi=10.1016/S1474-4422(19)30153-X}}</ref> Pierderea memoriei nu este întotdeauna un simptom incipient.<ref name="Tousi2017">{{Citat revistă|dată=October 2017|titlu=Diagnosis and management of cognitive and behavioral changes in dementia with Lewy bodies|journal=Curr Treat Options Neurol|volum=19|număr=11|pagină=42|pmid=28990131|doi=10.1007/s11940-017-0478-x}}</ref> Boala se agravează în timp și este de obicei diagnosticată atunci când declinul cognitiv interferează cu funcționarea zilnică normală.<ref name="McKeithConsensus2017">{{Citat revistă|dată=July 2017|titlu=Diagnosis and management of dementia with Lewy bodies: Fourth consensus report of the DLB Consortium|journal=Neurology|volum=89|număr=1|pagini=88–100|pmid=28592453|pmc=5496518|doi=10.1212/WNL.0000000000004058}}</ref><ref name="NINDS2020Book">{{Citat web|url= https://www.ninds.nih.gov/Disorders/Patient-Caregiver-Education/Hope-Through-Research/Lewy-Body-Dementia-Hope-Through-Research |publisher= US National Institutes of Health |accessdate= March 18, 2020 |date= January 10, 2020 |titlu=Lewy body dementia: Hope through research|lucrare=National Institute of Neurological Disorders and Stroke|archivedate=April 30, 2021|archiveurl=https://web.archive.org/web/20210430175606/https://www.ninds.nih.gov/Disorders/Patient-Caregiver-Education/Hope-Through-Research/Lewy-Body-Dementia-Hope-Through-Research}}</ref> Funcția [[Miocard|inimii]] și fiecare nivel al funcției gastrointestinale, de la mestecat până la [[defecație]], pot fi afectate, [[Constipație|constipația]] fiind unul dintre cele mai des întâlnite simptome.<ref name="Taylor2020" /><ref name="Palma2018">{{Citat revistă|dată=March 2018|titlu=Treatment of autonomic dysfunction in Parkinson disease and other synucleinopathies|journal=Mov Disord|volum=33|număr=3|pagini=372–90|pmid=29508455|pmc=5844369|doi=10.1002/mds.27344}}</ref> De asemenea, se poate manifesta hipotensiunea ortostatică.<ref name="Taylor2020" /> Boala poate afecta comportamentul; schimbările de dispoziție precum [[Depresie (stare)|depresia]] și [[Apatie|apatia]] sunt frecvente.<ref name="McKeithConsensus2017" />"""
    #---
    newtext = text
    #---
    import pywikibot
    #---
    newtext = fix_page(newtext, 'Demența cu corpi Lewy', move_dots=False, infobox = True)
    pywikibot.showDiff( text, newtext )
#---
if __name__ == "__main__":
    testee()
#---
