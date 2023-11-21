"""
from wprefs.bots.fix_pt_months import pt_months
"""
import sys
import re
import wikitextparser as wtp

# ---
# ---
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
# ---
months_lower = {k.lower(): v for k, v in months.items()}
# ---
months_line = "|".join(months.keys())


def make_new_val(val):
    newval = val
    # match month and year
    # ---
    maa = r'^(?P<d>\d{1,2} |)(?P<m>%s) (?P<y>\d{4})$' % months_line
    # match date like : January 10, 2020
    maa2 = r'^(?P<m>%s) (?P<d>\d{1,2}), (?P<y>\d{4})$' % months_line
    # ---
    sas = re.search(maa, val.strip())
    if sas:
        d = sas.group('d')
        m = sas.group('m')
        y = sas.group('y')
        # ---
        pt_m = months_lower.get(m.lower(), '')
        # ---
        if pt_m != '':
            # ---
            if d != '':
                pt_m = f'de {pt_m}'
            # ---
            newval = f"{d} {pt_m} {y}"
        # ---
        return newval
    # ---
    sas2 = re.search(maa2, newval.strip())
    # ---
    if sas2:
        d = sas2.group('d')
        m = sas2.group('m')
        y = sas2.group('y')
        # ---
        pt_m = months_lower.get(m.lower(), '')
        # ---
        if pt_m != '':
            # ---
            if d != '':
                pt_m = f'de {pt_m}'
            # ---
            newval = f"{d} {pt_m} {y}"
        # ---
        return newval
    # ---
    return newval


def pt_months(text):
    parsed = wtp.parse(text)
    tags = parsed.get_tags()
    # ---
    for x in tags:
        if 'dd' in sys.argv:
            print('--------------------------------')
            print(str(x))
            print(dir(x))
        # ---
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
