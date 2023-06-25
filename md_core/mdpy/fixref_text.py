
import pywikibot
import re
#---
from mdpy import printe
from mdpy.bots import txtlib2
# ---
def remove_new_Line(text):
    # ---
    newtext = text
    # ---
    ingr = txtlib2.extract_templates_and_params(text)
    # ---
    for temp in ingr:
        # ---
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        # ---
        printe.output( "----------------------------------------------------------------" )
        printe.output( "template (%s) is :" % namestrip )
        # ---
        newtemp = template
        # ---
        newtemp = re.sub(r'(\{\{\s*%s\s*)\n*(\|)' % re.escape(namestrip) , '\g<1>\g<2>' , newtemp )
        newtemp = re.sub(r'\n\s*\|', '|' , newtemp, flags=re.DOTALL)
        # ---
        for x in params:
            # ---
            value = params[x]
            # ---
            value = re.escape(value)
            x = re.escape(x)
            newtemp = re.sub(r"(\|\s*%s\s*\=\s*)(%s)\s*" % (x,value) , "\g<1>\g<2>" , newtemp, flags=re.DOTALL)
        # ---
        newtemp = re.sub(r'\n\s*\}\}\s*$', '}}', newtemp)
        # ---
        if newtemp != template :
            newtext = newtext.replace( template , newtemp )
    # ---
    return newtext
# ---
def fix_ref_template( text ) :
    regref = re.compile( r'(?i)(?P<params><ref[^>/]*>)(?P<content>.*?)</ref>' , re.IGNORECASE|re.DOTALL)
    # ---
    newtext = text
    # ---
    for match in regref.finditer(text):
        # ---
        aaa = match.group()
        # ---
        content = match.group('content')
        if not content.strip():
            continue
        # ---
        content = content.strip()
        # ---
        if content.find('{{Cite') == -1 and content.find('{{cite') == -1 :
            continue
        # ---
        if newtext.find(content) != -1 :
            content2 = remove_new_Line( content )
            if content2 != content :
                bbb = aaa.replace( content , content2 )
                newtext = newtext.replace( aaa , bbb )
    # ---
    return newtext
# ---