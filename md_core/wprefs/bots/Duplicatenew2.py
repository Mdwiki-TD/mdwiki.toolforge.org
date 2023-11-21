#!/usr/bin/python3
"""

تجميع المراجع المتشابهة



"""
#
# (C) Ibrahem Qasim, 2022
#
#

import re
import itertools
from contextlib import suppress

# ---
from wprefs.bots.replace_except import replaceExcept, removeprefix


def get_html_attributes_value(text, param):
    # rar = r'(?i){0}\s*=\s*[\'"]?(?P<{0}>[^\'" >]+)[\'"]?'.format(param)
    rar = r'(?i){0}\s*=\s*[\'"]?(?P<{0}>[^\'" >]+)[\'"]?'.format(param)
    if not text:
        return ''
    m = re.search(rar, text)
    if m:
        return m.group(param)
    return ''


def merge_references(text):
    # ---
    # Match references
    REFS = re.compile(r'(?is)<ref(?P<params>[^>\/]*)>(?P<content>.*?)<\/ref>')
    fmt = r'(?i){0}\s*=\s*(?P<quote>["\']?)\s*(?P<{0}>.+?)\s*(?P=quote)'
    # ---
    name_r = fmt.format('name')
    group_r = fmt.format('group')
    # ---
    ref_tab_new = {}
    # ---
    for Match in REFS.finditer(text):
        content = Match.group('content')
        if not content.strip():
            # printe.output( "\tno content" )
            continue
        # ---
        params = Match.group('params')
        # print(f"{params=}")
        Group = re.search(group_r, params, re.IGNORECASE | re.DOTALL)
        if Group:
            Group = Group.group('group')
        # ---
        namefound = re.search(name_r, params)
        # ---
        if Group not in ref_tab_new:
            ref_tab_new[Group] = {}
        # ---
        if namefound:
            # ---
            name = namefound.group('name')
            quote = namefound.group('quote')
            quoted = namefound.group('quote') == '"'
            # ---
            # change the regex if params.find '" == -1
            # if params.find('"') == -1 and params.find("'") == -1:
            if Group is None:
                if quote == '' or quote is None:
                    name2 = get_html_attributes_value(params, 'name')
                    if name2 and name2 != "":
                        name = name2
                        # printe.output("get the name again:%s" % name )
            # ---
            if name not in ref_tab_new[Group]:
                ref_tab_new[Group][name] = {"org": Match.group(), "others": []}
            else:
                ref_tab_new[Group][name]["others"].append(Match.group())
    # ---
    # Fix references
    for groupname, tab in ref_tab_new.items():
        for name, tab2 in tab.items():
            if name.find("autogen") == -1:
                org = tab2["org"]
                for other in tab2["others"]:
                    text = text.replace(other, org)
    # ---
    return text


