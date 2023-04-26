
"""
"""
#---
import re
import sys
#---
formola_params = [
    "Ac", "Ag", "Al", "Am", "Ar", "As", "At", "Au", 
    "B", "Ba", "Be", "Bh", "Bi", "Bk", "Br", "C", 
    "Ca", "Cd", "Ce", "Cf", "Cl", "Cm", "Cn", "Co", 
    "Cr", "Cs", "Cu", "D", "Db", "Ds", "Dy", "Er", 
    "Es", "Eu", "F", "Fe", "Fl", "Fm", "Fr", "Ga", 
    "Gd", "Ge", "H", "He", "Hf", "Hg", "Ho", "Hs", 
    "I", "In", "Ir", "K", "Kr", "La", "Li", "Lr", 
    "Lu", "Lv", "Mc", "Md", "Mg", "Mn", "Mo", "Mt", 
    "N", "Na", "Nb", "Nd", "Ne", "Nh", "Ni", "No", 
    "Np", "O", "Og", "Os", "P", "Pa", "Pb", "Pd", 
    "Pm", "Po", "Pr", "Pt", "Pu", "Ra", "Rb", "Re", 
    "Rf", "Rg", "Rh", "Rn", "Ru", "S", "Sb", "Sc", 
    "Se", "Sg", "Si", "Sm", "Sn", "Sr", "Ta", "Tb", 
    "Tc", "Te", "Th", "Ti", "Tl", "Tm", "Ts", "U", 
    "V", "W", "Xe", "Y", "Yb", "Zn", "Zr"
]
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1] or 'test' in sys.argv: print(s)
#---
def add_Chemical_data( temptext, boxtable ) :
    #---
    lic = [
        "charge",
        "chemical_formula",
        "chemical_formula_ref",
        "chemical_formula_comment",

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
        
        "Jmol",
        "Jmol2",

        "molecular_weight",
        "molecular_weight_round",
        "molecular_weight_unit",
        "molecular_weight_ref",
        "molecular_weight_comment",

        "chirality",

        "density",
        "density_notes",

        "melting_point",
        "melting_high",
        "melting_notes",

        "boiling_point",
        "boiling_high",
        "boiling_notes",

        "solubility",
        "sol_units",
        "specific_rotation",
    ]
    #---
    temptext_new      = temptext
    new_param_sorted = ""
    #---
    n = 0
    #---
    for x in formola_params:
        if not x in boxtable: continue
        #---
        n += 1
        #---
        vv = f"| {x} = {boxtable[x].strip()} "
        #---
        # if n = 5 or 10 or 15 or 20
        if n % 5 == 0:  vv += "\n"
        #---
        new_param_sorted += vv
    #---
    for x in lic :
        if not x in boxtable: continue
        #---
        vc = "| %s = %s\n" % ( x , boxtable[x].strip() )
        #---
        new_param_sorted += vc
    #---
    merpatams = list(set(lic + formola_params))
    #---
    for x in merpatams:
        #---
        finde1 = re.search( rf"(\|\s*{x}\s*\=\s*)", temptext_new, flags = re.IGNORECASE )
        #---
        if finde1:
            tt = finde1.group(1)
            #---
            faf = tt + boxtable.get(x, "").strip()
            #---
            if temptext_new.find(faf) != -1 :
                temptext_new = temptext_new.replace(faf, '')
            else:
                printn( "*+temptext_new find (%s) == -1 ." % str([faf]) )
    #---
    temptext_new = re.sub(r"(<!--\s*Chemical data\s*-->)", "", temptext_new , flags = re.IGNORECASE )
    temptext_new = re.sub(r"(<!--\s*Chemical and physical data\s*-->)", "", temptext_new , flags = re.IGNORECASE )
    #---
    new_param_sorted = "\n<!-- Chemical and physical data -->\n" + new_param_sorted + "\n}}"
    #---
    temptext_new = temptext_new.strip()
    #---
    printn(f'new_param_sorted = ({new_param_sorted})')
    #---
    if temptext_new.endswith("}}"):
        temptext_new = temptext_new[:-2] + new_param_sorted
    else:
        printn( "*+temptext_new.endswith(\"}}\") == False ." )
    #---
    printn(f'temptext_new = ({temptext_new})')
    return temptext_new
#---
if __name__ == "__main__" :
    printn_t[1] = True
    #---
    # python3 pwb.py medUpdater/MedWork
    import pywikibot
    #---
    dir = os.path.dirname(os.path.abspath(__file__))
    #---
    text = codecs.open(os.path.join(dir, "bots/resources.txt"), "r", "utf-8").read()
    newtext = add_Chemical_data(text, {})
    #---
    pywikibot.showDiff(text, newtext)
    #---
    codecs.open(os.path.join(dir, "bots/resources_new.txt"), "w", "utf-8").write(newtext)
    #---