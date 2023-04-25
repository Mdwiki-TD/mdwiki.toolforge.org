
"""

"""
#---
import re
#---
printn_t = {1:False}
#---
def printn(s):
    if printn_t[1]: print(s)
#---
def add_External_links( temptext , boxtable, lkj='') :
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
    f4f = re.search( r"(\<\!\-\-\s*Clinical data\s*\-\-\>)(\s*|)(\|\s*Drugs\.com\s*\=\s*\*\!\*Drugs\*\!\*)", new_temp_replaced , flags = re.IGNORECASE )
    if f4f:
        new_temp_replaced = new_temp_replaced.replace( f4f.group(1) + f4f.group(2) + f4f.group(3) , f4f.group(3) + f4f.group(2) + f4f.group(1)  )
    #---
    for x in pa :
        new_val = ""
        if x in boxtable :
            addr += "| %s = %s\n" % ( x , boxtable[x] )
            if re.match( lkj , boxtable[x].strip() ) :
                new_val = boxtable[x]

        finde1 = re.search( r"(\|\s*%s\s*\=\s*)" % x , new_temp_replaced , flags = re.IGNORECASE )
        if finde1:
            tt = finde1.group(1)
            new_temp_replaced = new_temp_replaced.replace( tt + boxtable.get(x,"").strip() , new_val  )#jjjj
    #---
    new_temp_replaced = re.sub(r"(\<\!\-\-\s*External links\s*\-\-\>)", "", new_temp_replaced )
    #---
    put_er = ""
    findp = re.search( r"(\|\s*Drugs\.com\s*\=\s*\*\!\*Drugs\*\!\*)", new_temp_replaced , flags = re.IGNORECASE )
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
        test = re.sub(r"(\<\!\-\-\s*External links\s*\-\-\>)", "", test , flags = re.IGNORECASE )
        #---
        if new_temptext == test :
            #---
            # القالب لا يحتوي على <!-- External links --> 
            #---
            new_temptext = re.sub(r"(\|\s*MedlinePlus\s*\=)", "\n<!--External links-->\n\g<1>", new_temptext , flags = re.IGNORECASE )
            #---
    #---
    return new_temptext
#---
if __name__ == "__main__" :
    printn_t[1] = True
    add_External_links('temptext', {})