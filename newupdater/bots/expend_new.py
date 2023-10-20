"""
from bots.expend_new import expend_infoboxs
"""
import wikitextparser as wtp

from lists.expend_lists import main_temps_list


def printn(s):
    return


def expend_new(template, min_len=1):
    template_name = str(template.normal_name()).strip()
    template.name = template_name + '\n'
    to_del = []

    template.rm_dup_args_safe()

    for arg in template.arguments:
        value = arg.value.rstrip()
        if len(arg.name.strip()) <= min_len:
            continue
        arg.value = value + '\n'
        arg.name = arg.name.strip().ljust(16)

    for aa in to_del:
        template.del_arg(aa)

    return template


def expend_infoboxs(new_text):
    parsed = wtp.parse(new_text)
    for temp in parsed.templates:
        temp_str = temp.string

        if not temp_str or temp_str.strip() == '':
            continue

        name = str(temp.normal_name()).strip().lower()

        isvalid = name.startswith('infobox') or name.endswith('infobox') or name.endswith('box')

        if name not in main_temps_list and not isvalid:
            continue

        temp = expend_new(temp)
        new_temp = temp.string
        new_text = new_text.replace(temp_str, new_temp)
        del temp, new_temp

    return new_text
