"""
"""
#---
import re
import sys
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1] or 'test' in sys.argv: print(s)
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
    new_temp_replaced = re.sub(r"(<!--\s*Pharmacokinetic data\s*-->)", "", new_temp_replaced , flags = re.IGNORECASE )
    #---
    before = re.search( r"(<!--\s*Chemical data\s*-->)", new_temp_replaced , flags = re.IGNORECASE )
    before2 = re.search( r"(<!--\s*Chemical and physical data\s*-->)", new_temp_replaced , flags = re.IGNORECASE )
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
if __name__ == "__main__" :
    printn_t[1] = True
    add_Pharmacokinetic_data('temptext', {})