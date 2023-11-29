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
import os
import json
from pathlib import Path
from nccommons import api

# Specify the root folder
main_dir = Path(__file__).parent
root_folder = os.path.join(str(main_dir), 'images')

# Base URL for nccommons.org API
NCCOMMONS_API_BASE_URL = "https://nccommons.org/api/"


def create_category(disease_name):
    cat_text = '[[Category:Atlasdermatologico]]'
    cat_title = f'Category:{disease_name}'
    # ---
    new = api.create_Page(cat_text, cat_title)
    # ---
    return cat_title


def upload_image(category_name, image_path, image_url, image_name, disease_url):
    # split disease_url to get last text after =
    diseaseid = disease_url.split('=')[-1]
    image_id = image_url.split('=')[-1]
    image_text = f'''== {{int:summary}} ==
{{Information
|Description = 
* Atlasdermatologico disease ID: [{disease_url} {diseaseid}]
* Image ID: [{image_url} {image_id}]
|Date = 
|Source = {disease_url}
|Author = https://www.atlasdermatologico.com.br/
|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/
}}

== {{int:license}} ==
{{CC-BY-NC-SA-3.0}}

[[{category_name}]]
[[Category:Atlasdermatologico]]'''
    file_name = f'File:{image_name}'
    upload = api.upload_by_url(file_name, image_text, image_url, comment='')
    print(f"upload result: {upload}")


# Main function


def process_folders(root_folder):
    for root, dirs, files in os.walk(root_folder):
        # Check if there's an info.json file in the current folder
        if "info.json" not in files:
            print(f"No info.json file found in {root}")
            continue
        info_file_path = os.path.join(root, "info.json")

        # Read information from info.json
        with open(info_file_path, "r") as info_file:
            info_data = json.load(info_file)
        disease_name = info_data.get("disease_name")
        disease_url = info_data.get("disease_url")
        images_info = info_data.get("images_info", {})

        if not disease_name:
            print(f"No disease_name found in {info_file_path}")
            continue

        # Create category
        category = create_category(disease_name)

        if category:
            # Upload images
            for image_name, image_url in images_info.items():
                image_path = os.path.join(root, image_name)
                upload_image(category, image_path, image_url, image_name, disease_url)
        break


if __name__ == "__main__":
    # Process all subfolders in the specified root folder
    process_folders(root_folder)
