from wprefs.wpref_text import fix_page
import pywikibot

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
# ---
# ---
# ---
newtext = fix_page(text, 'Demența cu corpi Lewy', move_dots=False, infobox=True, lang='pt')
pywikibot.showDiff(text, newtext)

# python3 core8/pwb.py wprefs/bots/test_pt_months
