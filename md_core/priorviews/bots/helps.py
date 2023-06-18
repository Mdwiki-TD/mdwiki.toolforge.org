'''

'''
import sys
import pywikibot
import json
import os
from urllib.parse import urlencode
import codecs
import datetime
from datetime import timedelta
#---
Dir = os.path.dirname(os.path.abspath(__file__))
#---
def views_url(title, lang, view):
    params = {
        'project': f"{lang}.wikipedia.org",
        'platform': 'all-access',
        'agent': 'all-agents',
        'start': "2015-07-01",
        'redirects': '0',
        'pages': title
    }
    d_end   = datetime.datetime.utcnow() - timedelta(days = 1)
    d_end   = d_end.strftime('%Y-%m-%d')
    params['end'] = d_end
    params = urlencode(params)
    url_views = f"https://pageviews.wmcloud.org/?{params}"

    view = f'[{url_views} {view:,}]'
    return view
                