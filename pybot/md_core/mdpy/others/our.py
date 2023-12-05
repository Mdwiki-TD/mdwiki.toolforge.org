#!/usr/bin/python3
"""

python3 core8/pwb.py mdpy/our

"""
#
# (C) Ibrahem Qasim, 2022
#
#
from pywikibot.comms import http
import json
import pywikibot

import sys

# ---
from mdpy.bots import txtlib2
from mdpy import printe
from mdpy.bots import mdwiki_api

# ---
import os

project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
public_html = project + '/public_html'
# ---
values = {}


def fix_p(title, text, param):
    uu = '{{ourworldindatamirror|%s}}' % param
    nn = f'<templatestyles src="Owid/styles.css"/><ourworldindatamirror>{param}</ourworldindatamirror>'
    newtext = text
    if text.find(uu) != -1:
        newtext = text
        newtext = newtext.replace(uu, nn)
        # ---
    return newtext


def work(title):
    # ---
    global values
    # ---
    text = mdwiki_api.GetPageText(title)
    # ---
    ingr = txtlib2.extract_templates_and_params(text)
    # ---
    pas = ''
    # ---
    newtext = text
    # ---
    for temp in ingr:
        # ---
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        # ---
        if namestrip.lower() == 'ourworldindatamirror':
            # ---
            pas += str(params) + '\n'
            # ---
            param = params.get(1) or params.get('1') or ''
            # ---
            if param == '' and len(params.keys()) == 1:
                pp = list(params.keys())[0]
                vv = params[pp]
                if pp.find('https') != -1 and vv.find('Webarchive') != -1:
                    param = pp + '=' + vv
                    # ---
                    newtext = fix_p(title, newtext, param)
                    # ---
            # ---
            param = param.strip()
            if param not in values:
                values[param] = [title]
            else:
                values[param].append(title)
    # ---
    if newtext != text:
        sa = True
        # ---
        if 'ask' in sys.argv:
            sa = False
            pywikibot.showDiff(text, newtext)
            sas = pywikibot.input(f'<<lightyellow>>API: Do you want to accept these changes? ([y]es, [N]o, [a]ll): for page {title}')
            if sas in ['', 'y']:
                sa = True
        # ---
        if sa:
            vav = mdwiki_api.page_put_new(newtext, 'fix ourworldindatamirror template.', title)
    # ---
    printe.output(pas)


# ---
# ---
errors = {}


def check_urls(urls):
    global errors
    for u in urls:
        url = u
        url = url.split('{{')[0].strip()
        if url.find('http') == -1:
            url = 'https://owidm.wmcloud.org/grapher/' + url
        # ---
        print(url)
        # ---
        req = http.fetch(url)
        # ---
        if 500 <= req.status_code < 600:
            printe.output(f'<<lightred>> received {req.uri} status from {req.status_code}')
            errors[u] = True


def make_log(dad):
    lists = {x: len(z) for x, z in dad.items()}
    # ---
    global errors
    # ---
    sorts = sorted(lists.items(), key=lambda x: x[1], reverse=True)
    # ---
    text = ''
    text_error = ''
    # ---
    for x, va in sorts:
        ta = f'\n== {x} ==\n'  # .replace('https://ourworldindata.org/grapher/','')
        # ---
        vav = errors.get(x, False)
        # ---
        ta += 'used %d times.\n' % va
        # ---
        if x.find('https') == -1:
            ta += f"[https://owidm.wmcloud.org/grapher/{x.replace(' ', '%20')} {x}]"
        else:
            ta += x
        # ---
        ta += '\n=== pages ===\n%s' % "\n".join([f"*[[{s}]]" for s in dad[x]])
        # print(ta)
        # ---
        if vav:
            text_error += ta
        else:
            text += ta
    # ---
    te = '= errors = \n' + text_error + '\n'
    te += '= no errors = \n' + text + '\n'
    # ---
    mdwiki_api.page_put(newtext=te, summary='update', title='User:Mr. Ibrahem/Ourworldindatamirror', diff=False)


def main():
    nn = ''
    # ---
    global values
    # ---
    if 'read' in sys.argv:
        list = mdwiki_api.Get_template_pages("Template:Ourworldindatamirror", namespace="0", limit="max")
        # ---
        num = 0
        # ---
        for page in list:
            num += 1
            # ---
            printe.output(f'<<lightyellow>> work {num}/{len(list)} page: {page}')
            # ---
            work(page)
            # ---
            if '50' in sys.argv and num > 50:
                break
        # ---
        with open(project + '/md_core/mdpy/our.json', 'w') as f:
            json.dump(values, f)
        # ---
    else:
        with open(project + '/md_core/mdpy/our.json') as f:
            values = json.load(f)
    # ---
    make_log(values)

    # ---


if __name__ == "__main__":
    main()
# ---
