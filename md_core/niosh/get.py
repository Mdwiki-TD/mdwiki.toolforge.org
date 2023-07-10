'''
python pwb.py niosh/s
python3 core8/pwb.py niosh/s
'''
import sys
import os
import re
import json
import urllib.parse
import pywikibot
import wikitextparser
import codecs
# ---
from mdpy import printe
# ---
Dir = os.path.dirname(os.path.abspath(__file__))
Dird = f"{Dir}/downloads/"
cite_file = f"{Dird}/cite_all_links.json"
both_file = f"{Dir}/jsons/both.json"
# ---
data = json.load(open(cite_file, 'r'))
# ---
boths = json.load(open(both_file, 'r'))
# ---


def run(x, urls):
    by_title = {}
    by_url = {}
    # ---
    urls_ = [x.lower() for x in urls]
    # ---
    for title, links in boths.items():
        ya = []
        for link in links:
            if link.lower() in urls_:
                ya.append(link)
                if not link in by_url:
                    by_url[link] = []
                if not title in by_url[link]:
                    by_url[link].append(title)
        # ---
        if len(ya) > 0:
            by_title[title] = ya
    # ---
    for _u in urls:
        if _u not in by_url:
            by_url[_u] = []
    # ---
    # sort by_url keys
    by_url = {k: v for k, v in sorted(by_url.items(), key=lambda item: item[0].lower(), reverse=False)}
    # ---
    json.dump(by_title, codecs.open(f"{Dir}/by_title/{x}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    json.dump(by_url, codecs.open(f"{Dir}/by_url/{x}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # ---
# ---
for x, urls in data.items():
    run(x, urls)
    # break
