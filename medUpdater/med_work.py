#!/usr/bin/env python

"""
#!/usr/bin/python
python3 pwb.py mdd -page:Aspirin ask 

python pwb.py mdd -page:Aspirin ask

done:
* Removed {{portal bar|Medicine}} if present
* Move identifiers to the bottom of the page such as this[3]

* drugbox :
** Add the heading <!--Names--> and add "pronounce", "tradename", and "synonyms" and "IUPAC_name" under it[4]
** Create the heading <!--External links--> and add "Drugs.com" and "MedlinePlus" under it[5]

** Add "class", "uses", and "side effects" under <!--Clinical data--> in that order. Add "defined_daily_dose" at the end of that section if not present[6]
** Move / add "onset" and "duration_of_action" after "routes_of_administration" and before "defined_daily_dose"[8]

** Create the heading <!-- Legal data --> if not present and add "legal_UK", "legal_US", "legal _status" under it[7]

* drug resources :
** Add <!--External links--> and "NLM" at the top of the drug resources template[9]

** If {{cite web | url = https://druginfo.nlm.nih.gov/drugportal/name/lactulose | publisher = U.S. National Library of Medicine | work = Drug Information Portal | title = XX }} is present remove it and add the value present in "title =" to the NLM value in the "drug resources" template. If the value is the same as the pagename add "PAGENAME"[10]

"""
#
# (C) Ibrahem Qasim, 2023
#
#
import re
import sys
import os
#---
def printn(s):
    return
#---
project = "/mnt/nfs/labstore-secondary-tools-project/mdwiki"
#---
if not os.path.isdir(project): project = "/mdwiki"
#---
import txtlib2
#---
lkj = r"\<\!\-\-\s*(External links|Names|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*\=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers)\s*\-\-\>"
#---
lkj2 = r"(\<\!\-\-\s*(?:External links|Names|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|Chemical and physical data|index_label\s*\=\s*Free Base|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status)\s*\-\-\>)"
#---
placeholders = {
    "uses":"<!-- primary uses -->",
    "side_effects":"<!-- common side effects and notable side effects -->",
    "interactions":"<!-- notable interactions -->",
    }
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
#---
_ETP_REGEX = re.compile(
    r"{{(?P<name>drug resources|drugbox)"
    r"(?:\|(?P<params>[^{]+?(?:{[^{]+?}[^{]*?)?)?)?}}"
    )
#---
def remove_cite_web( text, resources, line, title ):
    new_text = text
    External2 = re.search( "(\=\=\s*External links\s*\=\=)", new_text )
    #---
    title2 = re.escape(title)
    #---
    ioireg = r"(\*\s*\{\{\s*cite web\s*\|\s*url\s*\=\s*https\:\/\/druginfo\.nlm\.nih\.gov\/drugportal\/name\/%s\s*\|\s*publisher\s*\=\s*U\.S\. National Library of Medicine\s*\|\s*work\s*\=\s*Drug Information Portal\s*\|\s*title\s*\=\s*%s\s*\}\})" % (title2 , title2)
    #---
    vavo = re.search( ioireg, new_text, flags = re.IGNORECASE )
    if vavo :
        vas = vavo.group(1)
        # الوسيط موجود في القالب
        if line != "" and "NLM" in resources and resources["NLM"] == "":
            line2 = re.sub("(\s*NLM\s*\=\s*)", "\g<1>{{PAGENAME}}", line , flags = re.IGNORECASE )
            new_text = new_text.replace( line, line2 )
            if line != line2 and new_text.find(line2) != -1 :
                new_text = new_text.replace( vas, "" )             # حذف قالب الاستشهاد
        
        # الوسيط غير موجود في القالب
        elif new_text.find("{{drug resources") != -1 :
            new_text = re.sub( "\{\{drug resources", "{{drug resources\n<!--External links-->\n| NLM = {{PAGENAME}}", new_text , flags = re.IGNORECASE )
            if new_text.find("| NLM = {{PAGENAME}}") != -1 :
                new_text = new_text.replace( vas, "" )                 # حذف قالب الاستشهاد
            
            elif External2 and External2.group(1) != "" :
                ttuy = External2.group(1)
                drug_Line = "\n{{drug resources\n<!--External links-->\n| NLM = {{PAGENAME}}\n}}"
                new_text = new_text.replace(ttuy , ttuy + drug_Line )
                if new_text.find( drug_Line.strip() ) != -1 :
                    new_text = new_text.replace( vas, "" )             # حذف قالب الاستشهاد
    #---
    return new_text
