'''
# ---
from prior.json_en.lists import json_en_all
# tab = json_en_all.get(en, {})# {'extlinks': extlinks, 'refsname': refsname}
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
json_en_a = {}
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
        json_en_a = {**json_en_a, **data}
# ---
json_en_all = {}
# ---
for en, tab in json_en_a.items():
    # ---
    extlinks = tab['extlinks']
    refsname = tab['refsname']
    # ---
    if tab.get('lead'):
        extlinks.extend(tab['lead']['extlinks'])
        refsname.update(tab['lead']['refsname'])
    # ---
    if tab.get('old'):
        extlinks.extend(tab['old']['extlinks'])
        refsname.update(tab['old']['refsname'])
    # ---
    # refsname = list(set(refsname))
    # extlinks = list(set(extlinks))
    # ---
    json_en_all[en] = {'extlinks': extlinks, 'refsname': refsname}
