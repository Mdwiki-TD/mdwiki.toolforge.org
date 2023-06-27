#!/usr/bin/python
"""
#---
from mdpy.bots import open_url
# open_url.getURL(url)
# open_url.open_json_url(url)
#---
"""
#
# (C) Ibrahem Qasim, 2023
#
from mdpy import printe
from pywikibot import comms
import pywikibot
import traceback
import json
import re
import codecs
import time
import requests
import sys
sys.dont_write_bytecode = True
# ---
# ---


class classgetURL:
    def __init__(self, url):
        self.start = time.time()
        self.url = url
        self.html = ''

    def open_it(self):
        if self.url == '':
            printe.output('open_url.py: self.url == ""')
            return ''
        if 'printurl' in sys.argv:
            printe.output(f'getURL: {self.url}')

        try:
            # req = comms.http.fetch(self.url)
            req = requests.get(self.url)
            # ---
            if 500 <= req.status_code < 600:
                printe.output('received {0} status from {1}'.format(req.status_code, req.url))
                self.html = ''
            else:
                # ---
                self.html = req.text
        # ---
        except Exception as e:
            _Except_ions_ = [
                "Too long GET request",
                "HTTPSConnectionPool(host='en.wikipedia.org', port=443): Read timed out. (read timeout=45)",
                "('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))",
                '''('Connection aborted.', OSError("(104, 'ECONNRESET')"))''',
                '''HTTP Error 414: URI Too Long''',
                "HTTP Error 500: Internal Server Error",
            ]
            pywikibot.output('<<lightred>> Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
        # ---
        return self.html
# ---


def getURL(url, maxsleeps=0):
    bot = classgetURL(url)
    return bot.open_it()
# ---


def open_json_url(url, maxsleeps=0, **kwargs):
    bot = classgetURL(url)
    js_text = bot.open_it()
    # ---
    try:
        json1 = json.loads(js_text)
        return json1
    except Exception as e:
        pywikibot.output("Traceback (most recent call last):")
        pywikibot.output(traceback.format_exc())
        pywikibot.output(" CRITICAL:")
        return {}
    # ---
    return json1
# ---
