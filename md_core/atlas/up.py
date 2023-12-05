# -*- coding: utf-8 -*-
"""
write python code to do:
1. work in all sub folders in folder "images"
2. read info.json file in each sub folder
3. from info.json:
* get disease_name create category in nccommons.org with disease_name using def create_category(disease_name)
* get all images links from images_info in info.json like: ("Acanthosis Nigricans-Benign (Dermatology Atlas 1).jpg": "https://www.atlasdermatologico.com.br/img?imageId=1")
* upload images to nccommons.org using def upload_image(category_name, image_path, image_url)

python3 md_core/atlas/up.py
python3 core8/pwb.py atlas/up ask

"""
import sys
import os
import time
import json
from tqdm import tqdm
from new_api import printe
from pathlib import Path
from nccommons import api
from nccommons import mosab_api
from new_api.ncc_page import CatDepth

# Specify the root folder
main_dir = Path(__file__).parent
root_folder = os.path.join(str(main_dir), 'images')

# Base URL for nccommons.org API
NCCOMMONS_API_BASE_URL = "https://nccommons.org/api/"
done = []

pages = CatDepth('Category:Atlasdermatologico', sitecode='www', family="nccommons", depth=1, ns="all", nslist=[], without_lang="", with_lang="", tempyes=[])
time.sleep(5)
print('time.sleep(5)')
len_all_images = []

def create_set( disease_name, image_infos ):
    title = disease_name
    text = ''
    # ---
    if 'noset' in sys.argv: return
    # ---
    title = title.replace('_', ' ').replace('  ', ' ')
    if title in pages:
        printe.output(f'<<lightyellow>>{title} already exists')
        return
    # ---
    text += '{{Imagestack\n|width=850\n'
    text += f'|title={disease_name}\n|align=centre\n|loop=no\n'
    # ---

    # for image_name, image_url in image_infos.items():
    for image_name in image_infos.keys():
        # |File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg|
        text += f'|File:{image_name}|\n'
    text += '\n}}\n[[Category:Image set]]\n'
    text += f'[[Category:{disease_name}|*]]'
    # ---
    new = api.create_Page(text, title)
    # ---
    return new
def create_category(disease_name):
    cat_text = f'* Image set: [[{disease_name}]]\n[[Category:Atlasdermatologico]]'
    cat_title = f'Category:{disease_name}'
    # ---
    if 'nocat' in sys.argv: return cat_title
    # ---
    disease_name = disease_name.replace('_', ' ').replace('  ', ' ')
    if cat_title in pages:
        printe.output(f'<<lightyellow>>{cat_title} already exists')
        return
    # ---
    mosab_api.create_Page(cat_text, cat_title)
    # ---
    return cat_title
def upload_image(category_name, image_path, image_url, image_name, disease_url):
    global len_all_images
    # split disease_url to get last text after =
    image_name = image_name.replace('_', ' ').replace('  ', ' ')
    len_all_images.append(image_name)
    if f'File:{image_name}' in pages:
        printe.output(f'<<lightyellow>> File:{image_name} already exists')
        return
    # ---
    diseaseid = disease_url.split('=')[-1]
    image_id = image_url.split('=')[-1]

    image_text = '== {{int:summary}} ==\n'

    image_text += '{{Information\n' f'|Description = \n* Atlasdermatologico disease ID: [{disease_url} {diseaseid}]\n' f'* Image ID: [{image_url} {image_id}]\n' f'|Date = \n|Source = {disease_url}\n' '|Author = https://www.atlasdermatologico.com.br/\n' '|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/\n' '}}\n' '== {{int:license}} ==\n' '{{CC-BY-NC-SA-3.0}}\n' f'[[{category_name}]]\n' '[[Category:Atlasdermatologico]]'

    upload = mosab_api.upload_by_url(image_name, image_text, image_url, comment='')

    print(f"upload result: {upload}")
def get_info(root):
    info_file_path = os.path.join(root, 'info.json')

    # Read information from info.json
    with open(info_file_path, "r", encoding="utf-8") as info_file:
        info_data = json.load(info_file)

    return info_data
def process_folder(root):
    info_data = get_info(root)
    disease_name = info_data.get("disease_name", "").replace("_", " ")

    if not disease_name:
        print(f"No disease_name found in {os.path.join(root, 'info.json')}")
        return

    if disease_name in done:
        print(f"Skipping {disease_name}")
        return

    disease_url = info_data.get("disease_url")
    images_info = info_data.get("images_info", {})

    print(f'Processing {disease_name}')
    # Create category
    category = create_category(disease_name)

    if category and 'noup' not in sys.argv:
        # Upload images
        n = 0
        for image_name, image_url in tqdm(images_info.items(), desc="Uploading images", total=len(images_info.keys())):
            n += 1
            image_path = os.path.join(root, image_name)
            print(f"Uploading image {n}/{len(images_info.keys())}: {image_name}")
            upload_image(category, image_path, image_url, image_name, disease_url)

    create_set(disease_name, images_info)


def process_folders(root_folder):
    global len_all_images
    for root, dirs, files in os.walk(root_folder):
        # Check if there's an info.json file in the current folder
        if "info.json" not in files:
            print(f"No info.json file found in {root}")
            continue

        process_folder(root)
    # ---
    len_all_images = list(set(len_all_images))
    # ---
    print(f'len_all_images: {len(len_all_images)}')

if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folders(root_folder)
