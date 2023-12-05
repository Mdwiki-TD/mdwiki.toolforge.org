"""
July 25, 1975 should be translated as 25 de julio de 1975
"""
import re
import wikitextparser as wtp

# ---
# ---
es_months_tab = {
    'January': 'enero',
    'February': 'febrero',
    'March': 'marzo',
    'April': 'abril',
    'May': 'mayo',
    'June': 'junio',
    'July': 'julio',
    'August': 'agosto',
    'September': 'septiembre',
    'October': 'ctubre',
    'November': 'noviembre',
    'December': 'diciembre',
}
# ---
es_months_lower = {k.lower(): v for k, v in es_months_tab.items()}
# ---
es_months_line = "|".join(es_months_tab.keys())


def make_new_val(val):
    newval = val
    # match month and year
    # ---
    # match date like : January, 2020 or 10 January, 2020
    maa = r'^(?P<d>\d{1,2} |)(?P<m>%s) (?P<y>\d{4})$' % es_months_line
    # ---
    # match date like : January 10, 2020
    maa2 = r'^(?P<m>%s) (?P<d>\d{1,2}), (?P<y>\d{4})$' % es_months_line
    # ---
    sas = re.search(maa, val.strip())
    # ---
    if not sas:
        sas = re.search(maa2, newval.strip())
    # ---
    if sas:
        d = sas.group('d').strip()
        m = sas.group('m').strip()
        y = sas.group('y').strip()
        # ---
        pt_m = es_months_lower.get(m.lower(), '').strip()
        # ---
        if pt_m != '':
            # ---
            if d != '':
                pt_m = f'de {pt_m}'
            # ---
            newval = f"{d} {pt_m} de {y}"
        # ---
        return newval
    # ---
    return newval


def fix_es_months(text):
    parsed = wtp.parse(text)
    tags = parsed.get_tags()
    # ---
    for x in tags:
        if not x or not x.name:
            continue
        if x.name != 'ref':
            continue
        if not x.contents:
            continue
        # ---
        old = x.contents
        # ---
        parsed2 = wtp.parse(x.contents)
        # ---
        for temp in parsed2.templates:
            for arg in temp.arguments:
                na = arg.name
                val = arg.value.strip()
                # ---
                new_val = make_new_val(val)
                if new_val:
                    # arg.value = new_val
                    temp.set_arg(na, new_val)
                # --
        # ---
        _new = parsed2.string
        # ---
        x.contents = _new
        # ---
    # ---
    text = parsed.string
    # ---
    return text


# ---
