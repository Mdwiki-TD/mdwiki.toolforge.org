# -*- coding: utf-8 -*-
"""
:write python code to do:
1. Import necessary libraries for web scraping and file manipulation, such as os, requests, BeautifulSoup, json, and pathlib.

2. Define a variable 'main_dir' to represent the parent directory using the pathlib module.

3. Create a function named 'save_image' that takes a URL, folder name, and file name as parameters. Use the requests library to download the image and save it to the specified folder.

4. Create a function named 'process_disease_page' that takes a disease URL as a parameter. Inside this function, use requests to get the HTML content, BeautifulSoup to parse it, and extract information about image links. Return a dictionary with image names as keys and their corresponding URLs as values. Modify the format of 'image_name' to '{disease_name}_image_{index + 1}.jpg'.

5. Create a function named 'scrape_data' that takes a starting URL as a parameter. Inside this function, use requests and BeautifulSoup to navigate the given URL, find disease items, and iterate through them. For each disease item, call 'process_disease_page' to get image information and create a folder with 'create_folder'.

6. Create a function named 'create_folder' that takes a folder name, disease name, disease URL, and image information as parameters. Use os to create a folder with the specified name in 'main_dir'. Create an info.json file inside the folder, containing the disease name, disease URL, and the image information.

7. In the 'scrape_data' function, after creating the folder, iterate through the image information and call 'save_image' to download and save each image.

8. In the main block, set the initial URL (e.g., "https://www.atlasdermatologico.com.br/browse.jsf") and call 'scrape_data' to initiate the scraping process.

Note: Adjust the URL and other details as needed for your specific use case.

"""
