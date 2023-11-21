#!/usr/bin/python3
"""

@WikiProjectMed

python t.py test

python3 core8/pwb.py tw/t

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

# Create variables for each key, secret, token
consumer_key = twet_config.consumer_key
consumer_secret = twet_config.consumer_secret
access_token = twet_config.access_token
access_token_secret = twet_config.access_token_secret
bearer_token = twet_config.bearer_token


def auth_ready(tweet, link=None):
    # ---
    api = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    # ---
    # print(dir(api))
    # ---

    # ---
    # t = api.search_recent_tweets(tweet)
    t = api.create_tweet(text=tweet, media_ids=['1582864493234851846'])
    print(t)
    # ---

    # ---
    data = getattr(t, 'data')
    if data is not None and isinstance(data, dict) and data.get('id') is not None:
        print(data.get('id', ''))
        return True


# ---
project = '/data/project/mdwiki'
# ---
if not os.path.isdir(project):
    print(f'{project} is not dir')
    project = '/mdwiki'


def auth(tweet, link=None):
    # ---
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    api = tweepy.API(auth)
    # ---
    # t = api.update_status(tweet)
    t = api.update_status_with_media(tweet, project + '/md_core/tw/a.png')
    print(t)
    # ---
    dataid = getattr(t, 'id')
    if dataid is not None:
        print(dataid)
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
# ---
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
            if itemu.lower().strip() in ['xx', 'x']:
                continue
            vaild_links.append(itemu)
    # ---
    vaild_links = list(set(vaild_links))
    # ---
    print(f'len of vaild_links: {len(vaild_links)}')
    # ---
    if 'XX' in vaild_links:
        vaild_links.remove('XX')
    # ---
    return vaild_links


def get_done():
    # ---
    jsj = []
    # ---
    if not os.path.exists(json_file):
        print(f'create new file {json_file}')
        with codecs.open(json_file, "w", encoding="utf-8") as ffe:
            json.dump(['XX'], ffe)
        ffe.close()
        return jsj
    # ---
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


def start_md():
    done = get_done()
    # ---
    print(f'len of done: {len(done)}')
    # ---
    links = get_links()
    # ---
    print(f'len of links: {len(links)}')
    # ---
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
    article = link.replace("_", " ")
    link = 'https://mdwiki.org/wiki/' + link.replace(" ", "_")
    tweet = f'''Today article is: {article}\n{link}'''
    # ---
    print(f'tweet: {tweet}')
    # ---
    if 'notw' in sys.argv:
        return
    # ---
    u = auth(tweet, link=link)
    # ---
    if u == True:
        done.append(article)
        with codecs.open(json_file, "w", encoding="utf-8") as ii:
            json.dump(done, ii)
            print('json.dump(done, ii)')
        ii.close()

        # ---


# ---
if 'test' in sys.argv:
    print('test!')
    auth('test!')
else:
    start_md()
# ---
