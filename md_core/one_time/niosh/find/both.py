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
both_file = f"{Dir2}/jsons/both.json"
file_all_links = f"{Dir2}/jsons/all_links.json"
# ---
both = json.load(codecs.open(both_file, 'r', encoding='utf-8'))
# ---
print(f'all pages:{len(both.keys())}')
# ---
# sort both keys by lenth of it list


def do_all():
    # ---
    all_links = []

    def fix_links(x):
        x = x.split("#")[0].strip()
        x = re.sub(r'^https*://(www.|)cdc.gov/', 'https://www.cdc.gov/', x)
        return x

    # ---
    for x, le in both.items():
        all_links.extend(le)
    # ---
    all_links = list(set(all_links))
    # ---
    all_links = [fix_links(x) for x in all_links]
    # ---
    all_links = sorted(all_links, key=lambda x: x.lower(), reverse=False)
    # ---
    all_links = list(set(all_links))
    # ---
    json.dump(all_links, codecs.open(file_all_links, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    # ---
    len_all_links = len(all_links)
    # ---
    print(f'{len_all_links=}')


aa = {k: v for k, v in sorted(both.items(), key=lambda item: len(item[1]), reverse=True)}

n = 0

for x, le in aa.items():
    n += 1
    x2 = x.ljust(60)
    print(f'x: {x2}\t lenth:{len(le)}')
    if len(le) < 15:
        break
# ---

do_all()
