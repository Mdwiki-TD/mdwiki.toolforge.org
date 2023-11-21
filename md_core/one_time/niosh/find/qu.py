'''
python pwb.py niosh/bot
python3 core8/pwb.py niosh/bot
'''
import os
from pathlib import Path
import re
import codecs
import json

# ---
Dir = Path(__file__).parent
Dir2 = os.path.dirname(Dir)
# ---
file = f"{Dir2}/jsons/old/quarry.json"
file_json2 = f"{Dir2}/jsons/old/niosh.json"
# ---
data = json.load(codecs.open(file, 'r', encoding='utf-8'))
new = json.load(codecs.open(file_json2, 'r', encoding='utf-8'))
# ---
result = {}
'''
for item in data:
    page_title = item['page_title']
    el_to = item['el_to']

    if page_title in result:
        result[page_title].append(el_to)
    else:
        result[page_title] = [el_to]
    result[page_title] = list(set(result[page_title]))
    result[page_title].sort()
json.dump(result, codecs.open(file, 'w', encoding='utf-8'))
'''
# ---
# sort
titles = sorted(data.keys())
# ---
all_links = []


def fix_links(x):
    x = re.sub(r'^https*://(www.|)cdc.gov/', 'https://www.cdc.gov/', x)
    return x


# ---
for title in titles:
    exts = data[title]
    title = title.replace("_", " ")
    # ---
    tat = new.get(title, [])
    # ---
    for x in exts:
        if x.find('web.archive.org') > -1:
            # remove url suffix like https://web.archive.org/web/20150530203735/

            x = re.sub(r'^https?://web\.archive\.org/web/\d+/(.*)', r'\1', x.strip())

        if x.find('cdc.gov/niosh/') > -1:
            x = fix_links(x)
            tat.append(x)
    # ---
    tat = list(set(tat))
    # ---
    if tat:
        new[title] = tat
        all_links.extend(tat)
# ---
all_links = sorted(set(all_links))
# ---
# ---
len_all_links = len(all_links)
# ---
print(f'all pages:{len(new.keys())}, {len_all_links=}')
# ---
# sort dict keys
new = {k: v for k, v in sorted(new.items(), key=lambda item: item[0].lower(), reverse=False)}
# ---
json.dump(new, codecs.open(f"{Dir2}/jsons/both.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
