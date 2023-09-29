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
Dir = Path(__file__).parent.parent
# ---
from mdpy.bots import mdwiki_api
# ---
cat = "World Health Organization essential medicines"
# ---
links = mdwiki_api.subcatquery(cat, depth=3, ns="0")

print(f'md_links.py {len(links)} links found')

with codecs.open(f'{Dir}/lists/md_links.json', 'w', encoding='utf-8') as f:
    json.dump(links, f, ensure_ascii=False, indent=4)
