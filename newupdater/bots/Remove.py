"""

"""
# ---
import re
import sys

# ---
printn_t = {1: False}


def printn(s):
    if printn_t[1] or 'test' in sys.argv:
        print(s)


def remove_cite_web(text, resources_get_NLM, line, title):
    new_text = text
    External2 = re.search(r"(\=\=\s*External links\s*\=\=)", new_text)
    # ---
    title2 = re.escape(title)
    # ---
    ioireg = fr"\s*cite web\s*\|\s*url\s*=\s*https\:\/\/druginfo\.nlm\.nih\.gov\/drugportal\/(?:name|category)\/{title2}\s*\|\s*publisher\s*=\s*U\.S\. National Library of Medicine\s*\|\s*work\s*=\s*Drug Information Portal\s*\|\s*title\s*=\s*{title2}\s*"
    ioireg = r"(\*\s*{{" + ioireg + "}})"
    # ---
    vavo = re.search(ioireg, new_text, flags=re.IGNORECASE)
    if vavo:
        vas = vavo.group(1)
        # الوسيط موجود في القالب
        if line != "" and resources_get_NLM and resources_get_NLM == "":
            line2 = re.sub(r"(\s*NLM\s*\=\s*)", r"\g<1>{{PAGENAME}}", line, flags=re.IGNORECASE)
            new_text = new_text.replace(line, line2)
            if line != line2 and new_text.find(line2) != -1:
                new_text = new_text.replace(vas, "")  # حذف قالب الاستشهاد

        # الوسيط غير موجود في القالب
        elif new_text.find("{{drug resources") != -1:
            new_text = re.sub(r"\{\{drug resources", "{{drug resources\n<!--External links-->\n| NLM = {{PAGENAME}}", new_text, flags=re.IGNORECASE)
            if new_text.find("| NLM = {{PAGENAME}}") != -1:
                new_text = new_text.replace(vas, "")  # حذف قالب الاستشهاد

            elif External2 and External2.group(1) != "":
                ttuy = External2.group(1)
                drug_Line = "\n{{drug resources\n<!--External links-->\n| NLM = {{PAGENAME}}\n}}"
                new_text = new_text.replace(ttuy, ttuy + drug_Line)
                if new_text.find(drug_Line.strip()) != -1:
                    new_text = new_text.replace(vas, "")  # حذف قالب الاستشهاد
    # ---
    return new_text


def portal_remove(text):
    par = "{{portal bar|Medicine}}"
    new_text = text
    new_text = re.sub(r"\{\{\s*portal bar\s*\|\s*Medicine\s*\}\}", "", new_text, flags=re.IGNORECASE)
    # ---
    return new_text


# ---
if __name__ == "__main__":
    printn_t[1] = True
    remove_cite_web('temptext', {}, '', '')
