#!/usr/bin/env python
"""
python3 pwb.py medUpdater/med -page:Aspirin ask 
python3 pwb.py medUpdater/med -page:Retinol ask 

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import sys
import os
import codecs
#---
import txtlib2
#---
from bots import resources
# if __name__ == "__main__":  from bots import resources_new as resources
#---
resources.extract_templates_and_params = txtlib2.extract_templates_and_params
#---
from bots.data_legal    import add_Legal_data
from bots.names         import add_Names
from bots.Chemical      import add_Chemical_data, formola_params
from bots.Clinical      import add_Clinical
from bots.Physiological import Physiological_data
from bots.Pharmaco      import add_Pharmacokinetic_data
from bots.External      import add_External_links
from bots.old_params    import rename_params
#---
def printn(s):
    return
#---
project = "/data/project/mdwiki/"
#---
if not os.path.isdir(project): project = "/mdwiki"
#---
lkj = r"<!--\s*(Monoclonal antibody data|External links|Names*|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers)\s*-->"
#---
lkj2 = r"(<!--\s*(?:Monoclonal antibody data|External links|Names*|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers)\s*-->)"
#---
def aligns(text):
    #---
    newtext = text
    params = {}
    #---
    for temp in txtlib2.extract_templates_and_params(newtext):
        #---
        name, namestrip, _params, txt = temp["name"], temp["namestrip"], temp["params"], temp["item"]
        #---
        if txt.strip() == newtext.strip():
            params = _params
            break
        #---
    #---
    for p in params:
        #---
        if p.strip() in formola_params: continue
        #---
        newparam = '| %s' % p.ljust(18) + '='
        newtext = re.sub(r'\s*(\|\s*%s\s*\=\s*)' % p.strip(), '\n' + newparam, newtext)
    #---
    for param in params:
        #---
        if param.strip() in formola_params: continue
        #---
        newtext = re.sub(r'\s*(\|\s*%s\s*\=)' % param.strip(), '\n\g<1>', newtext)
    #---
    newtext = re.sub(r'\s*\}\}\s*$', '\n}}', newtext)
    #---
    return newtext
#---
def work_on_text(title, text):
    #---
    new_text = text
    #---
    new_text = resources.move_resources(new_text, title, lkj=lkj, lkj2=lkj2)
    #---
    drugbox = ""
    #---
    drugbox_params = {}
    #---
    ingr = txtlib2.extract_templates_and_params(new_text)
    #---
    for temp in ingr:
        #---
        namestrip, params, txt = temp["namestrip"], temp["params"], temp["item"]
        #---
        if namestrip.lower() in ["drugbox", "infobox drug"] and drugbox == "" :
            drugbox = txt
            #---
            drugbox_params = params
            #---
        elif namestrip.lower() in [ "infobox medical condition (new)","infobox medical condition" ] :
            printn( "*find temp:[%s]." % namestrip )
    #---
    drug_box_new = drugbox
    #---
    drug_box_new = re.sub(r"<!--\s*Identifiers\s*-->","", drug_box_new, flags=re.IGNORECASE)
    #---
    Names_section = ""
    #--- 
    # add names section
    drug_box_new, Names_section = add_Names(drug_box_new, drugbox_params)
    #---
    Names_section = "<!-- Names -->\n" + re.sub(lkj2, '', Names_section)
    #---
    printn(f'Names_section: {Names_section}')
    #---
    # add Clinical data
    drug_box_new = add_Clinical(drug_box_new, drugbox_params , Names_section)
    #---
    # add Physiological data section
    drug_box_new = Physiological_data(drug_box_new, drugbox_params)
    #---
    # add External links
    drug_box_new = add_External_links(drug_box_new, drugbox_params, lkj=lkj)
    #---
    # add Legal data
    drug_box_new = add_Legal_data(drug_box_new, drugbox_params)
    #---
    # add Pharmacokinetic data
    drug_box_new = add_Pharmacokinetic_data(drug_box_new, drugbox_params)
    #---
    # add Chemical data
    drug_box_new = add_Chemical_data(drug_box_new, drugbox_params)
    #---
    #---
    drug_box_new = drug_box_new.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
    drug_box_new = drug_box_new.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
    #---
    drug_box_new = aligns(drug_box_new)
    #---
    drug_box_new = re.sub(rf'\s*{lkj2}\s*', "\n\n\g<1>\n", drug_box_new, flags=re.DOTALL)
    #---
    drug_box_new = re.sub(f'{lkj}', "<!-- \g<1> -->", drug_box_new)
    #---
    drug_box_new = re.sub(r'\n\s*\n\s*[\n\s]+', '\n\n', drug_box_new, flags=re.DOTALL|re.MULTILINE)
    #---
    new_text = new_text.replace(drugbox, drug_box_new)
    #---
    new_text = re.sub(r"\{\{drug resources\s*\<\!", "{{drug resources\n<!", new_text, flags=re.IGNORECASE)
    #---
    return new_text
#---
def test():
    #---
    # python3 pwb.py medUpdater/MedWork
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