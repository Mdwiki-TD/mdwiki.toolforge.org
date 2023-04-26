"""
<!-- Names-->
#---
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
def add_Names(temptext, boxtable) :
    #---
    new_temptext = temptext
    new_temp_replaced = temptext
    #---
    Names_section = ""
    params_to_add = [ "pronounce", "tradename", "synonyms", "IUPAC_name" ]
    #---
    names_params = [
        "pronounce",
        "pronounce_ref",
        "pronounce_comment",
        "tradename",
        "synonyms",
        "INN",
        "AAN",
        "BAN",
        "JAN",
        "USAN",
        "IUPAC_name",
    ]
    #---
    for xe in names_params:
        #---
        if xe in boxtable or xe in params_to_add:
            Names_section += "| %s = %s\n" % ( xe, boxtable.get(xe,"").strip() )
        #---
        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % xe , new_temp_replaced , flags = re.IGNORECASE )
        #---
        if finde1:
            ttr = finde1.group(1)
            #---
            goo = ttr + boxtable.get(xe,"").strip()
            #---
            new_temp_replaced = new_temp_replaced.replace( goo , '')
            new_temp_replaced = new_temp_replaced.replace( goo.strip() , '')
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
    findp = re.search( r"(\|\s*width\s*\=\s*(?:\d+|))\s*\|", new_temp_replaced , flags = re.IGNORECASE )
    if findp:
        put_under = findp.group(1)
    #---
    after_Names = ""#<!-- Names -->
    er_Nam = re.search( r"(<!--\s*Names\s*-->)", new_temp_replaced , flags = re.IGNORECASE )
    if er_Nam:
        after_Names = er_Nam.group(1)
    #---
    put_before = ""#<!-- Clinical data -->
    before = re.search( r"(<!--\s*Clinical data\s*-->)", new_temp_replaced , flags = re.IGNORECASE )
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
            new_temp_replaced = re.sub(r"(<!--\s*Names\s*-->)", "", new_temp_replaced , flags = re.IGNORECASE )
            new_temptext = new_temp_replaced.replace( put_before , beff , 1  )
            
        elif put_under != "" :
            printn( "put_under != ''" )
            unde = put_under + "\n<!--Names-->\n" + Names_section
            new_temp_replaced = re.sub(r"(<!--\s*Names\s*-->)", "", new_temp_replaced , flags = re.IGNORECASE )
            new_temptext = new_temp_replaced.replace( put_under , unde  , 1 )
    #---
    if Names_section == "<!--Names-->\n" :
        Names_section = ""
    #---
    return new_temptext , Names_section
#---
if __name__ == "__main__" :
    printn_t[1] = True
    add_Names('temptext', {})