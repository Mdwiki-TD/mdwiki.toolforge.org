
import re

import wikitextparser as wtp


def change_lay_source(temp):
    # ---
    url    = ''
    for x in ['layurl', 'lay-url']:
        if temp.has_arg(x):
            val = temp.get_arg(x).value
            if val.strip() != '':
                url = val.strip()
            temp.del_arg(x)
    # ---
    Date   = ''
    for x in ['laydate', 'lay-date']:
        if temp.has_arg(x):
            val = temp.get_arg(x).value
            if val.strip() != '':
                Date = val.strip()
            temp.del_arg(x)
    # ---
    source = ''
    for x in ['laysource', 'lay-source']:
        if temp.has_arg(x):
            val = temp.get_arg(x).value
            if val.strip() != '':
                source = val.strip()
            temp.del_arg(x)
    # ---
    lay_temp = ''
    # ---
    if url != '' or source != '':
        lay_temp = f'''|template = cite press release|url = {url}|title = |date = {Date}|website = {source}'''
        lay_temp = "* {{lay source" + lay_temp + "}}"
    # ---
    return lay_temp, temp

def fix_ref_template(text, returnsummary=False):
    # ---
    summary = 'Normalize references'
    # ---
    newtext = text
    # ---
    parsed = wtp.parse(text)
    # ---
    for tag in parsed.tags("ref"):
        # ---
        content = tag.contents
        # ---
        if not content.strip():
            continue
        # ---
        templates = tag.templates
        # ---
        for temp in templates:
            # ---
            name = str(temp.normal_name()).strip()
            # ---
            temp_str = temp.string
            # ---
            laysource, temp = change_lay_source(temp)
            # ---
            temp_new = temp.string
            # ---
            temp_new = re.sub(r'\n', '', temp_new, flags=re.DOTALL)
            # ---
            if laysource != '':
                temp_new = temp_new + "\n" + laysource
                summary = 'Normalize references, move lay source params'
            # ---
            newtext = newtext.replace(temp_str, temp_new)
    # ---
    if returnsummary:
        return newtext, summary
    # ---
    return newtext
