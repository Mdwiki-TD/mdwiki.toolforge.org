'''
بوت لإضافة
جدول old
إلى جميع ملفات جسون في
مجلد json_en


python3.10 core8/pwb.py prior/add_old new

python3.10 core8/pwb.py prior/add_old

python3 core8/pwb.py prior/add_old new  -file:en_1.json
python3 core8/pwb.py prior/add_old new  -file:en_2.json
python3 core8/pwb.py prior/add_old new  -file:en_3.json
python3 core8/pwb.py prior/add_old new  -file:en_4.json
python3 core8/pwb.py prior/add_old new  -file:en_5.json
python3 core8/pwb.py prior/add_old new  -file:en_6.json
python3 core8/pwb.py prior/add_old new  -file:en_7.json
python3 core8/pwb.py prior/add_old new  -file:en_8.json
python3 core8/pwb.py prior/add_old new  -file:en_9.json
python3 core8/pwb.py prior/add_old new  -file:en_10.json
python3 core8/pwb.py prior/add_old new  -file:en_11.json
python3 core8/pwb.py prior/add_old new  -file:en_12.json
python3 core8/pwb.py prior/add_old new  -file:en_13.json
python3 core8/pwb.py prior/add_old new  -file:en_14.json
'''
import sys
import os
import json

# ---
from prior import get_them
from mdpy import printe

# ---
project = '/data/project/mdwiki/'
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
project += '/md_core/prior'
project_js_new = f'{project}/json_en/'
# ---


class PriorAddOld:
    def __init__(self):
        self.all_file = []

    def run(self):
        p = 0
        for filename in os.listdir(project_js_new):
            if filename.endswith('.json'):
                p += 1
                self.all_file.append(filename)
                print(f'jsub -N p{p} python3 core8/pwb.py prior/add_old -file:{filename}')
        # ---
        file_to = ''
        # ---
        for arg in sys.argv:
            arg, _, value = arg.partition(':')
            if arg == '-file':
                file_to = value
                break
        # ---
        if file_to in self.all_file:
            self.all_file = [file_to]
            print(f'file: {file_to}')
        else:
            print(f'no file: {file_to}')
            return
        # ---
        for filename in self.all_file:
            filename = os.path.join(project_js_new, filename)
            # ---
            print(f'filename: {filename}..')
            # ---
            data = json.load(open(filename))
            # ---
            data_new = data
            # ---
            len_all = len(data)
            n = 0
            # ---
            for title, tab in data.items():
                # ---
                n += 1
                # ---
                print(f'page: {n}/{len_all}')
                # ---
                title2 = tab['en']
                # ---
                if 'new' in sys.argv and tab.get('old', {}) != {}:
                    ext = tab['old'].get('extlinks', [])
                    ref = tab['old'].get('refsname', [])
                    lead_ex = tab['old'].get('lead', {}).get('extlinks', [])
                    lead_re = tab['old'].get('lead', {}).get('refsname', [])
                    # ---
                    if len(ext) > 0 and len(ref) > 0 and len(lead_ex) > 0 and len(lead_re) > 0:
                        # ---
                        continue
                # ---
                old = get_them.get_old(title2)
                # ---
                tab['old'] = {}
                tab['old']['extlinks'] = old.extlinks
                tab['old']['refsname'] = old.refsname
                tab['old']['lead'] = old.lead
                # ---
                lenex1 = str(len(old.extlinks)).ljust(4)
                lenre1 = str(len(old.refsname)).ljust(4)
                # ---
                lenex_lead1 = str(len(old.lead['extlinks'])).ljust(4)
                lenre_lead1 = str(len(old.lead['refsname'])).ljust(4)
                # ---
                printe.output(f'p0/\told\t\t{lenex1} extlinks, {lenre1} refsname')
                printe.output(f'p0/\told\t\t{lenex_lead1} lead_extlinks, {lenre_lead1} lead_refsname')
                # ---
                data_new[title] = tab
        # ---
        if data_new == data:
            print(f'no change: {filename}')
        else:
            # ---
            json.dump(data_new, open(filename, 'w'))


# ---
pao = PriorAddOld()
pao.run()
# ---
