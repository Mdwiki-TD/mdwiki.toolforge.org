"""
from wprefs.files import reffixed_list, setting, append_reffixed_file
"""
#
# (C) Ibrahem Qasim, 2023
#
#
import json
import codecs
import os
import sys
from pathlib import Path

# ---
sys.path.append('/data/project/mdwiki/md_core/')
# ---
from wprefs.helps import exepts

# ---
project = '/data/project/mdwiki'
# ---
if not os.path.isdir(project):
    project = 'I:/mdwiki'
# ---
Dir = Path(__file__).parent
# ---
fixwikirefs = project + '/confs/fixwikirefs.json'
reffixed_file = f'{Dir}/reffixed.csv'
# ---
setting = {}
# ---
if os.path.isfile(fixwikirefs):
    try:
        setting = json.load(codecs.open(fixwikirefs, "r", encoding="utf-8-sig"))
        # print(setting)
    except Exception:
        setting = {}


def make_ref_done_list():
    # ---
    reffixed = ''
    # ---
    try:
        with codecs.open(reffixed_file, "r", encoding="utf-8-sig") as mama:
            reffixed = mama.read()
        mama.close()
    except Exception:
        exepts()
    # ---
    reffixed_list = [x.strip() for x in reffixed.split('\n') if x.strip() != '']
    # ---
    return reffixed_list


# ---
reffixed_list = make_ref_done_list()


def append_reffixed_file(lang, title, titles=[]):
    lio = f'{lang}:{title}'
    # ---
    if titles:
        nan = "\n".join([f'{lang}:{t}' for t in titles])
        lio += f"\n{nan}"
    # ---
    with codecs.open(reffixed_file, "a", encoding="utf-8") as ggg:
        ggg.write('\n' + lio)
    ggg.close()


def save_wprefcash(title, newtext):
    # ---
    title2 = title
    title2 = title2.replace(':', '-').replace('/', '-').replace(' ', '_')
    # ---
    try:
        filename = project + '/public_html/wprefcash/' + title2 + '.txt'
        with codecs.open(filename, "w", encoding="utf-8") as uy:
            uy.write(newtext)
        uy.close()
        # ---
        print(filename)
        # ---
    except Exception:
        exepts()

        filename = project + '/public_html/wprefcash/title2.txt'
        with codecs.open(filename, "w", encoding="utf-8") as gf:
            gf.write(newtext)
        gf.close()
        # ---
        print(filename)
    # ---
    return ''