def DuplicateReferences(text):
    # ---
    text = merge_references(text)
    # ---
    autogen = "autogen"
    # ---
    found_refs = {}
    found_ref_names = set()
    named_repl = {}
    # ---
    # Match references
    REFS = re.compile(r'(?is)<ref(?P<params>[^>\/]*)>(?P<content>.*?)<\/ref>')
    fmt = r'(?i){0}\s*=\s*(?P<quote>["\']?)\s*(?P<{0}>.+?)\s*(?P=quote)'
    # ---
    name_r = fmt.format('name')
    group_r = fmt.format('group')
    # ---
    # ("group_r:" + group_r )
    # ---
    NAMES = re.compile(name_r)
    GROUPS = re.compile(group_r)
    # ---
    for Match in REFS.finditer(text):
        content = Match.group('content')
        if not content.strip():
            # printe.output( "no content" )
            continue
        # ---
        params = Match.group('params')
        Group = re.search(group_r, params, re.IGNORECASE | re.DOTALL)
        if Group:
            Group = Group.group('group')
        # ---
        if Group not in found_refs:
            found_refs[Group] = {}
        # ---
        groupdict = found_refs[Group]
        # ---
        if content in groupdict:
            v = groupdict[content]
            v[1].append(Match.group())
        else:
            v = [None, [Match.group()], False, False]
        # ---
        namefound = re.search(name_r, params)
        # ---
        if namefound:
            # ---
            quote = namefound.group('quote')
            name = namefound.group('name')
            quoted = quote == '"'
            # ---
            # change the regex if params.find '" == -1
            # if params.find('"') == -1 and params.find("'") == -1:
            if Group is None:
                if quote == '' or quote is None:
                    # print("get the name again:" )
                    name = get_html_attributes_value(params, 'name')
            # ---
            if not v[0]:
                # First name associated with this content
                if name not in found_ref_names:
                    # first time ever we meet this name
                    v[2] = quoted
                    v[0] = name
                else:
                    # if has_key, means that this name is used
                    # with another content. We'll need to change it
                    v[3] = True
            elif v[0] != name:
                named_repl[name] = [v[0], v[2]]
            # ---
            found_ref_names.add(name)
        # ---
        groupdict[content] = v
    # ---
    # printe.output('found %d in found_ref_names.' % len(found_ref_names) )
    # ---
    # Find used autogenerated numbers
    used_numbers = set()
    for name in found_ref_names:
        number = removeprefix(name, autogen)
        with suppress(ValueError):
            used_numbers.add(int(number))
    # ---
    # generator to give the next free number for autogenerating names
    free_number = (str(i) for i in itertools.count(start=1) if i not in used_numbers)
    # ---
    iui_to_named = {}
    # ---
    # Fix references
    for groupname, references in found_refs.items():
        group = f'group="{groupname}" ' if groupname else ''
        # ---
        for ref, v in references.items():
            if len(v[1]) == 1 and not v[3]:
                continue
            # ---
            name = v[0]
            # ---
            if not name:
                name = f'"{autogen}{next(free_number)}"'
            elif v[2]:
                name = f'"{name}"'
            # ---
            named = f'<ref {group}name={name}>{ref}</ref>'
            text = text.replace(v[1][0], named, 1)
            # ---
            # replace multiple identical references with repeated ref
            repeated_ref = f'<ref {group}name={name} />'
            # ---
            sas = v[1][1:]
            # print(f"v[1]: {v[1]}")
            # print(f"sas : {sas}")
            # ---
            iui = fr'<ref\s+{group}name\s*=\s*{name}\s*\/\>'
            iui_to_named[iui] = named
            # ---
            for ref in v[1][1:]:
                # Don't replace inside templates (T266411)
                # if text
                ref2 = re.escape(ref)
                # text = replaceExcept(text, ref2, repeated_ref, exceptions=['template'])
                text = replaceExcept(text, ref2, repeated_ref, exceptions=[])
        # ---
    # ---
    # Fix references with different names
    for ref, v in named_repl.items():
        # TODO : Support ref groups
        name = v[0]
        if v[1]:
            name = f'"{name}"'
        # ---
        text = re.sub(r'<ref name\s*=\s*(?P<quote>["\']?)\s*{}\s*(?P=quote)\s*/>'.format(ref), f'<ref name={name} />', text)
    # ---
    # iui_to_named = {}
    for iui, named in iui_to_named.items():
        if text.find(named) == -1:
            # ---
            # print("text not found: " + named)
            # ---
            text = replaceExcept(text, iui, named, exceptions=['template'], count=1)
            if text.find(named) == -1:
                text = re.sub(iui, named, text, 1)
            # ---
    # ---
    return text


# ---
if __name__ == "__main__":
    tet = """
{{Infobox medical condition (new)
| risksx = <ref name=Fer2016>t1</ref>
| risksx = <ref name=Fer2016>t1</ref>
| risks =
}}
'''PFPS'''<ref name=Fer2016 />

<references />
    """
    # ---
    # python3 core8/pwb.py wprefs/bots/Duplicatenew2
    newt = DuplicateReferences(tet)
    # ---
    # pywikibot.showDiff(tet, newt)
