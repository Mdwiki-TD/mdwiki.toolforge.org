"""
python3 core8/pwb.py wprefs/bots/es_refs
"""
import wikitextparser as wtp
from wprefs.helps import print_s


def mv_es_refs(text):
    # ---
    refs = {}
    # ---
    numb = 0
    # ---
    parsed = wtp.parse(text)
    tags = parsed.get_tags()
    # ---
    for x in tags:
        # ---
        if not x or not x.name:
            continue
        if x.name != 'ref':
            continue
        if not x.contents:
            continue
        # ---
        attrs = x.attrs
        name = attrs.get('name', '').strip()
        group = attrs.get('group', '').strip()
        # ---
        if group not in refs:
            refs[group] = {}
        # ---
        if name == '':
            numb += 1
            name = f'autogen_{numb}'
            x.set_attr('name', name)
        # ---
        if name not in refs[group]:
            refs[group][name] = x.contents
        elif refs[group][name] != x.contents:
            print_s(f'x.contents = {x.contents}')
        # ---
        asas = f'<ref name="{name}" />'
        if group != '':
            asas = f'<ref group="{group}" name="{name}" />'
        # ---
        x.string = asas
    # ---
    line = '\n'
    # ---
    for g, gag in refs.items():
        for name, ref in gag.items():
            la = f'<ref name="{name}">{ref}</ref>\n'
            if g != '':
                la = f'<ref group="{g}" name="{name}">{ref}</ref>\n'
            # ---
            line += la
    # ---
    line = line.strip()
    # ---
    tempin = False
    # ---
    for template in parsed.templates:
        # ---
        template_name = str(template.normal_name()).strip()
        if template_name.lower() in ['reflist', 'listaref']:
            refs_arg = template.get_arg('refs')
            template.set_arg('refs', line)
            tempin = True
    # ---
    if not tempin:
        return text
    # ---
    return parsed.string


