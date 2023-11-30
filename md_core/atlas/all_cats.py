# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py atlas/all_cats

"""
import os
import json
from pathlib import Path
from new_api.ncc_page import MainPage as ncc_MainPage

# Specify the root folder
main_dir = Path(__file__).parent
root_folder = os.path.join(str(main_dir), 'images')

def get_info(root):
    info_file_path = os.path.join(root, 'info.json')

    # Read information from info.json
    with open(info_file_path, "r", encoding="utf-8") as info_file:
        info_data = json.load(info_file)
    
    return info_data

def process_folders(root_folder):
    all_diseases = {}

    for root, dirs, files in os.walk(root_folder):
        # Check if there's an info.json file in the current folder
        if "info.json" not in files:
            print(f"No info.json file found in {root}")
            continue
        
        info_data = get_info(root)
        disease_name = info_data.get("disease_name", "").replace("_", " ")
        images_info  = info_data.get("images_info", {})
        if disease_name:
            all_diseases[disease_name] = len(images_info.keys())

    all_diseases = dict(sorted(all_diseases.items(), key=lambda x: x[1], reverse=True))

    text  = '{| class="wikitable sortable"\n|-\n'
    text += '! Category !! Image set !! Number of images\n|-\n'
    n     = 0
    for x, count in all_diseases.items():
        n += 1
        text += f'! {n} || [[:Category:{x}]] || [[{x}]] || {count} ||\n|-\n'

    text += '|}'

    page      = ncc_MainPage('User:Mr._Ibrahem/Atlasdermatologico', 'www', family='nccommons')
    # ---
    page.save(newtext=text, summary='update', nocreate=0, minor='')

if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folders(root_folder)
