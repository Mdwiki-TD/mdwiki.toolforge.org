"""
<!-- Legal data	-->
"""
#---
legal_params = [
    "INN_EMA",
    "engvar",
    "legal_AU",
    "legal_AU_comment",
    "legal_BR",
    "legal_BR_comment",
    "legal_CA",
    "legal_CA_comment",
    "legal_DE",
    "legal_DE_comment",
    "legal_EU",
    "legal_EU_comment",
    "legal_NZ",
    "legal_NZ_comment",
    "legal_UK",
    "legal_UK_comment",
    "legal_UN",
    "legal_UN_comment",
    "legal_US",
    "legal_US_comment",
    "legal_status",
    "DailyMedID",
    "licence_US",
    "license_US",
    "licence_CA",
    "license_CA",
    "licence_EU",
    "license_EU",
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
def add_Legal_data( temptext , boxtable ) :
    #---
    temptext_new = temptext
    new_temp_replaced = temptext
    #---
    aff = ""
    #---
    addr = ""
    #---
    frist_Param = ""
    #---
    for x in legal_params :
        new_val = ""
        if x in boxtable :
            line = "| %s = %s\n" % ( x , boxtable[x] )
            if frist_Param == "" : frist_Param = x
            addr += line

        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % x , new_temp_replaced, flags=re.IGNORECASE)
        if finde1:
            tt = finde1.group(1)
            new_temp_replaced = new_temp_replaced.replace( tt + boxtable.get(x,"").strip() , new_val  )#jjjj
    #---
    new_temp_replaced = re.sub(r"(<!--\s*Legal data\s*-->)", "", new_temp_replaced, flags=re.IGNORECASE)
    new_temp_replaced = re.sub(r"(<!--\s*Legal status\s*-->)", "", new_temp_replaced, flags=re.IGNORECASE)
    #---
    before = re.search( r"(<!--\s*Pharmacokinetic data\s*-->)", new_temp_replaced, flags=re.IGNORECASE)
    before3 = re.search( r"(<!--\s*Chemical data\s*-->)", new_temp_replaced, flags=re.IGNORECASE)
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
        test = re.sub(r"(<!--\s*Legal data\s*-->)", "", test, flags=re.IGNORECASE)
        test = re.sub(r"(<!--\s*Legal status\s*-->)", "", test, flags=re.IGNORECASE)
        if temptext_new == test :
            #---
            # القالب لا يحتوي على <!-- Legal status --> 
            #---
            temptext_new = re.sub(r"(\|\s*%s\s*\=)" % frist_Param, "\n<!-- Legal status -->\n\g<1>", temptext_new, flags=re.IGNORECASE)
            #---
    #---
    temptext_new = re.sub(r"<!--\s*Legal status\s*-->", "<!-- Legal data -->", temptext_new, flags=re.IGNORECASE)
    #---
    return temptext_new
#---
if __name__ == "__main__" :
    printn_t[1] = True
    add_Legal_data('temptext', {})