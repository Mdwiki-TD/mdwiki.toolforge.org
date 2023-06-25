
import re

import wikitextparser as wtp


def fix_ref_template(text):
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
        for template in templates:
            # ---
            name = str(template.normal_name()).strip()
            # ---
            temp_str = template.string
            # ---
            temp_new = re.sub(r'\n', '', temp_str, flags=re.DOTALL)
            # ---
            newtext = newtext.replace(temp_str, temp_new)
    # ---
    return newtext
