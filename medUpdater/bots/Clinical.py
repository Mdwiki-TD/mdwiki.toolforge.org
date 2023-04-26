
"""
<!-- Clinical data-->

"""
#---
Clinical_params = [ 
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
    "typical_dose",
    "dependency_liability",
    "addiction_liability",
    "duration",
    ]
#---
#---
import re
import sys
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1] or 'test' in sys.argv: print(s)
#---
placeholders = {
    "uses":"<!-- primary uses -->",
    "side_effects":"<!-- common side effects and notable side effects -->",
    "interactions":"<!-- notable interactions -->",
    }
#---
def add_Clinical( temptext, boxtable_strip , Names_section ) :
    #---
    boxtable_strip = { x.strip() : y for x, y in boxtable_strip.items() }
    #---
    new_temptext = temptext
    new_temp_replaced = temptext
    #---
    aff = ""
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
    for x in Clinical_params :
        new_val = ""
        #---
        old_val = boxtable_strip.get(x.strip(), "")
        #---
        if old_val != '':
            printn( '*x:"%s" in boxtable_strip' % x )
            addr += "| %s = %s\n" % ( x , old_val )

        elif x.strip() in param_to_add :
            addr += "| %s = %s\n" % ( x , placeholders.get(x,"") )
        #---
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            tt = finde1.group(1)
            new_temp_replaced = new_temp_replaced.replace( tt + old_val.strip() , new_val ) #jjjj
    #---
    # add defined_daily_dose
    if addr != "" and addr.find("defined_daily_dose") == -1 and new_temp_replaced.find("defined_daily_dose") == -1 :
        addr += "| defined_daily_dose = \n"
    #---
    section = re.search( r"(<!--\s*Clinical data\s*-->)", new_temp_replaced , flags = re.IGNORECASE )
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
if __name__ == "__main__" :
    printn_t[1] = True
    add_Clinical('temptext', {}, '')