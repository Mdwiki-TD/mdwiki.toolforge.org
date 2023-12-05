'''
python3 core8/pwb.py mdpy/fixref/fixreftest
'''
import pywikibot
from mdpy.fixref.fixref_text_new import fix_ref_template

# ---
text = """
    <!-- Definition and symptoms -->
    '''Hypoprolactinemia''' is a [[medical condition]] characterized by a lack of [[prolactin]], a [[hypothalamic-pituitary hormone]].<ref name=Tri2019>{{cite book |last1=Tritos |first1=Nicholas A. |last2=Klibanski |first2=Anne |title=Prolactin Disorders: From Basic Science to Clinical Management |date=2019 |publisher=Springer |isbn=978-3-030-11836-5 |page=104 |url=https://books.google.ca/books?id=J6SWDwAAQBAJ&pg=PA104 |language=en}}</ref> Symptoms include the inability to produce milk after [[childbirth]].<ref name=Yen2013/> Usually it occurs together with [[hypopituitarism]].<ref name=Yen2013/> Other complications may include [[infertility]] and [[sexual dysfunction]].<ref name=Tri2019/>

    <!-- Cause and diagnosis -->
    Causes include [[Sheehan's syndrome|Sheehan syndrome]], [[pituitary surgery]], [[traumatic brain injury]], and certain [[genetic mutations]].<ref name=Yen2013>{{cite book
    |author1=Jerome F. Strauss III|author2=Robert L. Barbieri|title=Yen & Jaffe's Reproductive Endocrinology: Physiology, Pathophysiology, and Clinical Management
    |url=https://books.google.com/books?id=TTCwAAAAQBAJ&pg=PA53|date=28 August 2013|publisher=Elsevier Health Sciences|isbn=978-1-4557-5972-9|pages=53–}}</ref><ref name=Bond2005>{{cite journal |last1=Bondanelli |first1=M
    |last2=Ambrosio
    |first2=MR |last3=Zatelli
    |first3=MC |last4=De Marinis |first4=L |last5=degli Uberti |first5=EC
    |title=Hypopituitarism after traumatic brain injury. |journal=European journal of endocrinology |date=May 2005 |volume=152 |issue=5 |pages=679-91 |doi=10.1530/eje.1.01895 |pmid=15879352}}</ref><ref name=Tri2019/> Diagnosis is by blood tests for prolactin, after being given [[thyrotropin]].<ref name=Mer2021>{{cite web |title=Hypopituitarism - Hormonal and Metabolic Disorders |url=https://www.merckmanuals.com/home/hormonal-and-metabolic-disorders/pituitary-gland-disorders/hypopituitarism |website=Merck Manuals Consumer Version |accessdate=2 February 2021}}</ref><ref name=Emed2021Diag>{{cite web |title=Prolactin Deficiency Workup |url=https://emedicine.medscape.com/article/124526-workup |website=Emedicine |accessdate=2 February 2021}}</ref> Confirming the diagnosis; however, is not necessarily required as there is no specific treatment.<ref name=Emed2021Diag/>

    <!-- Treatment and epidemiology -->
    While some evidence supports the use of [[prolactin|recombinant human prolactin]], it is not currently approved for medical use.<ref name=Tri2019/><ref>{{cite web |title=Prolactin Deficiency Medication: Antidopaminergic agents |url=https://emedicine.medscape.com/article/124526-medication |website=emedicine.medscape.com |accessdate=2 February 2021}}</ref> Treatment generally involves [[formula feeding]] the baby.<ref name=Emed2021Tx>{{cite web |title=Prolactin Deficiency Treatment & Management: Medical Care, Consultations |url=https://emedicine.medscape.com/article/124526-treatment |accessdate=2 February 2021 |date=9 November 2019}}</ref> Prolactin deficiency alone is rare.<ref name=Tri2019/> It occurs in about 17% of cases of hypopituitarism or about 8 per 100,000 people in Spain as of 1999.<ref name=Tri2019/>

    ==Signs and symptoms==
    Hypoprolactinemia is associated with [[ovarian dysfunction]] in women,<ref name="Kauppila 1988" /><ref name="Schwarzler 1997" /> and, in men, [[metabolic syndrome]],<ref name="CoronaMannucci2009">{{cite journal|last1=Corona|first1=Giovanni|last2=Mannucci|first2=Edoardo|last3=Jannini|first3=Emmanuele A|last4=Lotti|first4=Francesco|last5=Ricca|first5=Valdo|last6=Monami|first6=Matteo|last7=Boddi|first7=Valentina|last8=Bandini|first8=Elisa|last9=Balercia|first9=Giancarlo|last10=Forti|first10=Gianni|last11=Maggi|first11=Mario|title=Hypoprolactinemia: A New Clinical Syndrome in Patients with Sexual Dysfunction|journal=Journal of Sexual Medicine|volume=6|issue=5|year=2009|pages=1457–1466|issn=1743-6095|doi=10.1111/j.1743-6109.2008.01206.x|pmid=19210705}}</ref> [[anxiety]],<ref name="CoronaMannucci2009" /> [[arteriogenic]] [[erectile dysfunction]],<ref>{{cite book|title=Pituitary Hormones—Advances in Research and Application: 2013 Edition|url=https://books.google.com/books?id=olcbPlHdK0EC&pg=PA62|date=21 June 2013|publisher=ScholarlyEditions|isbn=978-1-4816-7922-0|pages=62–}}</ref> [[premature ejaculation]],<ref name="Corona 2009" /> [[oligozoospermia|low concentration of sperm]], [[asthenospermia|reduced sperm motility]], hypofunction of [[seminal vesicles]], and [[hypoandrogenism]].<ref name="Gonzales 1989" /> In one study, normal sperm characteristics were restored when prolactin levels were brought up to normal values in men with hypoprolactinemia.<ref name="Ufearo 1995" />

    Hypoprolactinemia can be a cause of [[lactation failure]] after childbirth.<ref name=Yen2013 /><ref name="pmid16597813">{{cite journal | vauthors = Prabhakar VK, Shalet SM | title = Aetiology, diagnosis, and management of hypopituitarism in adult life | journal = Postgrad Med J | volume = 82 | issue = 966 | pages = 259–66 | year = 2006 | pmid = 16597813 | pmc = 2585697 | doi = 10.1136/pgmj.2005.039768 | url = }}</ref><ref name="DonsJr.2009">{{cite book|author1=Robert F. Dons|author2=Frank H. Wians, Jr.|title=Endocrine and Metabolic Disorders: Clinical Lab Testing Manual, Fourth Edition|url=https://books.google.com/books?id=rS41IwpI-hIC&pg=PA103|date=17 June 2009|publisher=CRC Press|isbn=978-1-4200-7936-4|pages=103–}}</ref>

    ==Causes==
    Hypoprolactinemia can result from [[autoimmune disease]],<ref name="PhD2010" /> [[hypopituitarism]],<ref name=Yen2013 /> [[growth hormone deficiency]],<ref name="PhD2010" /> [[hypothyroidism]],<ref name="PhD2010">{{cite book|author=Andrew S. Davis|title=Handbook of Pediatric Neuropsychology|url=https://books.google.com/books?id=SU9-LSh4HgcC&pg=PT1134|date=25 October 2010|publisher=Springer Publishing Company|isbn=978-0-8261-5737-9|pages=1134–}}</ref> excessive [[dopamine]] action in the [[tuberoinfundibular pathway]] and/or the [[anterior pituitary]], and ingestion of drugs that activate the [[D2 receptor|D<sub>2</sub> receptor]], such as direct D<sub>2</sub> receptor [[agonist]]s like [[bromocriptine]] and [[pergolide]], and indirect D<sub>2</sub> receptor activators like [[substituted amphetamine|amphetamine]]s (through the induction of [[dopamine releasing agent|dopamine release]]).<ref name="Stone1996">{{cite book|author=Trevor W. Stone|title=CNS Neurotransmitters and Neuromodulators|url=https://books.google.com/books?id=ObG24oxrivEC&pg=PA214|date=9 May 1996|publisher=CRC Press|isbn=978-0-8493-7632-0|pages=214–}}</ref>

    ==Diagnosis==
    Guidelines for diagnosing hypoprolactinemia are defined as prolactin levels below 3&nbsp;µg/L in women,<ref name="Kauppila 1988">{{cite journal |vauthors=Kauppila A, Martikainen H, Puistola U, Reinilä M, Rönnberg L | title = Hypoprolactinemia and ovarian function | journal = Fertil. Steril. |date=Mar 1988 | volume = 49 | issue = 3 | pages = 437–41 | pmid = 3342895 | doi=10.1016/s0015-0282(16)59769-6}}</ref><ref name="Schwarzler 1997">{{cite journal |vauthors=Schwärzler P, Untergasser G, Hermann M, Dirnhofer S, Abendstein B, Berger P | title = Prolactin gene expression and prolactin protein in premenopausal and postmenopausal human ovaries | journal = Fertil. Steril. |date=Oct 1997 | volume = 68 | issue = 4 | pages = 696–701 | pmid = 9341613 | doi = 10.1016/S0015-0282(97)00320-8 }}</ref> and 5&nbsp;µg/L in men.<ref name="Corona 2009">{{cite journal |vauthors=Corona G, Mannucci E, Jannini EA, Lotti F, Ricca V, Monami M, Boddi V, Bandini E, Balercia G, Forti G, Maggi M | title = Hypoprolactinemia: a new clinical syndrome in patients with sexual dysfunction | journal = J. Sex. Med. | volume = 6 | issue = 5 | pages = 1457–66 |date=May 2009 | pmid = 19210705 | doi = 10.1111/j.1743-6109.2008.01206.x }}</ref><ref name="Gonzales 1989">{{cite journal |vauthors=Gonzales GF, Velasquez G, Garcia-Hjarles M | title = Hypoprolactinemia as related to seminal quality and serum testosterone | journal = Arch. Androl. | volume = 23 | issue = 3 | pages = 259–65 | year = 1989 | pmid = 2619414 | doi = 10.3109/01485018908986849 }}</ref><ref name="Ufearo 1995">{{cite journal |vauthors=Ufearo CS, Orisakwe OE | title = Restoration of normal sperm characteristics in hypoprolactinemic infertile men treated with metoclopramide and exogenous human prolactin | journal = Clin Pharmacol Ther | volume = 58 | issue = 3 | pages = 354–9 |date=September 1995 | pmid = 7554710 | doi = 10.1016/0009-9236(95)90253-8 }}</ref>

    ==Management==
    There are few treatments which increase prolactin levels in humans. Treatment differs based on the reason for diagnosis. Women who are diagnosed with hypoprolactinemia following [[lactation failure]] are typically advised to formula feed, although treatment with [[metoclopramide]] has been shown to increase milk supply in clinical studies. For [[Infertility|subfertility]], treatment may include [[Clomifene|clomiphene citrate]] or [[gonadotropin]]s.<ref>{{Cite web|url=https://emedicine.medscape.com/article/124526-medication|title=Prolactin Deficiency Medication: Antidopaminergic agents|website=emedicine.medscape.com|language=en|access-date=2017-11-25}}</ref>

    ==See also==
    * [[Hypothalamic–pituitary–prolactin axis]]
    * [[Hyperprolactinaemia|Hyperprolactinemia]]

    ==References==
    {{Reflist}}

    == External links ==
    {{Medical resources
    |  DiseasesDB      =
    |  ICD10           =
    |  ICD9            =
    |  ICDO            =
    |  OMIM            =
    |  MedlinePlus     =
    |  eMedicineSubj   =
    |  eMedicineTopic  =
    |  MeshID          =
    }}
    {{Endocrine pathology}}

    [[Category:Pituitary disorders]]
    [[Category:RTT]]"""
# ---
text = '''
<ref>{{cite journal
| vauthors = Grant JE, Kim SW, Odlaug BL
| url =  https://pubmed.ncbi.nlm.nih.gov/19217077/
| lay-date = 3 April 2009
| lay-url = https://www.sciencedaily.com/releases/2009/04/090401101900.htm
| lay-source = Science Daily
}}</ref>
'''


def test():
    newtext = fix_ref_template(text)
    pywikibot.showDiff(text, newtext)


# ---
if __name__ == "__main__":
    test()
# ---
