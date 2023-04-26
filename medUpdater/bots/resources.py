"""

"""
#---
import re
# from .. import txtlib2
import codecs
import os
#---
from medUpdater.bots.Remove        import remove_cite_web, portal_remove
#---
import sys
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1] or 'test' in sys.argv: print(s)
#---
def extract_templates_and_params(text): 
    try:
        from medUpdater import txtlib2
        return txtlib2.extract_templates_and_params(text)
    except:
        return {}
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
    External = re.search( dng , new_text , flags = re.IGNORECASE )
    External2 = re.search( r"(\=\=\s*External links\s*\=\=)", new_text , flags = re.IGNORECASE )
    External3 = re.search( r"(\{\{reflist\}\})", new_text , flags = re.IGNORECASE )
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
def move_resources(text, title, lkj='', lkj2=''):
    #---
    new_text = text
    #---
    drugbox = ""
    drugbox_params = {}
    #---
    drug_resources = ""
    resources_params = {}
    #---
    for temp in extract_templates_and_params(text):
        #---
        namestrip, params, txt = temp["namestrip"], temp["params"], temp["item"]
        #---
        printn(f'namestrip: ({namestrip})')
        #---
        if namestrip.lower() in [ "drug resources" ] and drug_resources == "":
            drug_resources = txt
            printn(f'drug_resources: {drug_resources}')
            resources_params = params
        #---
        if namestrip.lower() in ["drugbox", "infobox drug"] and drugbox == "" :
            drugbox = txt
            #---
            drugbox_params = params
            #---
            for param in drugbox_params :
                val = re.sub( lkj, "", params[param] , flags = re.IGNORECASE )
                #---
                val = val.split("\n\n\n<!--")[0].split("\n\n<!--")[0].split("\n<!--")[0]
                #---
                if param.strip() in identifiers_params:
                    page_identifier_params[param.strip()] = val
            #---
    drugbox_new = drugbox
    #---
    # remove identifiers from {{drugbox|
    drugbox_new = re.sub(r"<!--\s*Identifiers\s*-->","",drugbox_new , flags = re.IGNORECASE )
    #---
    for pa in page_identifier_params :
        #---
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % pa , drugbox_new )
        if finde1:
            tt = finde1.group(1)
            drugbox_new = drugbox_new.replace( tt + page_identifier_params[pa].strip() , '' )
        #---
        drugbox_new = drugbox_new.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
        drugbox_new = drugbox_new.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
        drugbox_new = drugbox_new.replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<")
    #---
    drugbox_new = re.sub(r'\n\s*\n\s*[\n\s]+', '\n\n', drugbox_new, flags = re.DOTALL | re.MULTILINE)
    #---
    new_text = new_text.replace( drugbox , drugbox_new )
    #---
    line = ''
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
    dir = os.path.dirname(os.path.abspath(__file__))
    text = codecs.open(os.path.join(dir, "resources.txt") , "r", "utf-8").read()
    newtext = move_resources(text, '')
    codecs.open(os.path.join(dir, "resources_new.txt") , "w", "utf-8").write(newtext)
    pywikibot.showDiff(text, newtext)