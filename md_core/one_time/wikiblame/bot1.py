'''

write code to read page in en.wikipedia.org using API, then create list with All links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]

python3 core8/pwb.py prior/p4 test
'''
import urllib.parse
import requests

# ---
session = requests.Session()


def get_url(url):
    try:
        html = session.get(url)
        return html.text
    except Exception as e:
        printe.output(f'except: {e}')
    return ''


def wikiblame(table):
    exampl_url = 'http://wikipedia.ramselehof.de/wikiblame.php?user_lang=en&lang=es&project=wikipedia&tld=org&article=Letrina+de+hoyo&needle=Till2014&skipversions=0&ignorefirst=0&limit=1500&offtag=22&offmon=7&offjahr=2023&searchmethod=int&order=desc&force_wikitags=on&user='
    endpoint = 'http://wikipedia.ramselehof.de/wikiblame.php'
    params = {'lang': table['lang'], 'project': 'wikipedia', 'tld': 'org', 'article': table['title'], 'needle': table['search'], 'skipversions': '0', 'ignorefirst': '0', 'limit': table.get('limit', '1500'), 'offtag': '22', 'offmon': '7', 'offjahr': '2023', 'searchmethod': 'int', 'order': 'desc', 'force_wikitags': 'on', 'user': table.get('user', '')}
    # ---
    url = endpoint + '?' + urllib.parse.urlencode(params)
    # ---
    html = get_url(url)
    # ---
    #
    # ---
