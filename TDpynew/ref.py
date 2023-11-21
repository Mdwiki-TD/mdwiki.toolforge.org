#!/usr/bin/python3
"""
اصلاح المراجع في ميدويكي

python pwb.py mdwiki/public_html/Translation_Dashboard/ref test

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re
import sys

# ---
print_pywikibot = {1: False}
try:
    import pywikibot

    print_pywikibot[1] = True
except BaseException:
    print_pywikibot[1] = False


def outputnew(s):
    if print_pywikibot[1] and 'test' in sys.argv:
        pywikibot.output(s)


# ---
ref_complite = re.compile(r'(<ref\s*name\s*\=*\s*[\"\']*([^>]*)[\"\']*\s*>[^<>]+</ref>)')
ref_short = re.compile(r'(<ref\s*name\s*\=\s*[\"\']*([^>]*)[\"\']*\s*\/\s*>)')


def fix_ref(first, alltext):
    first = first
    # ---
    refs = {}
    # ---
    for m in ref_complite.finditer(alltext):
        refec = m.group()

        name3 = re.sub(r"\s*\"$", "", m.group(2)).strip()

        if name3 != '':
            refs[name3] = refec
            outputnew('--------------------------')
            outputnew(f'name\t:{name3}')
            outputnew(f'ref\t:{refec}')
    # ---
    for g in ref_short.finditer(first):
        refe = g.group()
        # ---
        name = g.group(2).strip()
        name = re.sub(r"\s*\"$", "", name)
        name = name.strip()
        # ---
        outputnew('--------------------------')
        outputnew(f'name\t:{name}')
        outputnew(f'ref\t:{refe}')
        # ---
        rr = refs.get(name, False)
        if name != '' and rr:
            first = first.replace(refe, rr)
    # ---
    return first


# ---
if __name__ == '__main__':
    ff = """"""
    # ---
    all = """"""
    # ---
    if 'test' in sys.argv:
        new = fix_ref(ff, all)
        pywikibot.showDiff(ff, new)
# ---
