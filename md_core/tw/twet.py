#!/usr/bin/python3
"""

@WikiProjectMed

python twet.py test

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
# ---
# ---
# ---
# ---
'''
def auth22(tweet):
    # ---
    payload = {"text": tweet }
    # ---
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    ooo = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = ooo.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
    # ---
    data = getattr(json_response, 'data')
    if data and getattr(data, 'id') != None:
        print(data['id'])
        return True


def auth(tweet):
    # ---
    api = twitter.Api(consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token,
            access_token_secret=access_token_secret,
            base_url = 'https://api.twitter.com/2')
    # ---
    #print(api.VerifyCredentials())
    # ---
    #try:
        #print(api.VerifyCredentials())
    #except Exception as e:
        #print( f'except {e}' )
    # ---
    u = api.PostUpdates(tweet)
    # ---
    return u
# ---
from TwitterAPI import TwitterAPI


def auth(twet):
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
    r = api.request('statuses/update', {'status': twet })
    if r.status_code == 200:
        print('SUCCESS')
    else:
        print('FAILURE')


def auth(twet):
    BEARER = twitter.oauth2_dance(consumer_key, consumer_secret)

    t = twitter.Twitter(auth=twitter.OAuth2(bearer_token=BEARER))

    # Now work with Twitter
    z = t.search.tweets(q='yemen test!')
    print(z)
    api = twitter.OAuth2(consumer_key, consumer_secret, access_token, access_token_secret)
    r = api.request('statuses/update', {'status': twet })
    if r.status_code == 200:
        print('SUCCESS')
    else:
        print('FAILURE')
    # ---
# ---
'''


def auth(twet):
    # client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret)
    u = client.create_tweet(text=twet)
    # ---
    # auth = tweepy.OAuth2AppHandler(consumer_key, consumer_secret)
    # api = tweepy.API(auth)


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


def start_md():
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
    article = link.replace("_", " ")
    link = 'https://mdwiki.org/wiki/' + link.replace(" ", "_")
    tweet = f'''Today article is: {article}\n{link}'''
    # ---
    u = auth(tweet)
    # ---
    if u == True:
        done.append(link)
        with codecs.open(json_file, "w", encoding="utf-8") as ii:
            json.dump(done, ii)
        ii.close()

        # ---


# ---
if 'test' in sys.argv:
    print('test!')
    auth('test!')
else:
    start_md()
# ---
