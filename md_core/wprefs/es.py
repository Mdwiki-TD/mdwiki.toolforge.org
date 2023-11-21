"""
"""

import re
import wikitextparser as wtp

# ---
from wprefs.helps import print_s
from wprefs.bots.es_months import fix_es_months
from wprefs.bots.es_section import add_section
from wprefs.bots.es_refs import mv_es_refs

# ---
refs_temps = {
    'cite web': 'cita web',
    "cite arxiv": "cita arxiv",
    "cite certification": "cita certificación",
    "cite conference": "cita conferencia",
    "cite encyclopedia": "cita enciclopedia",
    "cite interview": "cita entrevista",
    "cite episode": "cita episodio",
    "cite newsgroup": "cita grupo de noticias",
    "cite comic": "cita historieta",
    "cite court": "cita juicio",
    "cite book": "cita libro",
    "cite mailing list": "cita lista de correo",
    "cite map": "cita mapa",
    "cite av media notes": "cita notas audiovisual",
    "cite news": "cita noticia",
    "cite podcast": "cita podcast",
    "cite journal": "cita publicación",
    "citation needed": "cita requerida",
    "cite thesis": "cita tesis",
    "cite tweet": "cita tuit",
    "cite av media": "cita video",
    "cite video game": "cita videojuego",
}
# ---
args_to = {
    "title": "título",
    "website": "sitioweb",
    "access-date": "fechaacceso",
    "accessdate": "fechaacceso",
    "language": "idioma",
    "archive-url": "urlarchivo",
    "archiveurl": "urlarchivo",
    "date": "fecha",
    "archive-date": "fechaarchivo",
    "archivedate": "fechaarchivo",
    "first": "nombre",
    "last": "apellidos",
    "first1": "nombre1",
    "last1": "apellidos1",
    "last2": "apellidos2",
    "first2": "nombre2",
}
# ---
params = {
    "nombre1": ["first1", "given1"],
    "enlaceautor1": [
        "authorlink1",
        "author1-link",
        "author-link1",
    ],
    "enlaceautor": [
        "author-link",
        "authorlink",
    ],
    "título": ["title"],
    "fechaacceso": ["accessdate"],
    "año": ["year"],
    "fecha": ["date"],
    "editorial": ["publisher"],
    "apellido-editor": ["editor-last", "editor-surname", "editor1-last"],
    "nombre-editor": ["editor-first", "editor-given", "editor1-first", "editor1-given"],
    "enlace-editor": ["editor-link", "editor1-link"],
    "ubicación": ["place", "location"],
    "lugar-publicación": ["publication-place"],
    "fecha-publicación": ["publication-date"],
    "edición": ["edition"],
    "sined": ["noed"],
    "volumen": ["volume"],
    "página": ["page"],
    "páginas": ["pages"],
    "en": ["at"],
    "enlace-pasaje": ["url-pasaje"],
    "idioma": ["language"],
    "título-trad": ["trans_title"],
    "capítulo": ["chapter"],
    "url-capítulo": ["url-chapter"],
    "capítulo-trad": ["trans_chapter"],
    "formato": ["format"],
    "cita": ["quote"],
    "separador": ["separator"],
    "resumen": ["laysummary", "layurl"],
    "fecha-resumen": ["laydate"],
    "apellidos1": [
        "last1",
    ],
    "apellidos2": [
        "last2",
    ],
    "nombre2": ["first2", "given2"],
    "enlaceautor2": ["authorlink2", "author2-link", "authorlink2"],
    "apellidos3": ["last3", "surname3", "author3"],
    "nombre3": ["first3", "given3"],
    "enlaceautor3": ["authorlink3", "author3-link", "authorlink3"],
    "apellidos4": ["last4", "surname4", "author4"],
    "nombre4": ["first4", "given4"],
    "enlaceautor4": ["authorlink4", "author4-link", "authorlink4"],
    "apellidos5": ["last5", "surname5", "author5"],
    "nombre5": ["first5", "given5"],
    "enlaceautor5": ["authorlink5", "author5-link", "authorlink5"],
    "apellidos6": ["last6", "surname6", "author6"],
    "nombre6": ["first6", "given6"],
    "enlaceautor6": ["authorlink6", "author6-link", "authorlink6"],
    "apellidos7": ["last7", "surname7", "author7"],
    "nombre7": ["first7", "given7"],
    "enlaceautor7": ["authorlink7", "author7-link", "authorlink7"],
    "apellidos8": ["last8", "surname8", "author8"],
    "nombre8": ["first8", "given8"],
    "enlaceautor8": ["authorlink8", "author8-link", "authorlink8"],
    "apellidos9": ["last9", "surname9", "author9"],
    "nombre9": ["first9", "given9"],
    "enlaceautor9": ["authorlink9", "author9-link", "authorlink9"],
    "separador-nombres": ["author-name-separator"],
    "separador-autores": ["author-separator"],
    "número-autores": ["display-authors"],
    "otros": ["others"],
}
# ---
for _new, _lal in params.items():
    for _old in _lal:
        args_to[_old] = _new


def fix_temps(text):
    # ---
    parsed = wtp.parse(text)
    # ---
    new_text = text
    # ---
    for template in parsed.templates:
        # ---
        name = str(template.normal_name()).strip()
        # ---
        if name.lower() in refs_temps.keys() or name.lower() in refs_temps.values():
            # ---
            old = template.string
            # ---
            # print_s(f'template = {template}')
            # ---=
            for arg in template.arguments:
                param = arg.name.strip()
                # value = arg.value.strip()
                # ---
                if param in args_to:
                    # ---
                    arg.name = args_to[param]
            # ---
            if template.has_arg('url-status'):
                template.del_arg('url-status')
            # ---
            template_name = refs_temps.get(name, name).strip()
            # ---
            if template_name.lower() != name.lower():
                template.name = template_name
            # ---
            new = template.string
            # ---
            # print_s(f'new = {new}')
            # ---
            new_text = new_text.replace(old, new)
            # ---
    # ---
    return new_text


def add_lang_en(text, lang=''):
    # ---
    print_s('add_lang_en:')
    # ---
    # Match references
    REFS = re.compile(r'(?is)(?P<pap><ref[^>\/]*>)(?P<ref>.*?<\/ref>)')
    # ---
    for Match in REFS.finditer(text):
        pap = Match.group('pap')
        ref = Match.group('ref')
        # ---
        if not ref.strip():
            continue
        # ---
        if re.sub(r'\|\s*language\s*\=\s*\w+', '', ref) != ref:
            continue
        # ---
        ref2 = re.sub(r'(\|\s*language\s*\=\s*)(\|\}\})', r'\g<1>en\g<2>', ref)
        # ---
        if ref2 == ref:
            ref2 = ref.replace('}}</ref>', '|language=en}}</ref>')
        # ---
        if ref2 != ref:
            text = text.replace(pap + ref, pap + ref2)
    # ---
    return text


def fix_es(text, title):
    # ---
    if text.find('#REDIRECCIÓN') != -1:
        return text
    # ---
    if len(text.split('\n')) < 10:
        return text
    # ---
    newtext = text
    # ---
    newtext = fix_es_months(newtext)
    # ---
    newtext = fix_temps(newtext)
    # ---
    newtext = add_section(newtext, title)
    # ---
    newtext = mv_es_refs(newtext)
    # ---
    newtext = newtext.replace('<references />', '{{listaref}}')
    # ---
    return newtext


# ---
