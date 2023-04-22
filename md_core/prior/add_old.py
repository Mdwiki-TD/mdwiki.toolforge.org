'''
'''
import sys
import os
import re
import json
import pywikibot
import codecs
#---
from prior import get_them
from mdpy import printe
#---
project = '/mnt/nfs/labstore-secondary-tools-project/mdwiki'
#---
if not os.path.isdir(project): project = '/mdwiki'
#---
project += '/md_core/prior'
#---
project_jsonnew = f'{project}/jsonnewen/'
#---
for filename in os.listdir(project_jsonnew):
    if filename.endswith('.json'):
        #---
        filename = os.path.join(project_jsonnew, filename)
        #---
        print(f'filename: {filename}..')
        #---
        data = json.load(open(filename, 'r'))
        #---
        data_new = data
        #---
        len_all = len(data)
        n = 0
        #---
        for title, tab in data.items():
            tab['old'] = {}
            #---
            n += 1
            #---
            print(f'page: {n}/{len_all}')
            #---
            title2 = tab['en']
            #---
            old = get_them.get_old(title2)
            tab['old'] = {}
            tab['old']['extlinks'] = old.extlinks
            tab['old']['refsname'] = old.refsname
            tab['old']['lead'] = old.lead
            #---
            lenex1 = str(len(old.extlinks)).ljust(4)
            lenre1 = str(len(old.refsname)).ljust(4)
            #---
            lenex_lead1 = str(len(old.lead['extlinks'])).ljust(4)
            lenre_lead1 = str(len(old.lead['refsname'])).ljust(4)
            #---
            printe.output(f'p0/\told\t\t{lenex1} extlinks, {lenre1} refsname')
            printe.output(f'p0/\told\t\t{lenex_lead1} lead_extlinks, {lenre_lead1} lead_refsname')
            #---
            data_new[title] = tab
        #---
        json.dump(data_new, open(filename, 'w'))
#---