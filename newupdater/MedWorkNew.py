#!/usr/bin/env python
"""
python3 pwb.py newupdater/med Aspirin from_toolforge
python3 pwb.py newupdater/med Retinol from_toolforge

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
from drugbox import TextProcessor
from mv_section import move_External_links_section
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
lkj2 = r"(<!--\s*(?:Monoclonal antibody data|External links|Names*|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status)\s*-->)"
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
    bot2     = move_External_links_section(new_text)
    #---
    new_text     = bot2.get_new_text()
    #---
    new_text = re.sub(r'\n\s*\[\[Category', '\n[[Category', new_text, flags=re.DOTALL | re.MULTILINE)
    #---
    return new_text
#---
def test():
    #---
    # python3 pwb.py newupdater/MedWorkNew
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