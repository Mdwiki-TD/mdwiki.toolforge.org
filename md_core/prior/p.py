'''

write code to read page in en.wikipedia.org using API, then create list with all links in the page.
title: WikiProjectMed:List/Prior
links like [[example]]
'''
import sys
import os
# get the directory name of the current script
filepath = os.path.abspath(__file__)
# print(f'filepath: {filepath}')
current_dir = os.path.dirname(filepath)
# print(f'current_dir: {current_dir}')
# create a new directory with the desired name
new_dir = os.path.join(current_dir, '..', 'mdpy')
# print(f'new_dir: {new_dir}')
# os.makedirs(new_dir, exist_ok=True)
sys.path.append(new_dir)
from mdpy import mdwiki_api
# mdwiki_api.post(params)
# mdwiki_api.wordcount(title, srlimit='30')
# mdwiki_api.purge(title)
# mdwiki_api.page_put(NewText, summary, title, time_sleep="", minor="")
# mdwiki_api.page_putWithAsk(oldtext, NewText, summary, title, Ask, minor="")
# mdwiki_api.create_Page(text, summary, title, ask, sleep=0, duplicate4="")
# mdwiki_api.Add_To_Bottom(appendtext, summary, title, ask)
# mdwiki_api.Add_To_Head(prependtext, summary, title, Ask)
# mdwiki_api.move(From, to, reason)
# mdwiki_api.Get_Newpages(limit="max", namespace="0", rcstart="")
# mdwiki_api.Get_UserContribs(user, limit="max", namespace="*", ucshow="")
# mdwiki_api.GetPageText(title)
# mdwiki_api.Get_All_pages(start, limit="max", namespace="*", apfilterredir='')
# mdwiki_api.Search(title, ns="", offset='', srlimit="max", RETURN_dict=False, addparams={})
# mdwiki_api.import_page(title)
# mdwiki_api.Get_page_links(title, namespace="*", limit="max")
# mdwiki_api.subcatquery(title, depth=0, ns="all", without_lang="", with_lang="", tempyes=[], limit=0)
# mdwiki_api.get_redirect(liste)
#---
title = "WikiProjectMed:List/Prior"
text  = mdwiki_api.GetPageText(title)
links = mdwiki_api.Get_page_links(title, namespace="*", limit="max")
print(links)