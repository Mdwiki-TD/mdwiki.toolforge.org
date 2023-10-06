"""
from bots.expend import Expend_Infobox #Expend_Infobox(text, title, section_0)
"""
import wikitextparser as wtp
from bots import txtlib2

from lists.expend_lists import main_temps_list, IMC_params, dup_params


def printn(s):
    return
# ---


def find_main_temp(text, parsed, title):
    # ---
    section_0 = ''
    # ---
    _section0 = parsed.get_sections(level=0)
    if _section0:
        # printn(_section0[0])
        section_0 = str(_section0[0].contents)
    # ---
    tempse_by_u = {}
    tempse = {}
    # ---
    ingr = txtlib2.extract_templates_and_params(section_0)
    u = 0
    for temp in ingr:
        u += 1
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        if (namestrip.find('infobox') != -1 or len(params) > 4) and section_0.find(f'>{template}') == -1:
            printn(f'find temp name: {namestrip}')
            tempse_by_u[u] = temp
            tempse[u] = len(template)
    # ---
    if len(tempse_by_u) == 1:
        for x in tempse_by_u:
            main_temp = tempse_by_u[x]
    else:
        PP = [[y1, u1] for u1, y1 in tempse.items()]
        PP.sort(reverse=True)
        # ---
        for y2, u2 in PP:
            main_temp = tempse_by_u[u2]
            break
    # ---
    params = main_temp['params']
    temptext = main_temp['item']
    # ---
    tempname = main_temp['namestrip']
    # ---
    printn(f'find_main_temp, result: {tempname}')
    # ---
    return params, temptext


def Expend_Infobox(newtext, title):
    # ---
    main_temp_params = {}
    main_temp_text = ''
    main_temp_title = ''
    # ---
    parsed = wtp.parse(newtext)
    # ---
    if main_temp_params == {}:
        # ---
        for template in parsed.templates:
            # ---
            name = str(template.normal_name()).strip()
            # ---
            if name.lower() in main_temps_list:
                # ---
                main_temp_title = name
                # ---
                printn(f'tempname: {name}')
                # ---
                main_temp_params = {str(param.name).strip(): str(param.value) for param in template.arguments}
                # ---
                main_temp_text = template.string
                # ---
                break
    # ---
    if main_temp_params == {}:
        main_temp_params, main_temp_text = find_main_temp(newtext, parsed, title)
    # ---
    if main_temp_params != {}:
        # ---
        new_temp_x = "{{" + main_temp_title + "\n"
        # ---
        # new_temp = main_temp_text
        # ---
        for param, value in main_temp_params.items():
            # newparam = '|%s=' % param.ljust(16)
            # new_temp = re.sub(r'\s*(\|\s*%s\s*\=)' % param, '\n' + newparam, new_temp)

            newparam_x = param.ljust(16)
            new_temp_x += f"|{newparam_x}={value.strip()}\n"
            # ---
        # ---
        # new_temp = re.sub(r'\s*\}\}\s*$', '\n}}', new_temp)
        # ---
        new_temp_x += "\n}}"
        # ---
        newtext = newtext.replace(main_temp_text, new_temp_x)
        newtext = newtext.replace(new_temp_x + "'''", new_temp_x + "\n'''")
    # ---
    return newtext
# ---


def Expend_Infoboxs(new_text, temp_name, temp_params, dups):
    parseds = wtp.parse(new_text)
    # ---
    for template in parseds.templates:
        # ---
        name = str(template.normal_name()).strip()
        # ---
        printn(f'Expend_Infoboxs: name:{name}')
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
# ---


def Expend_Infobox_new(new_text):
    # ---
    for tempname, _params in IMC_params.items():
        dups = dup_params.get(tempname, {})
        new_text = Expend_Infoboxs(new_text, tempname, _params, dups)
    # ---
    return new_text
# ---
