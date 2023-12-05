"""

python3 core8/pwb.py priorviews/find/find_creator new
python3 core8/pwb.py priorviews/find/find_creator -lang:ar

"""
from mdpy.bots import wiki_sql
import sys
import json
import os
from pathlib import Path
import codecs
from pymysql.converters import escape_string

# ---
from mdpy import printe

# ---
from priorviews.lists.links_by_section import links_by_lang
from priorviews.bots import helps

# ---
Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file = f'{Dir2}/lists/creators_by_lang.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
CreatorsData = json.load(codecs.open(file, 'r', 'utf-8'))


def log_Data():
    printe.output(f'<<yellow>> log_Data {len(CreatorsData)} CreatorsData')
    # dump CreatorsData
    helps.dump_data(file, CreatorsData)

    # ---


ADDED = 0


def get_creator(links, lang):
    # ---
    if lang not in CreatorsData:
        CreatorsData[lang] = {}

    def valid(x, tab, empty=''):
        i = tab.get(x) or tab.get(x.lower())
        if not i or i == empty:
            return True
        return False

    # ---
    if "new" in sys.argv:
        # links = [ x for x in links if not x in CreatorsData[lang] or CreatorsData[lang][x] == '']
        links = [x for x in links if valid(x, CreatorsData[lang])]
    # ---
    print(f'lang: {lang}, links: {len(links)}')
    # ---
    if len(links) == 0:
        return
    # ---
    # split links to 100 per group
    for i in range(0, len(links), 100):
        titles = [x.replace(" ", "_") for x in links[i : i + 100]]
        # ---
        titles = ", ".join([f'"{escape_string(x)}"' for x in titles])
        # ---
        query = f'''select rev_timestamp, page_title, actor_name, comment_text
            from revision, actor, page, comment
            where actor_id = rev_actor
            and rev_parent_id = 0
            and page_id = rev_page
            and page_namespace = 0
            and rev_comment_id = comment_id
            and page_title in ({titles})
        '''
        # ---
        result = wiki_sql.sql_new(query, lang)
        # ---
        for x in result:
            time_stamp = int(x["rev_timestamp"])
            page_title = x["page_title"].replace("_", " ")
            actor_name = x["actor_name"].replace("_", " ")
            comment_text = x["comment_text"]
            # ---
            TD = False
            # ---
            if comment_text.find("|User:Mr. Ibrahem/") != -1:
                TD = True
            # ---
            print(f"time:{time_stamp}", f"title:{page_title}", f"actor:{actor_name}")
            # ---
            tab = {"time": time_stamp, "actor": actor_name, "comment": comment_text, "TD": TD}
            # ---
            ADDED += 1
            # ---
            CreatorsData[lang][page_title] = tab
            # ---
            if ADDED % 50 == 0:
                log_Data()
            # ---
        # ---
        if "testt" in sys.argv:
            print(result)
            break


def start():
    # ---
    langkeys = links_by_lang.keys()
    # ---
    for arg in sys.argv:
        arg, sep, value = arg.partition(":")
        if arg == "-lang":
            langkeys = [value]
    # ---
    n = 0
    # ---
    for lang in langkeys:
        # ---
        links = links_by_lang[lang]
        # ---
        n += 1
        # ---
        get_creator(links, lang)
        # ---
    # ---
    log_Data()

    # ---


if __name__ == '__main__':
    start()
