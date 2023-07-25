'''

from prior.json_en.lists import json_en_all
'''
import sys
import os
import json
#---
Dir = os.path.dirname(os.path.abspath(__file__))
# ---
project_js_new = Dir
# ---
json_en_all = {}
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
        json_en_all = {**json_en_all, **data}
# ---
