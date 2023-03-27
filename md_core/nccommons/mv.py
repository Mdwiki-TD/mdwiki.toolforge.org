#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
python3 pwb.py nccommons/mv
"""
#
# (C) Ibrahem Qasim, 2023
#
#---
import re
import sys
import json
import time
import os
import codecs
import pywikibot
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project):  project = "I:/mdwiki/md_core/nccommons"
#---
from mdpy import mdwiki_api
#---
cats = mdwiki_api.Get_Newpages(limit="max", namespace="14", rcstart="", user='Fæ')
#---
pywikibot.output(f'len of cats: {len(cats)}')
#---
from nccommons import api

for cat in cats:
    text = mdwiki_api.GetPageText(cat)
    new = api.create_Page(text, cat)
    break