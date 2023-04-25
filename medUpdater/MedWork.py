#!/usr/bin/env python

"""
#!/usr/bin/python
python3 pwb.py medUpdater/med -page:Aspirin ask 

python pwb.py medUpdater/med -page:Aspirin ask

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import sys
import os
#---
import txtlib2
#---
from bots.Remove import remove_cite_web, portal_remove
from bots.identifier import add_Identifiers
from bots.data_legal import add_Legal_data
from bots.names import add_Names
from bots.Chemical import add_Chemical_data
from bots.Clinical import add_Clinical
from bots.Physiological import Physiological_data
from bots.External import add_External_links
#---
def printn(s):
    return
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project): project = "/mdwiki"
#---
lkj = r"\<\!\-\-\s*(External links|Names|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*\=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers)\s*\-\-\>"
#---
lkj2 = r"(\<\!\-\-\s*(?:External links|Names|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*\=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status)\s*\-\-\>)"
#---
identifiers = [
    "CAS_number",
    "CAS_supplemental",
    "CAS_number_Ref",
    "CAS_number2",
    "CAS_supplemental2",
    "CAS_number2_Ref",
    "PubChem",
    "PubChem2",
    "PubChemSubstance",
    "PubChemSubstance2",
    "IUPHAR_ligand",
    "IUPHAR_ligand2",
    "DrugBank",
    "DrugBank_Ref",
    "DrugBank2",
    "DrugBank2_Ref",
    "ChemSpiderID",
    "ChemSpiderID_Ref",
    "ChemSpiderID2",
    "ChemSpiderID2_Ref",
    "UNII",
    "UNII_Ref",
    "UNIIRef",
    "UNII2",
    "UNII2_Ref",
    "KEGG",
    "KEGG_Ref",
    "KEGG2",
    "KEGG2_Ref",
    "ChEBI",
    "ChEBI_Ref",
    "ChEBI2",
    "ChEBI2_Ref",
    "ChEMBL",
    "ChEMBL_Ref",
    "ChEMBL2",
    "ChEMBL2_Ref",
    "NIAID_ChemDB",
    "NIAID_ChemDB2",
    #"type",
    "PDB_ligand",
    "PDB_ligand2",
    "DTXSID",
    "DTXSID2",
    "ATCvet",
    "ATC_prefix",
    "ATC_suffix",
    "ATC_supplemental",
    "ATC_prefix2",
    "ATC_suffix2",
    "ATC_supplemental2",
    ]
#----
def add_Pharmacokinetic_data( temptext , boxtable ) :
    temptext_new = temptext
    new_temp_replaced = temptext
    #---
    lic = [
        "bioavailability", 
        "protein_bound", 
        "metabolism", 
        "metabolites", 
        "elimination_half-life", 
        "excretion"
        ]
    #---
    new_param_sorted = ""
    #---
    for x in lic :
        new_val = ""
        if x in boxtable :
            new_param_sorted += "| %s = %s\n" % ( x , boxtable[x] )
        #---
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        #---
        if finde1:
            tt = finde1.group(1)
            faf = tt + boxtable.get(x,"").strip()
            if new_temp_replaced.find(faf) != -1 :
                new_temp_replaced = new_temp_replaced.replace( faf , new_val )#jjjj
            else:
                printn( "*+new_temp_replaced find (%s) == -1 ." % str([faf]) )
    #---
    new_temp_replaced = re.sub(r"(\<\!\-\-\s*Pharmacokinetic data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    before = re.search( r"(\<\!\-\-\s*Chemical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    before2 = re.search( r"(\<\!\-\-\s*Chemical and physical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    #---
    bd = ""
    if before :
        bd = before.group(1)
    elif before2 :
        bd = before2.group(1)
    #---
    if bd != "" and new_temp_replaced.find(bd) != -1 and new_param_sorted != "" :
        new_param_sorted = "\n\n<!-- Pharmacokinetic data -->\n" + new_param_sorted
        #---
        unde = new_param_sorted + "\n" + bd.strip()
        #---
        temptext_new = new_temp_replaced.replace( bd , unde  , 1 )
    #---
    return temptext_new
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
        newparam = '| %s=' % p.ljust(18)
        newtext = re.sub(r'\s*(\|\s*%s\s*\=\s)' % p.strip(), '\n' + newparam, newtext)
    #---
    for param in params:
        newtext = re.sub(r'\s*(\|\s*%s\s*\=)' % param.strip(), '\n\g<1>', newtext)
    #---
    newtext = re.sub(r'\s*\}\}\s*$', '\n}}', newtext)
    #---
    return newtext
#---
def add_to_add(new_text, drug_resources, to_add):
    #---
    line = ""
    #---
    to_add = to_add.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
    to_add = to_add.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
    to_add = to_add.replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<")
    #---
    dng = "\=\=\s*External links\s*\=\=\s*\*\s*\{\{cite web\s*\|\s*\|\s*url\s*\=\s*https\:\/\/druginfo.*?\}\}"
    #---
    External = re.search( dng , new_text , flags = re.IGNORECASE )
    External2 = re.search( r"(\=\=\s*External links\s*\=\=)", new_text , flags = re.IGNORECASE )
    External3 = re.search( r"(\{\{reflist\}\})", new_text , flags = re.IGNORECASE )
    #---
    if drug_resources != "" :
        new_drug_resources = drug_resources
        #---
        if new_drug_resources.strip().endswith("}}") :
            new_drug_resources = new_drug_resources[:-2]
            line = new_drug_resources + "\n"+ to_add.strip() + "\n}}"
            new_text = new_text.replace( drug_resources , line )
    #---
    else:
        new_line = "{{drug resources\n\n<!--Identifiers-->\n" + to_add.strip() + "\n}}"
        tt = ""
        to = ""
        #---
        if External:
            tt = External.group(1)
        elif External2:
            tt = External2.group(1)
        #---
        elif External3:
            to = External3.group(1)
        #---
        if tt != "":
            new_text = new_text.replace(tt ,  tt + "\n" + new_line )
        #---
        elif to != "":
            new_text = new_text.replace(to ,  to + "\n== External links ==\n" + new_line )
        #---
        else:
            new_text = new_text + "\n\n== External links ==\n" + new_line
    #---
    return new_text, line
#---
def work_on_text(title, text):
    #---
    drug_resources = ""
    drugbox = ""
    #---
    resources_params = {}
    identifier_params = {}
    #---
    drugbox_params = {}
    #---
    ingr = txtlib2.extract_templates_and_params(text)
    #---
    for temp in ingr:
        #---
        namestrip, params, txt = temp["namestrip"], temp["params"], temp["item"]
        #---
        if namestrip.lower() in [ "drug resources" ] and drug_resources == "":
            drug_resources = txt
            for pap in params :
                resources_params[pap.strip()] = params[pap]
        #--- 
        if namestrip.lower() in [ "drugbox","infobox drug" ] and drugbox == "" :
            drugbox = txt
            #---
            for param in params :
                val = re.sub( lkj, "", params[param] , flags = re.IGNORECASE )
                #---
                val = val.split("\n\n\n\<\!\-\-")[0].split("\n\n\<\!\-\-")[0].split("\n\<\!\-\-")[0]
                #---
                drugbox_params[param.strip()] = val
                if param.strip() in identifiers:
                    identifier_params[param.strip()] = val
        elif namestrip.lower() in [ "infobox medical condition (new)","infobox medical condition" ] :
            printn( "*find temp:[%s]." % namestrip )
    #---
    to_add = ""
    for pa in identifier_params :
        if not pa in resources_params :
            to_add += "| %s = %s\n" % ( pa , identifier_params[pa] )
    #---
    #text3 = text.split("'''%s" % title)[0]
    idi_sect = ""
    #---
    new_text = text
    #---
    drugbox_new = drugbox
    #---
    Names_section = ""
    #--- 
    #if "names" in sys.argv or sys.argv:#xyz
    # إضافة قسم Names
    #---
    if drugbox != "" : 
        drugbox_new , Names_section = add_Names(drugbox_new, drugbox_params )
        finde13 = re.search( r"(\<\!\-\-\s*Identifiers\s*\-\-\>)", drugbox )
        if finde13:
            dd = finde13.group(1)
            idi_sect = drugbox.split(dd)[1].split("<!--Chemical data")[0].split("<!-- Chemical data")[0]
            idi_sect = idi_sect.split("<!-- Definition and medical uses -->")[0]
        #---
        # remove identifiers from {{drugbox|
        drugbox_new = re.sub(r"\<\!\-\-\s*Identifiers\s*\-\-\>","",drugbox_new , flags = re.IGNORECASE )
        for par in identifier_params :
            finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % par , drugbox_new )
            if finde1:
                tt = finde1.group(1)
                new_val = ""
                if re.match( lkj , identifier_params[par].strip() ) :
                    new_val = identifier_params[par]
                drugbox_new = drugbox_new.replace( tt + identifier_params[par].strip() , new_val )
        #---
        drugbox_new = drugbox_new.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
        drugbox_new = drugbox_new.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
        drugbox_new = drugbox_new.replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<")
    #---
    drugbox_new = Physiological_data(drugbox_new, drugbox_params)
    #---
    # إضافة External links
    drugbox_new = add_External_links(drugbox_new, drugbox_params, lkj=lkj)
    #---
    # إضافة Legal data
    drugbox_new = add_Legal_data(drugbox_new, drugbox_params )
    #---
    # إضافة Clinical data
    drugbox_new = add_Clinical(drugbox_new, drugbox_params , Names_section )
    #---
    # إضافة Pharmacokinetic data
    drugbox_new = add_Pharmacokinetic_data(drugbox_new, drugbox_params )
    #---
    # إضافة Chemical data
    drugbox_new = add_Chemical_data(drugbox_new, drugbox_params )
    #---
    if drugbox != drugbox_new :
        #---
        drugbox_new = drugbox_new.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
        drugbox_new = drugbox_new.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
        drugbox_new = drugbox_new.replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<")
    #---
    drugbox_new = re.sub(r"\s*" + lkj2, "\n\n\g<1>", drugbox_new , flags = re.IGNORECASE | re.DOTALL )
    #---
    if drugbox != drugbox_new :
        #---
        drugbox_new = aligns(drugbox_new)
        #---
        new_text = new_text.replace( drugbox, drugbox_new )
    #---
    line = ''
    #---
    # نقل المعرفات لأسفل
    if to_add.strip() != "" :
        new_text, line = add_to_add(new_text, drug_resources, to_add)
    #---
    resources_get_NLM = False
    #---
    if 'NLM' in resources_params :
        resources_get_NLM = resources_params['NLM']
    #---
    # إزالة استشهاد خاطىء
    new_text = remove_cite_web( new_text , resources_get_NLM , line , title )
    new_text = re.sub(r"\{\{drug resources\s*\<\!", "{{drug resources\n<!", new_text , flags = re.IGNORECASE )
    #---
    # إزالة شريط البوابات
    new_text = portal_remove( new_text)
    #---
    return new_text
#---