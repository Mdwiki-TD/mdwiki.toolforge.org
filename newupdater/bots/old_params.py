"""
from bots.old_params import rename_params
"""
# ---
import wikitextparser as wtp


def printn(s):
    return


def rename_params(temptext):
    # ---
    to_replace = {
        "side effects": "side_effects",
        # "routes_of_use" : "routes_of_administration",
        "side effect": "side_effects",
        "side_effect": "side_effects",
        "legal status": "legal_status",
        "smiles": "SMILES",
        "smiles2": "SMILES2",
    }
    # ---
    new_temptext = temptext
    # ---
    # Parse the wikitext
    parsed_old = wtp.parse(new_temptext)
    temps = parsed_old.templates
    # ---
    temps_okay = ['drugbox', 'infobox drug']
    # ---
    _temps_ = []
    # ---
    for temp in temps:
        # ---
        name = temp.normal_name()
        # ---
        if str(name).lower() in temps_okay:
            _temps_.append(temp)
        else:
            printn(f"*+name ({str([name])}) not in temps_okay .")
        # ---
    # ---
    if len(_temps_) == 0:
        printn("*+_temps_ == 0 .")
        return new_temptext
    # ---
    for temp in _temps_:
        old_temp = temp.string
        # ---
        if new_temptext.find(old_temp) == -1:
            printn(f"*+new_temptext find ({str([old_temp])}) == -1 .")
            continue
        # ---
        # Replace the old parameter with the new parameter
        for old, new in to_replace.items():
            if temp.has_arg(old):
                value = temp.get_arg(old).value
                printn(f'value: {value}')
                temp.set_arg(new, value, before=old)
                temp.del_arg(old)
        # ---
        printn('diff:')
        # ---
        new_temptext = new_temptext.replace(old_temp, temp.string)
    # ---
    return new_temptext


# ---
if __name__ == "__main__":
    # ---
    # python3 pwb.py medUpdater/bots/old_params
    # ---
    import pywikibot

    printn = print
    o = '''
{{drugbox
|side effects=test
<!-- asdadsxxx -->

|temp = {{sub
    |side effects=test1<!-- asdads -->
}}
}}
{{infobox drug
|side effects=22
|side effects=211
}}
'''
    n = rename_params(o)
    # ---
    pywikibot.showDiff(o, n)
    # ---