#---
def add_Names(temptext, boxtable) :
    #---
    new_temptext = temptext
    new_temp_replaced = temptext
    #---
    Names_section = ""
    paen = [ "pronounce", "tradename", "synonyms", "IUPAC_name" ]
    #---
    for xe in paen :
        new_valr = ""
        #---
        Names_section += "| %s = %s\n" % ( xe , boxtable.get(xe,"").strip() )
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % xe , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            ttr = finde1.group(1)
            goo = ttr + boxtable.get(xe,"").strip()
            if new_temp_replaced.find( goo ) != -1 :
                new_temp_replaced = new_temp_replaced.replace( goo , new_valr )#jjjj
            elif new_temp_replaced.find( goo.strip() ) != -1 :
                new_temp_replaced = new_temp_replaced.replace( goo.strip() , new_valr )#jjjj
            else:
                printn( "*new_temp_replaced find (%s) == -1 ." % str([goo]) )
        else:
            printn( "*no finde1 for %s" % xe )
    #---
    Names_section = Names_section.strip()
    #---
    printn( "*Names_section:" )
    printn( Names_section )
    printn( "/////////////" )
    #---
    put_under = ""
    findp = re.search( "(\|\s*width\s*\=\s*(?:\d+|))\s*\|", new_temp_replaced , flags = re.IGNORECASE )
    if findp:
        put_under = findp.group(1)
    #---
    after_Names = ""#<!-- Names -->
    er_Nam = re.search( "(\<\!\-\-\s*Names\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    if er_Nam:
        after_Names = er_Nam.group(1)
    #---
    put_before = ""#<!-- Clinical data -->
    before = re.search( "(\<\!\-\-\s*Clinical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    if before:
        put_before = before.group(1)
    #---
    if Names_section != "" :
        if after_Names != "" :
            printn( "after_Names != ''" )
            ben = after_Names + "\n" + Names_section
            new_temptext = new_temp_replaced.replace( after_Names , ben , 1  )
            
        elif put_before != "" :
            printn( "put_before != ''" )
            beff = "<!--Names-->\n" + Names_section + "\n" + put_before
            new_temp_replaced = re.sub( "(\<\!\-\-\s*Names\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
            new_temptext = new_temp_replaced.replace( put_before , beff , 1  )
            
        elif put_under != "" :
            printn( "put_under != ''" )
            unde = put_under + "\n<!--Names-->\n" + Names_section
            new_temp_replaced = re.sub( "(\<\!\-\-\s*Names\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
            new_temptext = new_temp_replaced.replace( put_under , unde  , 1 )
    #---
    if Names_section == "<!--Names-->\n" :
        Names_section = ""
    #---
    return new_temptext , Names_section
#---
def portal_remove(text) :
    par = "{{portal bar|Medicine}}"
    new_text = text
    new_text = re.sub("\{\{\s*portal bar\s*\|\s*Medicine\s*\}\}", "", new_text , flags = re.IGNORECASE )
    #---
    return new_text
#---
def add_Clinical( temptext , boxtable , boxtable_strip , Names_section ) :
    #---
    new_temptext = temptext
    new_temp_replaced = temptext
    #---
    aff = ""
    lic = [ 
        "class",  
        "uses", 
        "side effects", 
        "side effect", 
        "side_effects", 
        "side_effect", 
        "interactions", 
        "pregnancy_AU", 
        "pregnancy_AU_comment", 
        "pregnancy_US", 
        "pregnancy_US_comment", 
        "pregnancy_category", 
        "breastfeeding", 
        "PLLR", 
        "routes_of_administration", 
        "onset", 
        "duration_of_action", 
        "defined_daily_dose",
        "typical_dose"
        ]
    #---
    param_to_add = [ 
        "class",
        "uses",
        "side_effects", 
        "interactions", 
        "onset", 
        "duration_of_action", 
        "defined_daily_dose", 
        "typical_dose", 
        "breastfeeding"
        ]
    #---
    addr = ""
    #---
    for x in lic :
        old_val = ""
        new_val = ""#
        if x in boxtable :
            printn( '*x:"%s" in boxtable' % x )
            old_val = boxtable[x]
            line = "| %s = %s\n" % ( x , boxtable[x] )
            printn( line )
            addr += line
            
        elif x.strip() in boxtable_strip :
            old_val = boxtable_strip[x.strip()]
            addr += "| %s = %s\n" % ( x , old_val )
        elif x in param_to_add :
            addr += "| %s = %s\n" % ( x , placeholders.get(x,"") )
        #---
        finde1 = re.search( "(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            tt = finde1.group(1)
            new_temp_replaced = new_temp_replaced.replace( tt + old_val.strip() , new_val ) #jjjj
    #---
    # add defined_daily_dose
    if addr != "" and addr.find("defined_daily_dose") == -1 and new_temp_replaced.find("defined_daily_dose") == -1 :
        addr += "| defined_daily_dose = \n"
    #---
    section = re.search( "(\<\!\-\-\s*Clinical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    if addr != "":
        if section:
            aff = section.group(1)
            if section.group(1) != "" :
                unde = section.group(1) + "\n" + addr
                new_temptext = new_temp_replaced.replace( aff , unde , 1  )
        elif Names_section != "" and new_temp_replaced.find( Names_section.strip() ) != -1 :
            #---
            # إضافة القسم تحت قسم Names
            dodo = Names_section.strip() + "\n" + addr
            new_temptext = new_temp_replaced.replace( Names_section.strip() , dodo  , 1 )
    #---
    return new_temptext
#---
def add_External_links( temptext , boxtable ) :
    #---
    new_temptext = temptext
    new_temp_replaced = temptext
    #---
    Drugs = boxtable.get("Drugs.com","")
    dud_line = "*!*Drugs*!*"
    #---
    if Drugs.strip() != "" and new_temp_replaced.find(Drugs.strip()) != -1 :
        new_temp_replaced = new_temp_replaced.replace( Drugs.strip() , dud_line   )#jjjj
    #---
    addr = ""
    pa = [ "MedlinePlus" ] #"Drugs.com",
    #---
    #---
    f4f = re.search( "(\<\!\-\-\s*Clinical data\s*\-\-\>)(\s*|)(\|\s*Drugs\.com\s*\=\s*\*\!\*Drugs\*\!\*)", new_temp_replaced , flags = re.IGNORECASE )
    if f4f:
        new_temp_replaced = new_temp_replaced.replace( f4f.group(1) + f4f.group(2) + f4f.group(3) , f4f.group(3) + f4f.group(2) + f4f.group(1)  )
    #---
    for x in pa :
        new_val = ""
        if x in boxtable :
            addr += "| %s = %s\n" % ( x , boxtable[x] )
            if re.match( lkj , boxtable[x].strip() ) :
                new_val = boxtable[x]

        finde1 = re.search( "(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            tt = finde1.group(1)
            new_temp_replaced = new_temp_replaced.replace( tt + boxtable.get(x,"").strip() , new_val  )#jjjj
    #---
    new_temp_replaced = re.sub( "(\<\!\-\-\s*External links\s*\-\-\>)", "", new_temp_replaced )
    #---
    put_er = ""
    findp = re.search( "(\|\s*Drugs\.com\s*\=\s*\*\!\*Drugs\*\!\*)", new_temp_replaced , flags = re.IGNORECASE )
    if findp:
        put_er = findp.group(1)
    #---
    if put_er != "" :
        unde = "\n<!--External links-->\n" + put_er.strip() + "\n" + addr
        new_temptext = new_temp_replaced.replace( put_er, unde , 1 )
    #---
    new_temptext = new_temptext.replace( dud_line , Drugs.strip() )
    #---
    # 2021
    if new_temptext == temptext :
        test = new_temptext
        test = re.sub( "(\<\!\-\-\s*External links\s*\-\-\>)", "", test , flags = re.IGNORECASE )
        #---
        if new_temptext == test :
            #---
            # القالب لا يحتوي على <!-- External links --> 
            #---
            new_temptext = re.sub( "(\|\s*MedlinePlus\s*\=)", "\n<!--External links-->\n\g<1>", new_temptext , flags = re.IGNORECASE )
            #---
    #---
    return new_temptext
#---
def add_Legal_data( temptext , boxtable ) :
    #---
    finde13 = re.search( "(\<\!\-\-\s*Legal status\s*\-\-\>)", temptext , flags = re.IGNORECASE )
    #---
    temptext_new = temptext
    new_temp_replaced = temptext
    #---
    aff = ""
    lic = [ 
        "legal_AU",
        "legal_AU_comment",
        "legal_BR",
        "legal_BR_comment",
        "legal_CA",
        "legal_CA_comment",
        "legal_DE",
        "legal_DE_comment",
        "legal_NZ",
        "legal_NZ_comment",
        "legal_UK",
        "legal_UK_comment",
        "legal_US",
        "legal_US_comment",
        "legal_UN",
        "legal_UN_comment",
        "legal_status",
        "legal status",
        "DailyMedID",
        "licence_EU",
        "licence_US",
        "licence_CA",
        ]
    #---
    addr = ""
    #---
    frist_Param = ""
    #---
    for x in lic :
        new_val = ""
        if x in boxtable :
            line = "| %s = %s\n" % ( x , boxtable[x] )
            if frist_Param == "" : frist_Param = x
            addr += line

        finde1 = re.search( "(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            tt = finde1.group(1)
            new_temp_replaced = new_temp_replaced.replace( tt + boxtable.get(x,"").strip() , new_val  )#jjjj
    #---
    new_temp_replaced = re.sub( "(\<\!\-\-\s*Legal data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    new_temp_replaced = re.sub( "(\<\!\-\-\s*Legal status\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    before = re.search( "(\<\!\-\-\s*Pharmacokinetic data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    before3 = re.search( "(\<\!\-\-\s*Chemical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    #---
    if addr != "":
        addr = "\n<!-- Legal status -->\n" + addr
        if before:
            if before.group(1) != "" :
                unde = addr + "\n" + before.group(1).strip()
                temptext_new = new_temp_replaced.replace( before.group(1) , unde  , 1 )
    #---
    if temptext_new == temptext and frist_Param != "" :
        test = temptext_new
        test = re.sub( "(\<\!\-\-\s*Legal data\s*\-\-\>)", "", test , flags = re.IGNORECASE )
        test = re.sub( "(\<\!\-\-\s*Legal status\s*\-\-\>)", "", test , flags = re.IGNORECASE )
        if temptext_new == test :
            #---
            # القالب لا يحتوي على <!-- Legal status --> 
            #---
            temptext_new = re.sub( "(\|\s*%s\s*\=)" % frist_Param, "\n<!-- Legal status -->\n\g<1>", temptext_new , flags = re.IGNORECASE )
            #---
    #---
    return temptext_new
#---
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
        finde1 = re.search( "(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        #---
        if finde1:
            tt = finde1.group(1)
            faf = tt + boxtable.get(x,"").strip()
            if new_temp_replaced.find(faf) != -1 :
                new_temp_replaced = new_temp_replaced.replace( faf , new_val )#jjjj
            else:
                printn( "*+new_temp_replaced find (%s) == -1 ." % str([faf]) )
    #---
    new_temp_replaced = re.sub( "(\<\!\-\-\s*Pharmacokinetic data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    before = re.search( "(\<\!\-\-\s*Chemical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
    before2 = re.search( "(\<\!\-\-\s*Chemical and physical data\s*\-\-\>)", new_temp_replaced , flags = re.IGNORECASE )
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
def add_Chemical_data( temptext , boxtable ) :
    temptext_new = temptext
    new_temp_replaced = temptext
    #---
    lic = [ 
        "C",
        "H",
        "N",
        "O",
        "StdInChI",
        "StdInChIKey",
        "StdInChIKey_Ref",
        "SMILES"
        ]
    #---
    new_param_sorted = ""
    #---
    for x in lic :
        new_val = ""
        if x in boxtable :
            new_param_sorted += "| %s = %s\n" % ( x , boxtable[x] )
        #---
        finde1 = re.search( "(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        #---
        if finde1:
            tt = finde1.group(1)
            faf = tt + boxtable.get(x,"").strip()
            if new_temp_replaced.find(faf) != -1 :
                new_temp_replaced = new_temp_replaced.replace( faf , new_val )
            else:
                printn( "*+new_temp_replaced find (%s) == -1 ." % str([faf]) )
    #---
    new_temp_replaced = re.sub( "(\<\!\-\-\s*Chemical data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    new_temp_replaced = re.sub( "(\<\!\-\-\s*Chemical and physical data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    new_param_sorted = "\n<!-- Chemical and physical data -->\n" + new_param_sorted
    #---
    # temptext_new = new_temp_replaced.replace( bd , unde  , 1 )
    temptext_new = re.sub(r"\}\}$", new_param_sorted + "\n}}", new_temp_replaced.strip() , flags = re.IGNORECASE )
    #---
    return temptext_new
#---
def add_data( temptext, boxtable, params=[], tato="", finde="") :
    #print( " add_data...." ) 
    temptext_new = temptext
    new_temp_replaced = temptext
    #---
    aff = ""
    addr = ""
    #---
    for x in params :
        new_val = ""
        if x in boxtable :
            addr += "| %s = %s\n" % ( x , boxtable[x] )
        finde1 = re.search( "(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            tt = finde1.group(1)
            faf = tt + boxtable.get(x,"").strip()
            #---
            if new_temp_replaced.find(faf) != -1 :
                new_temp_replaced = new_temp_replaced.replace( faf , new_val )#jjjj
    #---
    new_temp_replaced = re.sub( "(\<\!\-\-\s*%s\s*\-\-\>)" % tato, "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    before = re.search( "(\<\!\-\-\s*%s\s*\-\-\>)" % finde , new_temp_replaced , flags = re.IGNORECASE )
    #---
    bd = ""
    if before :
        bd = before.group(1)
    #---
    if bd != "" and new_temp_replaced.find(bd) != -1 and addr != "" :
        addr = ( "\n<!-- %s -->\n" % tato ) + addr
        unde = addr + "\n" + bd.strip()
        temptext_new = new_temp_replaced.replace( bd, unde, 1 )
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
def add_to_add(new_text, drug_resources, resources, to_add, title):
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
    External2 = re.search( "(\=\=\s*External links\s*\=\=)", new_text , flags = re.IGNORECASE )
    External3 = re.search( "(\{\{reflist\}\})", new_text , flags = re.IGNORECASE )
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
    # إزالة استشهاد خاطىء
    new_text = remove_cite_web( new_text , resources , line , title )
    new_text = re.sub( "\{\{drug resources\s*\<\!", "{{drug resources\n<!", new_text , flags = re.IGNORECASE )
    #---
    return new_text
#---
def work_on_text(title, text):
    #---
    drug_resources = ""
    drugbox = ""
    #---
    resources_strip = {}
    resources = {}
    box_strip = {}
    box = {}
    #---
    drugbox_params_strip = {}
    drugbox_params = {}
    #---
    ingr = txtlib2.extract_templates_and_params(text)
    #---
    for temp in ingr:
        #---
        name, namestrip, params, txt = temp["name"], temp["namestrip"], temp["params"], temp["item"]
        #---
        if namestrip.lower() in [ "drug resources" ] and drug_resources == "":
            drug_resources = txt
            #print( "__________________"  )
            #print( "*drug_resources:%s" % drug_resources )
            #print( "drug_resources params:"  )
            #print( params  )
            #print( " <<lightyellow>> __________________"  )
            for pap in params :
                resources[pap] = params[pap]
                resources_strip[pap.strip()] = params[pap]
        #--- 
        if namestrip.lower() in [ "drugbox","infobox drug" ] and drugbox == "" :
            drugbox = txt
            #---
            for param in params :
                val = re.sub( lkj, "", params[param] , flags = re.IGNORECASE )
                #---
                val = val.split("\n\n\n\<\!\-\-")[0].split("\n\n\<\!\-\-")[0].split("\n\<\!\-\-")[0]
                #---
                drugbox_params[param] = val
                drugbox_params_strip[param.strip()] = val
                if param in identifiers or param.strip() in identifiers:
                    box[param] = val
                    box_strip[param.strip()] = val
        elif namestrip.lower() in [ "infobox medical condition (new)","infobox medical condition" ] :
            printn( "*find temp:[%s]." % namestrip )
    #---
    to_add = ""
    for pa in box_strip :
        if not pa in resources_strip :
            to_add += "| %s = %s\n" % ( pa , box_strip[pa] )
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
        for par in box :
            finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % par , drugbox_new )
            if finde1:
                tt = finde1.group(1)
                new_val = ""
                if re.match( lkj , box[par].strip() ) :
                    new_val = box[par]
                drugbox_new = drugbox_new.replace( tt + box[par].strip() , new_val )
        #---
        drugbox_new = drugbox_new.replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n\n","\n")
        drugbox_new = drugbox_new.replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|").replace("\n\n|","\n|")
        drugbox_new = drugbox_new.replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<").replace("\n\n<","\n<")
    #---
    tagnr = "Legal status"
    taton = "Physiological data"
    fng = ["source_tissues","target_tissues","receptors","agonists","antagonists","precursor","biosynthesis"]#,"metabolism"]
    drugbox_new = add_data(drugbox_new, drugbox_params , params = fng, tato = taton, finde = tagnr )
    #---
    # إضافة External links
    drugbox_new = add_External_links(drugbox_new, drugbox_params )
    #---
    # إضافة Legal data
    drugbox_new = add_Legal_data(drugbox_new, drugbox_params )
    #---
    # إضافة Clinical data
    drugbox_new = add_Clinical(drugbox_new, drugbox_params , drugbox_params_strip , Names_section )
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
    drugbox_new = re.sub( "\s*" + lkj2, "\n\n\g<1>", drugbox_new , flags = re.IGNORECASE | re.DOTALL )
    #---
    if drugbox != drugbox_new :
        #---
        drugbox_new = aligns(drugbox_new)
        #---
        new_text = new_text.replace( drugbox, drugbox_new )
    #---
    # نقل المعرفات لأسفل
    if to_add.strip() != "" :
        new_text = add_to_add(new_text, drug_resources, resources, to_add, title)
    #---
    # إزالة شريط البوابات
    new_text = portal_remove( new_text)
    #---
    return new_text
#---