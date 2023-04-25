
"""
<!-- Chemical and physical data -->
"chemical_formula",
"chemical_formula_ref",
"chemical_formula_comment",
"molecular_weight",
"molecular_weight_ref",
"molecular_weight_comment",
"index_label",
"index2_label",
"chirality",
"specific_rotation",
"density",
"density_notes",
"melting_point",
"melting_notes",
"boiling_point",
"boiling_notes",
"solubility",
"sol_units",
"SMILES",
"SMILES2",
"StdInChI",
"StdInChI_Ref",
"StdInChI_comment",
"StdInChIKey",
"StdInChIKey_Ref",
"StdInChI2",
"StdInChI2_Ref",
"StdInChIKey2",
"StdInChIKey2_Ref",
#---
"""
#---
import re
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1]: print(s)
#---
def add_Chemical_data( temptext, boxtable ) :
    temptext_new = temptext
    new_temp_replaced = temptext
    #---
    lic = [ 
        "C",
        "H",
        "N",
        "O",     
        "StdInChI",
        "StdInChI2",
        "StdInChI2_Ref",
        "StdInChIKey",
        "StdInChIKey2",
        "StdInChIKey2_Ref",
        "StdInChIKey_Ref",
        "StdInChI_Ref",
        "StdInChI_comment",
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
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        #---
        if finde1:
            tt = finde1.group(1)
            faf = tt + boxtable.get(x,"").strip()
            if new_temp_replaced.find(faf) != -1 :
                new_temp_replaced = new_temp_replaced.replace( faf , new_val )
            else:
                printn( "*+new_temp_replaced find (%s) == -1 ." % str([faf]) )
    #---
    new_temp_replaced = re.sub(r"(\<\!\-\-\s*Chemical data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    new_temp_replaced = re.sub(r"(\<\!\-\-\s*Chemical and physical data\s*\-\-\>)", "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    new_param_sorted = "\n<!-- Chemical and physical data -->\n" + new_param_sorted
    #---
    # temptext_new = new_temp_replaced.replace( bd , unde  , 1 )
    temptext_new = re.sub(r"\}\}$", new_param_sorted + "\n}}", new_temp_replaced.strip() , flags = re.IGNORECASE )
    #---
    return temptext_new
#---
if __name__ == "__main__" :
    printn_t[1] = True
    add_Chemical_data('temptext', {})