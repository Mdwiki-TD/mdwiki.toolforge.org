#!/usr/bin/python3
"""

@WikiProjectMed

python pwb.py twet/t
python twet.py
"""
#
# (C) Ibrahem Qasim, 2022
#
#
# ---
import tweepy
import re
import sys
import os
import codecs
import json
import requests
import random

# ---
# ---
import twet_config


def send(link):
    # ---
    # Create variables for each key, secret, token
    consumer_key = twet_config.consumer_key
    consumer_secret = twet_config.consumer_secret
    access_token = twet_config.access_token
    access_token_secret = twet_config.access_token_secret
    # ---
    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    # ---
    article = link.replace("_", " ")
    link = 'https://mdwiki.org/wiki/' + link.replace(" ", "_")
    tweet = f'''Today article is: {article}\n{link}'''
    # ---
    response = client.create_tweet(text=tweet)
    # ---
    data = getattr(response, 'data')
    if data and getattr(data, 'id') is not None:
        print(data.id)
        return True


def do_api(params):
    # ---
    params["format"] = "json"
    params["utf8"] = 1
    # ---
    url = 'https://' + 'mdwiki.org/w/api.php'
    # ---
    json1 = {}
    try:
        r4 = requests.Session().post(url, data=params)
        json1 = json.loads(r4.text)
        return json1
    except Exception:
        return {}
    # ---
    return {}


# ---
title = 'WikiProjectMed:List'
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
json_file = project + '/md_core/tw/done.json'


def get_links():
    # ---
    sects = do_api({"action": "parse", "page": title, "prop": "sections"})
    # pri   nt(sects)
    sections = sects.get("parse", {}).get("sections", {})
    # ---
    level = False
    for x in sections:
        lline = x['line'].strip().lower()
        if lline == 'conditions':
            level = x["index"]
            break
    # ---
    section_text = ''
    # ---
    if level:
        level = str(level)
        # ---
        print(level)
        # ---
        uxu = do_api({"action": "parse", "page": title, "prop": "sections|wikitext", "section": level})
        # ---
        section_text = uxu.get("parse", {}).get("wikitext", {}).get("*", "")
        # ---
    # ---
    link_regex = re.compile(r'\[\[(.*?)\]\]')
    vaild_links = []
    # ---
    for m2 in link_regex.finditer(section_text):
        sa = re.compile(r'\[\[(\:|)(\w{2}|\w{3}|w|en|image|file|category|template)\:', flags=re.IGNORECASE)
        sal = sa.findall(m2.group(0))
        if not sal:
            itemu = m2.group(1).split('|')[0].strip()
            vaild_links.append(itemu)
    # ---
    vaild_links = list(set(vaild_links))
    # ---
    print(f'len of vaild_links: {len(vaild_links)}')
    # ---
    return vaild_links


def get_done():
    # ---
    # ---
    jsj = []
    # ---
    # ---
    if not os.path.exists(json_file):
        with codecs.open(json_file, "w", encoding="utf-8") as ffe:
            json.dump(['XX'], ffe)
        ffe.close()
    # load json file
    with open(json_file) as f:
        jsj = json.load(f)
    f.close()
    return jsj


def get_one_link(done, links):
    # ---
    # chose one link
    link = random.choice(links)
    while link in done:
        link = random.choice(links)
    # ---
    return link


# ---
done = get_done()
links = get_links()
if set(links) == set(done):
    done = ['XX']
# ---
links = list(set(links) - set(done))
# ---
print(f'lenth of links: {len(links)} links:')
# ---
if len(links) == 0:
    print('close')
    sys.exit()
# ---
link = get_one_link(done, links)
# ---
# send it
u = send(link)
# ---
if u == True:
    done.append(link)
    with codecs.open(json_file, "w", encoding="utf-8") as ii:
        json.dump(done, ii)
    ii.close()
    # ---
