'''

python3 core8/pwb.py WHOem/lists/lang_links new
#---
with codecs.open(f'{Dir}/lists/lang_links.json', 'r', encoding='utf-8') as f:
    lang_links = json.load(f) # {'en': 'enwiki', 'redirect_to': '', 'langs': {'ar': 'arwiki'}}
#---
with codecs.open(f'{Dir}/lists/links_not_found.json', 'r', encoding='utf-8') as f:
    links_not_found = json.load(f) # ["error"]
#---
len of links_not_found: 7:
    Acetylsalicylic acid/atorvastatin/ramipril
    Acetylsalicylic acid/simvastatin/ramipril/atenolol/hydrochlorothiazide
    Amodiaquine/sulfadoxine/pyrimethamine
    Atorvastatin/perindopril/amlodipine
    Recombinant factor IX
    Factor IX concentrate
    Isoniazid/rifapentine

'''
import sys
import os
import json
import codecs
from pathlib import Path

# ---
from new_api.wiki_page import MainPage, change_codes
from mdpy import printe

# ---
from mdpy.bots import sql_for_mdwiki

# sql_for_mdwiki.mdwiki_sql(query, update = False)
mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# ---
Dir = Path(__file__).parent.parent
# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
with codecs.open(f'{Dir}/lists/md_links.json', 'r', encoding='utf-8') as f:
    md_links = json.load(f)
# ---
with codecs.open(f'{Dir}/lists/lang_links.json', 'r', encoding='utf-8') as f:
    lang_links = json.load(f)
# ---
links_not_found = []


def find_wd(title):
    qid = mdtitle_to_qid.get(title)
    # ---
    if qid is None:
        return
    # ---
    printe.output(f'qid: {qid}')


def work_in_page(title):
    # ---
    page = MainPage(title, 'en')
    # ---
    if not page.exists():
        printe.output(f'<<red>> page: {title} not found in enwiki.')
        links_not_found.append(title)
        return find_wd(title)
    # ---
    if title not in lang_links:
        lang_links[title] = {'en': title, 'redirect_to': "", 'langs': {}}
    # ---
    if page.isRedirect():
        target = page.get_redirect_target()
        if target != '':
            page = MainPage(target, 'en')
            lang_links[title]['en'] = target
            lang_links[title]['redirect_to'] = target
    # ---
    langlinks = page.get_langlinks()
    # ---
    langlinks['en'] = title
    # ---
    printe.output(f"<<blue>> en:{title}, \n\tlanglinks: {len(langlinks)}")
    # ---
    for lang, tit in langlinks.items():
        # ---
        lang = change_codes.get(lang) or lang
        # ---
        lang_links[title]['langs'][lang] = tit


def main():
    printe.output(f'list len of it: {len(md_links)}')
    # ---
    n = 0
    # ---
    for x in md_links:
        # ---
        n += 1
        # ---
        if 'new' in sys.argv and len(lang_links.get(x, {}).get('langs', {})) > 0:
            continue
        # ---
        pap = f'p {n}/{len(md_links)}: {x}'
        # ---
        printe.output(pap)
        # ---
        work_in_page(x)
    # ---
    with codecs.open(f'{Dir}/lists/lang_links.json', 'w', encoding='utf-8') as f:
        json.dump(lang_links, f, ensure_ascii=False, indent=4)
    # ---
    printe.output(f'<<lightred>> len of links_not_found: {len(links_not_found)}:')

    with codecs.open(f'{Dir}/lists/links_not_found.json', 'w', encoding='utf-8') as f:
        json.dump(links_not_found, f, ensure_ascii=False, indent=4)
    # ---
    for title in links_not_found:
        print(f'\t{title}')


if __name__ == '__main__':
    main()
