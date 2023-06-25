#!/usr/bin/python
"""
Change refs to newlines
python3 core8/pwb.py mdpy/fixref
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import json
import urllib
import codecs
import pywikibot
import re
import sys
import os
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project): project = '/mdwiki'
# ---
from mdpy import printe
from mdpy.bots import mdwiki_api
from mdpy.bots import txtlib2
# ---
thenumbers = { 1 : 20000 , 'done' : 0 }
# ---
from mdpy.fixref_text_new import fix_ref_template
# ---
def work( title ):
    # ---
    Ask = False
    if 'ask' in sys.argv: Ask = True
    # ---
    text = mdwiki_api.GetPageText( title )
    # ---
    new_text = fix_ref_template( text )
    # ---
    summary = 'Normalize references'
    # ---
    if new_text != text :
        thenumbers['done'] += 1
        # ---
        mdwiki_api.page_put(oldtext=text, newtext=new_text, summary=summary, title=title, returntrue=False, diff=True)
    else:
        printe.output( 'no changes.')
    # ---
def main():
    # ---
    List = []
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(':')
        # ---
        if arg == '-number' and value.isdigit():
            thenumbers[1] = int(value)
        # ---
        if arg == '-file':
            text = codecs.open(project + '/public_html/find/%s' % value.strip() , 'r', 'utf8').read()
            List = [ x.strip() for x in text.split('\n') if x.strip() != '' ]
        # ---
        if arg == 'allpages':
            List = mdwiki_api.Get_All_pages( '' )
        # ---
        # python pwb.py mdwiki/mdpy/fixref -page:Histrelin ask
        if arg in ['-page', '-title']:
            List = [ value ]
        # ---
    # ---
    num = 0
    for title in List:
        num += 1
        # ---
        if thenumbers['done'] >= thenumbers[1] and len(List) > 1:
            break
        work( title ) 
    # ---
# ---
if __name__ == "__main__":
    main()
# ---
