"""
<!-- Physiological data -->
"""
#---
Physiological_params = [
    "source_tissues",
    "target_tissues",
    "receptors",
    "agonists",
    "antagonists",
    "precursor",
    "biosynthesis",
    "sources",
    "targets",
]
#---
import re
import sys
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1] or 'test' in sys.argv: print(s)
#---
def add_data( temptext, boxtable, params=[], tato="", finde="") :
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
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % x , new_temp_replaced, flags=re.IGNORECASE)
        if finde1:
            tt = finde1.group(1)
            faf = tt + boxtable.get(x,"").strip()
            #---
            if new_temp_replaced.find(faf) != -1 :
                new_temp_replaced = new_temp_replaced.replace( faf , new_val )#jjjj
    #---
    new_temp_replaced = re.sub(r"(<!--\s*%s\s*-->)" % tato, "", new_temp_replaced, flags=re.IGNORECASE)
    #---
    before = re.search( r"(<!--\s*%s\s*-->)" % finde , new_temp_replaced, flags=re.IGNORECASE)
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
def Physiological_data(drugbox_new, drugbox_params) :
    #---
    tagnr = "Legal status"
    taton = "Physiological data"
    #---
    drugbox_new = add_data(drugbox_new, drugbox_params , params = Physiological_params, tato = taton, finde = tagnr )
    #---
    return drugbox_new
#---
if __name__ == "__main__" :
    printn_t[1] = True
    Physiological_data('temptext', {})