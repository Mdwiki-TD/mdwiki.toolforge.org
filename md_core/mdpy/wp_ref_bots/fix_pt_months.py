"""
from mdpy.bots.fix_pt_months import pt_months
"""
import re
import wikitextparser as wtp
#---
months = {
    'January': 'janeiro',
    'February': 'fevereiro',
    'March': 'março',
    'April': 'abril',
    'May': 'maio',
    'June': 'junho',
    'July': 'julho',
    'August': 'agosto',
    'September': 'setembro',
    'October': 'outubro',
    'November': 'novembro',
    'December': 'dezembro',
}
#---
months_lower = { k.lower(): v for k, v in months.items() }
#---
months_line = "|".join(months.keys())
#---
def printn(s):
    return
def pt_months_old(text):
    # translate months from english to Português
    # regex to find text like =19 September 2022 or =September 2022
    regexline = r'(?i)(?P<param>\|\s*\w+\s*\=\s*)(?P<d>\d{1,2} |)(?P<m>%s) (?P<y>\d{4})(?![^\|\}\s])' % months_line
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
        ref2 = ref
        #---
        maa = re.compile(regexline, flags=re.IGNORECASE).finditer(ref)
        for match in maa:
            old = match.group()
            param = match.group('param')
            d = match.group('d')
            m = match.group('m')
            y = match.group('y')
            #---
            pt_m = months_lower.get(m.lower(), '')
            #---
            if pt_m == '': continue
            #---
            if d != '': pt_m = f'de {pt_m}'
            #---
            oldval = f"{param}{d}{m} {y}"
            printn(f"oldval: {oldval}")
            # printn(f"old   : {old}")
            #---
            newval = f"{param}{d}{pt_m} de {y}"
            #---
            printn(f"newval: {newval}")
            ref2 = ref2.replace(oldval, newval)
        #---
        if ref2 != ref:
            text = text.replace( pap + ref, pap + ref2 )
        #---
    #---
    return text
#---
def make_new_val(val):
    newval = val
    # match month and year
    #---
    maa = r'^(?P<d>\d{1,2} |)(?P<m>%s) (?P<y>\d{4})$' % months_line
    # match date like : January 10, 2020 
    maa2 = r'^(?P<m>%s) (?P<d>\d{1,2}), (?P<y>\d{4})$' % months_line
    #---
    sas = re.search(maa, val.strip())
    if sas:
        d = sas.group('d')
        m = sas.group('m')
        y = sas.group('y')
        # ---
        pt_m = months_lower.get(m.lower(), '')
        #---
        if pt_m != '':
            #---
            if d != '': pt_m = f'de {pt_m}'
            #---
            newval = f"{d} {pt_m} {y}"
        #---
        return newval
    # ---
    sas2 = re.search(maa2, newval.strip())
    #---
    if sas2:
        d = sas2.group('d')
        m = sas2.group('m')
        y = sas2.group('y')
        # ---
        pt_m = months_lower.get(m.lower(), '')
        #---
        if pt_m != '': 
            #---
            if d != '': pt_m = f'de {pt_m}'
            #---
            newval = f"{d} {pt_m} {y}"
        #---
        return newval
    # ---
    return newval
#---
def pt_months(text):
    parsed = wtp.parse(text)
    tags   = parsed.get_tags()
    #---
    for x in tags:
        if x.name != 'ref': continue
        if not x.contents: continue
        #---
        old = x.contents
        #---
        parsed2 = wtp.parse(x.contents)
        #---
        for temp in parsed2.templates:
            for arg in temp.arguments:
                na  = arg.name
                val = arg.value.strip()
                #---
                new_val = make_new_val(val)
                if new_val:
                    # arg.value = new_val
                    temp.set_arg(na, new_val)
                #--
        #---
        _new = parsed2.string
        #---
        x.contents = _new
        #---
    #---
    text = parsed.string
    #---
    return text
#---
# python pwb.py mdpy/bots/fix_pt_months
#---
def testee():
    text = """Boala se agravează în timp și este de obicei diagnosticată atunci când declinul cognitiv interferează cu funcționarea zilnică normală.<ref name="McKeithConsensus2017">{{Citat revistă
|dată=July 2017
|titlu=Diagnosis and management of dementia with Lewy bodies: Fourth consensus report of the DLB Consortium
|journal=Neurology
|volum=89
|număr=1
|pagini=88–100
|pmid=28592453
|pmc=5496518
|doi=10.1212/WNL.0000000000004058}}</ref><ref name="NINDS2020Book">{{Citat web
|url= https://www.ninds.nih.gov/Disorders/Patient-Caregiver-Education/Hope-Through-Research/Lewy-Body-Dementia-Hope-Through-Research 
|publisher= US National Institutes of Health 

|accessdate= 12 March 2020 
|date= January 10, 2020 
|archivedate=April 30, 2021

|titlu=Lewy body dementia: Hope through research
|lucrare=National Institute of Neurological Disorders and Stroke
|archiveurl=https://web.archive.org/web/20210430175606/https://www.ninds.nih.gov/Disorders/Patient-Caregiver-Education/Hope-Through-Research/Lewy-Body-Dementia-Hope-Through-Research}}</ref>"""
    #---
    newtext = text
    #---
    printn = print
    #---
    import pywikibot
    #---
    newtext = new(newtext)
    pywikibot.showDiff( text, newtext )
#---
if __name__ == "__main__":
    testee()
#---
