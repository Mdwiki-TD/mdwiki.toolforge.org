'''
python3 core8/pwb.py WHOem/lists/md_links

with codecs.open(f'{Dir}/lists/md_links.json', 'r', encoding='utf-8') as f:
    md_links = json.load(f)

#---
'''
import json
import codecs
from pathlib import Path

# ---
from mdpy.bots import mdwiki_api

# ---
Dir = Path(__file__).parent.parent
# ---
cats = ["World Health Organization essential medicines", "World Health Organization essential medicines (vaccines)", "World Health Organization essential medicines (alternatives)", "World Health Organization essential medicines (removed)"]
# ---
all_p = []
# ---
for cat in cats:
    links = mdwiki_api.subcatquery(cat, depth=0, ns="0")
    all_p.extend(links)
    print(f'md_links.py {len(links)} links found')
# ---
all_p = list(set(all_p))
# ---
with codecs.open(f'{Dir}/lists/md_links.json', 'w', encoding='utf-8') as f:
    json.dump(all_p, f, ensure_ascii=False, indent=4)
# ---
