'''
# ---
from priorviews.bots import helps
# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# helps.talk_url(lang, user, labl)
# helps.dump_data(file, data)
# ---
'''
import sys
import json
from pathlib import Path
import re
import codecs
import datetime
from urllib.parse import urlencode
from datetime import timedelta

# ---
from mdpy import printe

Dir = Path(__file__).parent


def views_url(title, lang, view):
    params = {
        'project': f"{lang}.wikipedia.org",
        'platform': 'all-access',
        'agent': 'all-agents',
        'start': "2015-07-01",
        'redirects': '0',
        'pages': title
    }
    d_end = datetime.datetime.utcnow() - timedelta(days=1)
    d_end = d_end.strftime('%Y-%m-%d')
    # params['end'] = d_end
    params['end'] = "2023-06-01"
    params = urlencode(params)
    url_views = f"https://pageviews.wmcloud.org/?{params}"

    view = f'[{url_views} {view:,}]'
    return view


def isv(comment):
    # ---
    comment = comment.lower()
    # ---
    if comment.find('translators without borders') != -1:
        print(f' <<yellow>> translators without borders: {comment}')
        return True
    if comment.find('(twb)') != -1:
        print(f' <<yellow>> (twb): {comment}')
        return True
    # ---
    if comment.find("|user:mr. ibrahem/") != -1:
        print(f' <<yellow>> |user:mr. ibrahem/ {comment}')
        return True
    # ---
    return False


def is_ip(user):
    # skip user match ip address
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', user):
        print(f' <<yellow>> skip user match ip address: {user}')
        return True
    # ---
    # skip user match ip address like: 2001:569:F867:EE00:1540:D99D:3F7:3EAE
    if re.match(r'^(?:(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}|::(?:[A-Fa-f0-9]{1,4}:){0,5}[A-Fa-f0-9]{1,4}|(?:[A-Fa-f0-9]{1,4}:){1,2}:|:(?::[A-Fa-f0-9]{1,4}){1,6}|(?:[A-Fa-f0-9]{1,4}:){1,6}:|:(?::[A-Fa-f0-9]{1,4}){1,7}|(?:[A-Fa-f0-9]{1,4}:){1,7}:|:(?::[A-Fa-f0-9]{1,4}){1,8}|(?:[A-Fa-f0-9]{1,4}:){1,8}:)$', user):
        print(f' <<yellow>> skip user match ip address: {user}')
        return True
    # ---
    return False


def talk_url(lang, user, labl):
    old = f'[[w:{lang}:User talk:{user}|{user}]]'
    # --
    pas = {
        'title': f'User_talk:{user}',
        'action': 'edit',
        'section': 'new'
    }
    url = f"//{lang}.wikipedia.org/w/index.php?" + urlencode(pas)
    # ---
    return f'[{url} {labl}]'


def dump_data(file, data):
    printe.output(f'<<green>> dump_data() file:{file}.')
    try:
        with codecs.open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except KeyboardInterrupt:
        printe.output('<<red>> keyboard interrupt sys.exit()')
        # ---
        with codecs.open(f'{file}_1', 'w', encoding='utf-8') as f:
            json.dump(data, f)
        # ---
        sys.exit()
    except Exception as e:
        printe.output(f'<<red>> dump Error: {e}')


# ---
