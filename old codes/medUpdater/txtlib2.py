#!/usr/bin/python
#---*- coding: utf-8 -*-
"""
import txtlib2
# ingr = txtlib2.extract_templates_and_params(text)
# for temp in ingr: name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
"""
#
# (C) Ibrahem Qasim, 2021
# 
#
#---
import sys
sys.dont_write_bytecode = True
#---
import os
u_path = '/data/project/mdwiki/core/'
if os.path.exists(u_path):
    sys.path.append(os.path.abspath(u_path))
#---
try:
    import wikitextparser
except ImportError:
    try:
        import mwparserfromhell as wikitextparser
    except ImportError:
        # print required because pywikibot is not imported completely
        raise ImportError("""
Pywikibot is missing a MediaWiki markup parser which is necessary.
Please update the required module with either

    pip install "mwparserfromhell>=0.5.0"

or

    pip install "wikitextparser>=0.47.5"
""") from None
#---
def extract_templates_and_params(text):
    #---
    result = []
    #---
    pra = wikitextparser
    #---
    parser_name = pra.__name__
    parsed = pra.parse(text)
    if parser_name == 'wikitextparser':
        templates = parsed.templates
        arguments = 'arguments'
    else:
        templates = parsed.ifilter_templates(matches=lambda x: not x.name.lstrip().startswith('#'), recursive=True)
        arguments = 'params'
    #---
    for template in templates:
        #---
        params = {}
        for param in getattr(template, arguments):
            value = str(param.value)
            key = str(param.name)
            key = key.strip()
            params[key] = value
        #---
        name = template.name.strip()
        #---
        if parser_name == 'wikitextparser':
            name = str(template.normal_name()).strip()
            pa_item = template.string
        else:
            pa_item = template.__str__()
        #---
        namestrip = name
        #---
        ficrt = { 'name': "قالب:" + name, 'namestrip': namestrip, 'params' : params, 'item' : pa_item }
        #---
        result.append(ficrt)
    #---
    return result
#---