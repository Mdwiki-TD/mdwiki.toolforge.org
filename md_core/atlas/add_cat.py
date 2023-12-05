# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py atlas/add_cat

"""
import os
import json
from pathlib import Path
from tqdm import tqdm
from new_api import printe
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

    n = 0
    for root, dirs, files in os.walk(root_folder):
        # Check if there's an info.json file in the current folder
        if "info.json" not in files:
            printe.output(f"No info.json file found in {root}")
            continue

        info_data = get_info(root)
        disease_name = info_data.get("disease_name", "").replace("_", " ")
        # images_info = info_data.get("images_info", {})
        if disease_name:
            n += 1
            printe.output(f"{n} diseases:{disease_name}:")
            page = ncc_MainPage(f'Category:{disease_name}', 'www', family='nccommons')
            # ---
            categories  = page.get_categories(with_hidden=False)
            # ---
            text = page.text
            # ---
            if 'Category:Atlasdermatologico' not in categories:
                printe.output(categories)
                text += '\n[[Category:Atlasdermatologico]]'
                # ---
                page.save(newtext=text, summary='added [[:Category:Atlasdermatologico]]', nocreate=0, minor='')


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folders(root_folder)
