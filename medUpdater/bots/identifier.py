"""
<!-- Identifiers -->
"index_label",
"index_comment",
"index2_label",
"index2_comment",
"CAS_number",
"CAS_number_Ref",
"CAS_supplemental",
"CAS_number2",
"CAS_number2_Ref",
"CAS_supplemental2",
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
"ATC_prefix",
"ATC_suffix",
"ATC_supplemental",
"ATC_prefix2",
"ATC_suffix2",
"ATC_supplemental2",

"""
#---
import re
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1]: print(s)
#---
def add_Identifiers( temptext , boxtable) :
    #---

    #---
    return ''
#---
if __name__ == "__main__" :
    printn_t[1] = True
    add_Identifiers('temptext', {})