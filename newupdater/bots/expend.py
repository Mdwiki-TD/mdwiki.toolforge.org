"""
from bots.expend import expend_infoboxs_and_fix
"""
import wikitextparser as wtp
from lists.expend_lists import IMC_params, dup_params


def printn(s):
    return


def expend_and_fix(new_text, temp_name, temp_params, dups):
    parseds = wtp.parse(new_text)
    # ---
    for template in parseds.templates:
        # ---
        name = str(template.normal_name()).strip()
        # ---
        printn(f'expend_and_fix: name:{name}')
        # ---
        if name.lower() == temp_name.lower().strip():
            # ---
            new_temp = "{{" + name + "\n"
            # ---
            params = {}
            # ---
            for param in template.arguments:
                na = str(param.name).strip()
                na = dups.get(na.lower(), na)
                params[na] = str(param.value)
            # ---
            for x in params:
                if not x in temp_params:
                    temp_params.append(x)
            # ---
            temp_text = template.string
            # ---
            for x in temp_params:
                value = params.get(x, '').strip()
                # ---
                newparam = f'| {x.ljust(16)}'
                new_temp += f"{newparam}= {value}\n"
                # ---
            new_temp += "}}"
            # ---
            # template.string = new_temp
            # ---
            new_text = new_text.replace(temp_text, new_temp)
            # ---
            break
    # ---
    # new_text = parsed.string
    return new_text


def expend_infoboxs_and_fix(new_text):
    for tempname, _params in IMC_params.items():
        dups = dup_params.get(tempname, {})
        new_text = expend_and_fix(new_text, tempname, _params, dups)

    return new_text
