# -*- coding: utf-8 -*-
"""
1. open url https://www.atlasdermatologico.com.br/browse.jsf
2. match all <li class="ui-datalist-item">
like:(
    <span itemscope="" itemtype="http://schema.org/MedicalCondition"><a href="/disease.jsf?diseaseId=2" class="capitalized">
    <span itemprop="name">accessory tragus</span>
    <meta itemprop="description" content="photos of accessory tragus" />
    <meta itemprop="relevantSpecialty" content="http://schema.org/Dermatology" /></a>
    </span></li>)
    
3. get disease href and name
4. create folder with the disease name
4. open diseaseId and get all links with class="thumbWrapper" like:(<a href="img?imageId=3" class="thumbWrapper"></a>)
5. open etch image and save it to the folder with the disease name

* use print() to output steps in the code
* images name should be like: {disease_name} (Dermatology Atlas {imageId}).jpg
* disease  url should be like: https://www.atlasdermatologico.com.br/{disease_url} 
* after create_folder should add file like info.json in create_folder contains:
    disease name
    disease_url 
    all images link in the disease_url like:
    "image_name": "image_url"
* add main_dir = Path(__file__).parent, and change : folder_name to os.path.join(str(main_dir), disease_name)
* also image_url = urljoin("https://www.atlasdermatologico.com.br/", link['href'])


python3 md_core/atlas/bot.py

"""
#
import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import json

main_dir = Path(__file__).parent
main_dir = os.path.join(str(main_dir), 'images')

if not os.path.exists(main_dir):
    os.makedirs(main_dir)


def remove_session_id_from_url(url):
    # Define a regular expression to match the session ID pattern
    session_id_pattern = re.compile(r';jsessionid=[^?&]+')

    # Use the regular expression to replace the session ID with an empty string
    cleaned_url = session_id_pattern.sub('', url)

    return cleaned_url


# Function to download and save an image
def save_image(url, folder_name, file_name):
    response = requests.get(url, stream=True)
    image_path = os.path.join(folder_name, file_name)

    with open(image_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


# Function to process disease page and return image information
def process_disease_page(disease_url, disease_name):
    print(f"Processing disease page: {disease_url}")

    response = requests.get(disease_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_links = soup.find_all('a', class_='thumbWrapper')
    images_info = {}

    for index, link in enumerate(image_links):
        image_url = urljoin("https://www.atlasdermatologico.com.br/", link['href'])
        image_url = remove_session_id_from_url(image_url)

        image_name = f"{disease_name} (Dermatology Atlas {index + 1}).jpg"
        images_info[image_name] = image_url

    return images_info


# Main function to scrape data from the given URL
def scrape_data(url):
    print(f"Opening URL: {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    disease_items = soup.find_all('li', class_='ui-datalist-item')

    for item in disease_items:
        disease_name = item.find('span', itemprop='name').get_text().strip()
        disease_name = disease_name.title()

        disease_href = item.find('a')['href']
        disease_url = urljoin("https://www.atlasdermatologico.com.br/", disease_href)
        disease_url = remove_session_id_from_url(disease_url)

        # Step 4: Process disease page and collect image information
        images_info = process_disease_page(disease_url, disease_name)

        # Step 5: Create a folder with the disease name and info.json file
        folder_name = os.path.join(main_dir, disease_name)

        create_folder(folder_name, disease_name, disease_url, images_info)

        # Step 6: Save images in the created folder
        for image_name, image_url in images_info.items():
            save_image(image_url, folder_name, image_name)
            print(f"  - Downloaded image: {image_name}")


def create_folder(folder_name, disease_name, disease_url, images_info):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    info_data = {"disease_name": disease_name, "disease_url": disease_url, "images_info": images_info}

    info_file_path = os.path.join(folder_name, "info.json")
    with open(info_file_path, 'w') as info_file:
        json.dump(info_data, info_file, indent=4)


if __name__ == "__main__":
    atlas_url = "https://www.atlasdermatologico.com.br/browse.jsf"

    # Step 1: Open the URL
    # Step 2-6: Extract data, collect image information, and download images
    scrape_data(atlas_url)