if __name__ == '__main__':
    import pywikibot

    text = """{{Ficha de medicamento
        | IUPAC_name      = (''R'',''R'')-(+)-Methyl 2-phenyl-2-(2-piperidyl)acetate

        <!--Clinical data-->
        | image           = Dexmethylphenidate structure.svg
        | width           = 200
        | image2          = Dextromethylphenidate-based-on-hydrochloride-xtal-1995-3D-balls.png

        <!--Names-->
        | pronounce       =
        | tradename       = Focalin, Focalin XR, Attenade, others
        | Drugs.com       = {{drugs.com|monograph|dexmethylphenidate-hydrochloride}}
        | MedlinePlus     = a603014

        <!-- Legal status -->
        | DailyMedID      = Dexmethylphenidate

        <!-- Pharmacokinetic data -->
        | pregnancy_AU    = <!-- A / B1 / B2 / B3 / C / D / X -->
        | pregnancy_AU_comment=
        | pregnancy_US    = C
        | pregnancy_US_comment= <ref name=Preg2019 />
        | pregnancy_category=
        | legal_AU        = Schedule 8
        | legal_CA        = Schedule III
        | legal_DE        = Anlage III
        | legal_UK        = Class B
        | legal_US        = Schedule II
        | legal_status    =
        | dependency_liability= Physical: None Psychological: High

        <!--External links-->
        | routes_of_administration= By mouth
        | bioavailability = 11–52%
        | protein_bound   = 30%
        | metabolism      = [[Liver]]
        | onset           =
        | elimination_half-life= 4 hours
        | duration_of_action=
        | excretion       = [[Kidney]]

        <!--Chemical data-->
        | synonyms        = d-threo-methylphenidate (D-TMP)
        | C               = 14
        | H               = 19
        | N               = 1
        | O               = 2
        | SMILES          = O=C([C@@H]([C@@H]1NCCCC1)C2=CC=CC=C2)OC
        | StdInChI        = 1S/C14H19NO2/c1-17-14(16)13(11-7-3-2-4-8-11)12-9-5-6-10-15-12/h2-4,7-8,12-13,15H,5-6,9-10H2,1H3/t12-,13-/m1/s1
        | StdInChIKey     = DUGOZIWVEXMGBE-CHWSQXEVSA-N
        | StdInChIKey_Ref = {{stdinchicite|correct|chemspider}}
        | StdInChI_Ref    = {{stdinchicite|correct|chemspider}}
        | verifiedrevid   = 460779887
        | Verifiedfields  = changed
        | Watchedfields   = changed
        }}

        El '''dexmetilfenidato''', vendido bajo la marca Focalin entre otras, es un medicamento utilizado para tratar el [[trastorno por déficit de atención con hiperactividad]]  en mayores de 5 años. <ref name="AHFS2019">{{Cita web|url=https://www.drugs.com/monograph/dexmethylphenidate-hydrochloride.html|título=Dexmethylphenidate Hydrochloride Monograph for Professionals|fechaacceso=15 de abril de 2019|sitioweb=Drugs.com|editorial=American Society of Health-System Pharmacists|idioma=en|urlarchivo=https://web.archive.org/web/20201107154606/https://www.drugs.com/monograph/dexmethylphenidate-hydrochloride.html|fechaarchivo=7 de noviembre de 2020}}</ref> Si no se observa ningún beneficio después de 4 semanas, es razonable suspender su uso. <ref name="AHFS2019"/> Se toma por vía oral. <ref name="AHFS2019"/> La formulación de liberación inmediata dura hasta 5 horas, mientras que la formulación de liberación prolongada dura hasta 12 horas. <ref>{{Cita libro|título=Mosby's Drug Reference for Health Professions - E-Book|fecha=2013|editorial=Elsevier Health Sciences|isbn=9780323187602|página=455|url=https://books.google.ca/books?id=41z07XtCfa0C&pg=PA455|fechaacceso=2019-04-15|fechaarchivo=https://web.archive.org/web/20200515132241/https://books.google.ca/books?id=41z07XtCfa0C&pg=PA455}}</ref>

        Los efectos secundarios comunes incluyen dolor abdominal, pérdida de apetito y fiebre. Los efectos secundarios graves pueden incluir abuso, [[psicosis]], muerte súbita cardíaca, [[manía]], [[anafilaxia]], [[convulsiones]] y erección peligrosamente prolongada. La seguridad durante el embarazo y la [[lactancia]] no está clara. El dexmetilfenidato es un estimulante del sistema nervioso central . No está claro cómo actúa en el TDAH. Es el enantiómero más activo del metilfenidato.  <ref name=Preg2019>{{cita web|título=Dexmethylphenidate Use During Pregnancy |url=https://www.drugs.com/pregnancy/dexmethylphenidate.html |sitioweb=Drugs.com |fechaacceso=2019-04-15 |idioma=en |fechaarchivo=2019-04-15 |urlarchivo=https://web.archive.org/web/20190415194448/https://www.drugs.com/pregnancy/dexmethylphenidate.html }}</ref> <ref name="Moen2009">{{Cita publicación|título=Dexmethylphenidate extended release: a review of its use in the treatment of attention-deficit hyperactivity disorder|apellidos=Moen MD, Keam SJ|fecha=diciembre de 2009|publicación=CNS Drugs|volumen=23|número=12|páginas=1057–83|doi=10.2165/11201140-000000000-00000|pmid=19958043}}</ref> <ref name="AHFS2019"/>

        El uso médico del dexmetilfenidato se aprobó en [[Estados Unidos]] en 2001.<ref name="Daily2019" group="test">{{cita web|título=DailyMed - dexmethylphenidate hydrochloride tablet |url=https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=779ece39-b6fa-4977-8df5-d018d39d4d0d |sitioweb=dailymed.nlm.nih.gov |fechaacceso=15 de abril de 2019 |fechaarchivo=2020-08-07 |urlarchivo=https://web.archive.org/web/20200807103106/https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=779ece39-b6fa-4977-8df5-d018d39d4d0d  }}</ref> Está disponible como [[medicamento genérico]].<ref name=AHFS2019/> El costo al por mayor de un suministro para un mes en Estados Unidos es de unos 8 USD.<ref name=NADAC2019>{{cita web|título=NADAC as of 2019-02-27 |url=https://data.medicaid.gov/Drug-Pricing-and-Payment/NADAC-as-of-2019-02-27/s7c9-pfa6 |sitioweb=Centers for Medicare and Medicaid Services |fechaacceso=3 de marzo de 2019 |fechaarchivo=2019-03-06 |urlarchivo=https://web.archive.org/web/20190306044447/https://data.medicaid.gov/Drug-Pricing-and-Payment/NADAC-as-of-2019-02-27/s7c9-pfa6 }}</ref> En 2017, ocupó el puesto 189 entre los medicamentos más recetados en Estados Unidos, con más de tres millones de recetas. También está disponible en [[Suiza]].<ref>{{cita web|título= The Top 300 of 2020 | url = https://clincalc.com/DrugStats/Top300Drugs.aspx |sitioweb= ClinCalc |fechaacceso= 11 de abril de 2020 |fechaarchivo= 12 de febrero de 2021 |urlarchivo= https://web.archive.org/web/20210212142534/https://clincalc.com/DrugStats/Top300Drugs.aspx }}</ref><ref name="ref1">{{cita web|título= Dexmethylphenidate Hydrochloride - Drug Usage Statistics |sitioweb= ClinCalc | url = https://clincalc.com/DrugStats/Drugs/DexmethylphenidateHydrochloride |fechaacceso= 11 de abril de 2020 |fechaarchivo= 12 de abril de 2020 |urlarchivo= https://web.archive.org/web/20200412011147/https://clincalc.com/DrugStats/Drugs/DexmethylphenidateHydrochloride  }}</ref><ref>{{cita web|título=Focalin XR |url=https://www.drugs.com/international/focalin-xr.html |sitioweb=Drugs.com |fechaacceso=15 de abril de 2019 |idioma=en |fechaarchivo=15 de abril de 2019 |urlarchivo=https://web.archive.org/web/20190415200212/https://www.drugs.com/international/focalin-xr.html  }}</ref>

        == Referencias ==
        {{listaref}}

        ==Enlaces externos==
        {{Traducido ref|en|User:Mr. Ibrahem/Dexmethylphenidate|oldid=1164576097|trad=|fecha=09 de julio de 2023}}
        {{Portal|Medicina}}
        {{Control de autoridad}}

        [[Categoría:Farmacología]]
        """

    new_text = mv_es_refs(text)
    pywikibot.showDiff(text, new_text)
