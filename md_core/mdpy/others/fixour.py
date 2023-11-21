#!/usr/bin/python3
"""

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import re

# ---
numbers = {1: 20000, 'done': 0}
# ---
import os

project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
public_html = project + '/public_html'
# ---
from new_api.mdwiki_page import MainPage, NEW_API

api_new = NEW_API('www', family='mdwiki')
api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# pages   = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)
# ---
'''
page      = MainPage(title, 'www', family='mdwiki')
exists    = page.exists()
if not exists: return
# ---
text        = page.get_text()
save_page   = page.save(newtext='', summary='', nocreate=1, minor='')
# ---
'''


def work(title):
    # ---
    page = MainPage(title, 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        return
    # ---
    text = page.get_text()
    # <templatestyles src="Owid/styles.css"/><ourworldindatamirror>cumulative-covid-cases-region</ourworldindatamirror>
    # ---
    regref = re.compile(r'<templatestyles\s*src="Owid/styles.css"\s*/\s*>\s*<ourworldindatamirror>(?P<content>.*?)</ourworldindatamirror>', re.IGNORECASE | re.DOTALL)
    # ---
    newtext = text
    # ---
    for match in regref.finditer(text):
        # ---
        aaa = match.group()
        # ---
        content = match.group('content')
        if not content.strip():
            continue
        # ---
        content = content.strip()
        # ---
        if newtext.find(content) != -1:
            newtext = newtext.replace(aaa, '{{ourworldindatamirror|%s}}' % content)
    # ---
    sus = 'fix ourworldindatamirror'
    # ---
    if newtext != text:
        numbers['done'] += 1
        # ---
        save_page = page.save(newtext=newtext, summary=sus)


def main():
    nn = ''
    # ---
    list = api_new.Get_All_pages(start='COVID', namespace="0", limit="max", apfilterredir='', limit_all=0)
    # ---
    num = 0
    # ---
    for page in list:
        num += 1
        # ---
        if numbers['done'] >= numbers[1]:
            break
        # ---
        work(page)

    # ---


# python py/replace1.py
# ---
if __name__ == "__main__":
    main()
# ---
