#!/usr/bin/python3
"""

إنشاء قائمة بعدد الكلمات

python3 core8/pwb.py mdpy/words newlist
python3 core8/pwb.py mdpy/words newpages
python3 core8/pwb.py mdpy/words listnew

python3 core8/pwb.py mdpy/words more400

python3 core8/pwb.py mdpy/words less100
python3 core8/pwb.py mdpy/words sql

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import os
import json
import codecs
import sys

# ---
# ---
from mdpy.bots import mdwiki_api
from mdpy import printe
from mdcount.links import get_valid_Links

# ---
from mdcount import lead

# ---
json_file = {}
# ---
words_n = {}
# ---
all_words_n = {}


def get_word_files():
    # ---
    global json_file, words_n, all_words_n
    # ---
    project = '/data/project/mdwiki/'
    # ---
    if not os.path.isdir(project):
        project = '/mdwiki'
    # ---
    json_file[1] = project + '/public_html/Translation_Dashboard/Tables/allwords.json'
    # ---
    all_words_n = json.loads(codecs.open(json_file[1], "r", encoding="utf-8").read())
    # ---
    json_file[0] = project + '/public_html/Translation_Dashboard/Tables/words.json'
    # ---
    words_n = json.loads(codecs.open(json_file[0], "r", encoding="utf-8").read())
    # ---
    printe.output(f'len of words_n:{len(words_n.keys())}')

    # ---


# ---
get_word_files()


def log(file, table):
    json.dump(table, open(file, 'w'), sort_keys=True)
    # ---
    printe.output(f'<<lightgreen>> {len(table)} lines to {file}')


# ---
Nore = {1: False}
for arg in sys.argv:
    if arg in ['new', 'listnew', 'less100', 'more400']:
        Nore[1] = True


def mmain():
    # ---
    n = 0
    # ---
    limit = 10000
    if 'limit100' in sys.argv:
        limit = 100
    # ---
    vaild_links = get_valid_Links(words_n)
    # ---
    kkk = {1: vaild_links}
    # ---
    for x in kkk[1]:
        # ---
        n += 1
        # ---
        printe.output('------------------')
        printe.output('page %d from %d, x:%s' % (n, len(kkk[1]), x))
        # ---
        if n >= limit:
            break
        # ---
        text = mdwiki_api.GetPageText(x)
        # ---
        # pageword = mdwiki_api.wordcount(x)
        # leadword = lead.count_lead(x)
        leadword, pageword = lead.count_all(title='', text=text)
        # ---
        printe.output('\t\t pageword:%d' % pageword)
        printe.output('\t\t leadword:%d' % leadword)
        # ---
        all_words_n[x] = pageword
        words_n[x] = leadword
        # ---
        if n == 10 or str(n).endswith('00'):
            log(json_file[0], words_n)
            log(json_file[1], all_words_n)
        # ---
    # ---
    log(json_file[0], words_n)
    log(json_file[1], all_words_n)


# ---
if __name__ == '__main__':
    mmain()
    # ---
    sys.argv.append('sql')
    # ---
    mmain()
# ---
