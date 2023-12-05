#!/usr/bin/python3
"""
Change refs to newlines
python3 core8/pwb.py mdpy/fixref
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import codecs
import sys
import os

from mdpy.fixref.fixref_text_new import fix_ref_template
from mdpy.bots import catdepth2
from mdpy.bots import mdwiki_api
from mdpy import printe

project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
# ---
thenumbers = {1: 20000, 'done': 0}


def work(title):
    # ---
    Ask = False
    if 'ask' in sys.argv:
        Ask = True
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    summary = 'Normalize references'
    # ---
    new_text, summary = fix_ref_template(text, returnsummary=True)
    # ---
    if new_text != text:
        thenumbers['done'] += 1
        # ---
        mdwiki_api.page_put(oldtext=text, newtext=new_text, summary=summary, title=title, returntrue=False, diff=True)
    else:
        printe.output('no changes.')


def main():
    # ---
    List = []
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg == '-number' and value.isdigit():
            thenumbers[1] = int(value)
        # ---
        if arg == '-file':
            text = codecs.open(project + f'/public_html/find/{value.strip()}', 'r', 'utf8').read()
            List = [x.strip() for x in text.split('\n') if x.strip() != '']
        # ---
        if arg == 'allpages':
            List = mdwiki_api.Get_All_pages('')
        # ---
        # python pwb.py mdpy/fixref/start -cat:CS1_errors:_deprecated_parameters ask
        if arg == '-cat':
            List = catdepth2.subcatquery(value, depth='0', ns='0')
        # ---
        # python pwb.py mdpy/fixref/start -page:Histrelin ask
        if arg in ['-page', '-title']:
            List = [value]
        # ---
    # ---
    num = 0
    for title in List:
        num += 1
        # ---
        if thenumbers['done'] >= thenumbers[1] and len(List) > 1:
            break
        work(title)

    # ---


# ---
if __name__ == "__main__":
    main()
# ---
