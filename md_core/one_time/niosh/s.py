'''
python pwb.py niosh/s
python3 core8/pwb.py niosh/s
'''
import os
from pathlib import Path
import re
import json
import codecs

# ---
from mdpy import printe

# ---
Dir = Path(__file__).parent
Dird = f"{Dir}/downloads/"
Dird_js = f"{Dir}/downloads_js/"
cite_file = f"{Dird_js}/cite_all_links.json"
# ---

nas_rep = {
    # "nn": "date",
    "ti": "title",
    # "au": "author",
    # "so": "source",
    "lt": "url",
}
cite_all_links = {}


def work_in_file(filename):
    filename2 = os.path.join(Dird_js, filename)
    # ---
    text = codecs.open(filename2, 'r', encoding='utf-8').read()
    # ---
    n = 0
    # ---
    tab = []
    # ---
    for x in text.split('NN:'):
        n += 1
        # ---
        if n == 1:
            continue
        # ---
        x = f"NN: {x.strip()}"
        # ---
        # x = re.sub(r'\s*\n\s\s\s\s', ' ', x)
        # ---
        nan = {}
        # ---
        for z in x.splitlines():
            # printe.output(z)
            # if z match "^(\w\w):(.*?)$"
            z = z.strip()
            mat = re.match(r'^(\w\w):(.*?)$', z)
            if mat:
                na = mat.group(1)
                na = nas_rep.get(na.lower(), na)
                # ---
                value = mat.group(2).strip()
                value = re.sub(r'\s+', ' ', value)
                # ---
                nan[na] = value
        # ---
        tab.append(nan)
        # ---
    # ---
    lista = [x['url'].replace('http://', 'https://') for x in tab if x.get('url', '').find('cdc.gov/niosh/') != -1]
    lista = sorted(lista, key=lambda x: x.lower(), reverse=False)
    # ---
    lista = list(set(lista))
    # ---
    cite_all_links[filename.replace('.txt', '')] = lista
    # ---
    json.dump(tab, codecs.open(f"{filename2}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # ---


# scan all txt files in Dir and work on them
for filename in os.listdir(Dird):
    if filename.endswith('.txt'):
        filename2 = os.path.join(Dird, filename)
        # ---
        printe.output(f'filename: {filename2}..')
        # ---
        work_in_file(filename)
        # break
# ---
json.dump(cite_all_links, codecs.open(cite_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
