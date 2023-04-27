"""

"""
#---
import re
import sys
# from .. import txtlib2
import codecs
import os
import wikitextparser as wtp
#---
from medUpdater.bots.Remove        import remove_cite_web, portal_remove
#---
printn_t = {1:False}
#---
def extract_templates_and_params(text): 
    try:
        from medUpdater import txtlib2
        return txtlib2.extract_templates_and_params(text)
    except:
        return {}
#---
def printn(s):
    if printn_t[1] or 'test' in sys.argv: print(s)
#---
identifiers_params = [
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
#---
page_identifier_params = {}
#---
def add_resources(new_text, drug_resources, resources_params):
    #---
    to_add = ''
    #---
    for pa in page_identifier_params :
        #---
        if not pa in resources_params :
            to_add += "| %s = %s\n" % ( pa , page_identifier_params[pa] )
        #---
    #---
    to_add = to_add.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
    to_add = to_add.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
    to_add = to_add.replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<")
    #---
    dng = "\=\=\s*External links\s*\=\=\s*\*\s*\{\{cite web\s*\|\s*\|\s*url\s*\=\s*https\:\/\/druginfo.*?\}\}"
    #---
    External = re.search( dng , new_text, flags=re.IGNORECASE)
    External2 = re.search( r"(\=\=\s*External links\s*\=\=)", new_text, flags=re.IGNORECASE)
    External3 = re.search( r"(\{\{reflist\}\})", new_text, flags=re.IGNORECASE)
    #---
    line = ""
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
_lkj_ = r"<!--\s*(Monoclonal antibody data|External links|Names|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers)\s*-->"
#---
_lkj2_ = r"(<!--\s*(?:Monoclonal antibody data|External links|Names|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status)\s*-->)"
#---
def move_resources(text, title, lkj=_lkj_, lkj2=_lkj2_):
    #---
    new_text = text
    #---
    drugbox_old = ""
    drugbox_params = {}
    #---
    drug_resources = ""
    resources_params = {}
    #---
    # Parse the wikitext
    temps = wtp.parse(text).templates
    #---
    infobox_temp = {}
    resources_temp = False
    #---
    for temp in temps:
        name = str(temp.normal_name()).lower()
        #---
        if name in ['drugbox', 'infobox drug']:
            infobox_temp   = temp
        if name in ['drug resources']:
            resources_temp = temp
    #---
    if infobox_temp == {}: return text
    #---
    infobox_old = infobox_temp.string
    # identifiers_params
    #---
    # remove identifiers_params from infobox
    #---
    for param in identifiers_params:
        if infobox_temp.has_arg(param):
            #---
            value = infobox_temp.get_arg(param).value
            #---
            fa = re.search(lkj2, value)
            #---
            if fa:
                printn(f'fa = {fa}')
                printn(dir(fa))
                tt = fa.group()
                printn(f'tt = {tt}')
                value = value.replace(tt, '').strip()
            #---
            page_identifier_params[param] = value
            #---
            infobox_temp.del_arg(param)
    #---
    infobox_new = infobox_temp.string
    #---
    # remove identifiers from {{drugbox|
    infobox_new = re.sub(r"<!--\s*Identifiers\s*-->","", infobox_new, flags=re.IGNORECASE)
    #---<!--Identifiers-->
    if new_text.find(infobox_old) != -1 :
        #---
        infobox_new = re.sub(r'\n\s*\n\s*[\n\s]+', '\n\n', infobox_new, flags=re.DOTALL|re.MULTILINE)
        #---
        new_text = new_text.replace(infobox_old, infobox_new)
    #---
    # add params to resources_temp
    #---
    line = ''
    #---
    if resources_temp != False:
        #---
        resources_old = resources_temp.string
        #---
        printn(f'resources_temp = {resources_temp}')
        #---
        resources_params = resources_temp.arguments
        #---
        printn(f'resources_params = {resources_params}')
        #---
        for param, value in page_identifier_params.items():
            value = value.strip()
            #---
            if resources_temp.has_arg(param):
                #---
                printn(f'resources_temp.has_arg({param}) = {resources_temp.has_arg(param)}')
                #---
                old_value = resources_temp.get_arg(param).value
                #---
                if value != '' and old_value.strip() == '':
                    resources_temp.set_arg(f' {param} ', value)
                #---
            else:
                resources_temp.set_arg(f' {param} ', f'{value}\n', preserve_spacing=False)
        #---
        resources_new = resources_temp.string
        #---
        printn(f'resources_new = {resources_new}')
        #---
        resources_new = re.sub(r'\n\n\n+<', '\n\n<', resources_new, flags=re.DOTALL|re.MULTILINE)
        #---
        new_text = new_text.replace(resources_old, resources_new)
        #---
    else:
        #---
        # نقل المعرفات لأسفل
        new_text, line = add_resources(new_text, drug_resources, resources_params)
        #---
    resources_get_NLM = False
    #---
    if 'NLM' in resources_params :
        resources_get_NLM = resources_params['NLM']
    #---
    # إزالة استشهاد خاطىء
    new_text = remove_cite_web( new_text , resources_get_NLM , line , title )
    #---
    # إزالة شريط البوابات
    new_text = portal_remove(new_text)
    #---
    return new_text
#---
if __name__ == "__main__" :
    # python3 pwb.py medUpdater/bots/resources
    printn_t[1] = True
    import pywikibot
    diro = os.path.dirname(os.path.abspath(__file__))
    text = codecs.open(os.path.join(diro, "resources.txt") , "r", "utf-8").read()
    newtext = move_resources(text, '')
    codecs.open(os.path.join(diro, "resources_new.txt") , "w", "utf-8").write(newtext)
    pywikibot.showDiff(text, newtext)