#!/usr/bin/env python
"""
python3 pwb.py medUpdater/med Aspirin from_toolforge
python3 pwb.py medUpdater/med Retinol from_toolforge

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import sys
sys.dont_write_bytecode = True
import os
import codecs
import wikitextparser as wtp
#---
import resources_new
from bots.old_params    import rename_params
#---
def printn(s):
    return
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project): project = "/mdwiki"
#---
lkj = r"<!--\s*(Monoclonal antibody data|External links|Names*|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers)\s*-->"
#---
lkj2 = r"(<!--\s*(?:Monoclonal antibody data|External links|Names*|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status)\s*-->)"
#---
from bot_params import all_params, params_to_add, params_placeholders, all_formola_params
#---
class TextProcessor:
    def __init__(self, text):
        self.text = text
        self.new_text = text
        
        self.drugbox_params = {}
        self.all_drugbox_params = {}
        self.olddrugbox = ""
        self.drugbox_title = ""
        self.newdrugbox = ""
        #---
        self.params_done_lowers = []
        #---
        self.run()
    
    def get_new_temp(self):
        return self.newdrugbox
    
    def get_old_temp(self):
        return self.olddrugbox
    
    def get_txt_params(self, text):
        #---
        txt = ''
        params = {}
        parsed = wtp.parse(text)
        #---
        for template in parsed.templates:
            #---
            name = str(template.normal_name()).strip()
            #---
            if name.lower() in ["infobox medical condition (new)", "infobox medical condition"]:
                printn("*find temp:[%s]." % name)
                continue
            #---
            if name.lower() in ["drugbox", "infobox drug"]:
                #---
                self.drugbox_title = name
                #---
                txt = template.string
                #---
                params = {str(param.name).strip(): str(param.value) for param in template.arguments}
                #---
                break
        #---
        return txt, params
    
    def run(self):
        #---
        self.olddrugbox, self.drugbox_params = self.get_txt_params(self.text)
        #---
        if self.olddrugbox == "": return
        #---
        drugbox2 = re.sub(lkj2, '', self.olddrugbox)
        #---
        drugbox2, params = self.get_txt_params(drugbox2)
        #---
        self.drugbox_params     = params
        self.all_drugbox_params = params
        #---
        # create self.newdrugbox
        self.new_temp()
        #---

    def add_section(self, section):
        if section == "": return
        #---
        text = '\n\n' + section
        #---
        self.newdrugbox += text
    
    def get_combo(self):
        #---
        combo_titles = {
            "mab" : "Monoclonal antibody data",
            "vaccine" : "Vaccine data",
            "combo" : "Combo data"
        }
        #---
        Type = self.drugbox_params.get("type", "").lower().strip()
        #---
        empty = False
        if re.match(r"<!--\s*empty\s*-->", Type): empty = True
        #---
        # remove html coments
        Type = re.sub(r"<!--.*?-->", "", Type)
        #---
        sec_title = combo_titles.get(Type) or "| type = mab / vaccine / combo"
        #---
        all_combo = all_params['combo']['all']
        #---
        if Type in combo_titles:
            #---
            params = all_params['combo'][Type]
            #---
            for p in all_combo: 
                if not p in params: params.append(p)
            #---
            all_combo = params
            #---
        #---
        if empty: sec_title = ''
        #---
        sec_params = all_combo
        #---
        return sec_title, sec_params

    def get_chemical(self):
        #---
        sec_params = all_params.get('chemical', {})
        #---
        sec_text = ""
        #---
        n = 0
        #---
        for x in all_formola_params:
            #---
            if not x in self.drugbox_params: continue
            #---
            x_val = self.drugbox_params.get(x, '').strip()
            #---
            self.params_done_lowers.append(x.strip().lower())
            #---
            n += 1
            #---
            vv = f"| {x}={x_val} "
            #---
            if n % 5 == 0:  vv += "\n"
            #---
            sec_text += vv
        #---
        # remove all_formola_params from sec_params
        for p in all_formola_params:
            if p in sec_params: 
                sec_params.remove(p)
        #---
        return sec_text, sec_params
    #---
    def create_section(self, sectionname):
        #---
        sections_titles = {
            "first": "",
            "combo": "",
            "names": "Names",
            "gene": "GENE THERAPY",
            "clinical": "Clinical data",
            "external": "External links",
            "legal": "Legal data",
            "physiological": "Physiological data",
            "pharmacokinetic": "Pharmacokinetic data",
            "chemical": "Chemical and physical data",
            "last": ""
        }
        #---
        sec_title = sections_titles[sectionname]
        #---
        sec_params = all_params.get(sectionname, [])
        add_params = params_to_add.get(sectionname, [])
        #---
        if sectionname == "combo":
            sec_title, sec_params = self.get_combo()
        #---
        section_title = ''
        if sec_title != '':
            section_title = f'<!-- {sec_title} -->'
        #---
        if sectionname in ['first', 'last']:    section_title = ''
        #---
        sec_text = ''
        #---
        if sectionname == "chemical":
            sec_text, sec_params = self.get_chemical()
        #---
        if sectionname == "last":
            sec_params = [ x for x in self.drugbox_params.keys() if x.lower().strip() not in self.params_done_lowers ]
        #---
        for p in sec_params:
            p = p.strip()
            #---
            if p in self.drugbox_params or p in add_params:
                p_value = self.drugbox_params.get(p, '').strip()
                #---
                if p_value.strip() == '':
                    p_value = params_placeholders.get(p, '').strip()
                #---
                p2 = p.ljust(18)
                #---
                self.params_done_lowers.append(p.lower())                
                #---
                p_v = f'\n| {p2}={p_value}'
                #---
                sec_text += p_v
                #---
        #---
        if sec_text != '' and section_title != '':
            sec_text = f'{section_title}\n{sec_text}'
        #---
        return sec_text
        #---
    
    def new_temp(self):
        #---
        self.newdrugbox = '{{' + self.drugbox_title
        #---
        first_section = self.create_section('first')
        self.add_section(first_section)
        #---
        combo_section = self.create_section('combo')
        self.add_section(combo_section)
        #---
        names_section = self.create_section('names')
        self.add_section(names_section)
        #---
        GENE_section = self.create_section('gene')
        self.add_section(GENE_section)
        #---
        Clinical_section = self.create_section('clinical')
        self.add_section(Clinical_section)
        #---
        External_links_section = self.create_section('external')
        self.add_section(External_links_section)
        #---
        Legal_section = self.create_section('legal')
        self.add_section(Legal_section)
        #---
        Physiological_section = self.create_section('physiological')
        self.add_section(Physiological_section)
        #---
        Pharmacokinetic_section = self.create_section('pharmacokinetic')
        self.add_section(Pharmacokinetic_section)
        #---
        Chemical_section = self.create_section('chemical')
        self.add_section(Chemical_section)
        #---
        last_section = self.create_section('last')
        self.add_section(last_section)
        #---
        self.newdrugbox += '\n}}'    
#---
def work_on_text(title, text):
    #---
    new_text = text
    #---
    new_text = rename_params(new_text)
    #---
    new_text = resources_new.move_resources(new_text, title, lkj=lkj, lkj2=lkj2)
    #---
    bot = TextProcessor(new_text)
    #---
    drugbox      = bot.get_old_temp()
    drug_box_new = bot.get_new_temp()
    #---
    if drugbox == '': return text
    #---
    drug_box_new = re.sub(rf'\s*{lkj2}\s*', "\n\n\g<1>\n", drug_box_new, flags=re.DOTALL)
    #---
    drug_box_new = re.sub(r'\n\s*\n\s*[\n\s]+', '\n\n', drug_box_new, flags=re.DOTALL|re.MULTILINE)
    #---
    drug_box_new = re.sub(r'{{(Infobox drug|Drugbox|drug resources)\s*\n*', '{{\g<1>\n', drug_box_new, flags=re.DOTALL|re.MULTILINE)
    #---
    # replace the old drugbox by newdrugbox
    new_text = new_text.replace(drugbox, drug_box_new)
    #---
    new_text     = re.sub(r"\{\{(Infobox drug|Drugbox|drug resources)\s*\<\!", "{{\g<1>\n<!", new_text, flags=re.IGNORECASE)
    #---
    return new_text
#---
def test():
    #---
    # python3 pwb.py medUpdater/MedWorkNew
    import pywikibot
    #---
    dir = os.path.dirname(os.path.abspath(__file__))
    #---
    text = codecs.open(os.path.join(dir, "bots/resources.txt"), "r", "utf-8").read()
    newtext = work_on_text("test", text)
    #---
    pywikibot.showDiff(text, newtext)
    #---
    codecs.open(os.path.join(dir, "bots/resources_new.txt"), "w", "utf-8").write(newtext)
    #---
#---
if __name__ == "__main__":
    #---
    test()