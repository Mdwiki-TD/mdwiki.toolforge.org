'''
# ---
from prior.json_langs.lists import json_langs_by_langs
# tab = json_langs_by_langs.get(lang, {}).get(title, {})# {'extlinks': extlinks, 'refsname': refsname}
# ---
'''
import os
from pathlib import Path
import json

# ---
Dir = Path(__file__).parent
# ---
project_js_new = Dir
# ---
json_langs_all = {}
# ---
# get All json file inside dir project_js_new
for filename in os.listdir(project_js_new):
    if filename.endswith('.json'):
        filename2 = os.path.join(project_js_new, filename)
        # ---
        print(f'filename: {filename2}..')
        # ---
        data = json.load(open(filename2))
        # ---
        json_langs_all = {**json_langs_all, **data}
# ---
json_langs_by_langs = {}
# ---
for en, tab in json_langs_all.items():
    for lang, ta in tab['langs'].items():
        if lang not in json_langs_by_langs:
            json_langs_by_langs[lang] = {}
        # ---
        title = ta['title']
        extlinks = ta['extlinks']
        refsname = ta['refsname']
        # ---
        json_langs_by_langs[lang][title] = {'extlinks': extlinks, 'refsname': refsname, 'en': en}
# ---
