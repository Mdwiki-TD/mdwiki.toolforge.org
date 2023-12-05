"""


"""
import sys
import json
from pathlib import Path
import codecs

# ---
from mdpy import printe

# ---
from priorviews.lists import translators

# translators.tra_by_lang
# translators.counts_by_translator
# ---
text_main = '''
<div style="height:580px;width:100%;overflow-x:auto; overflow-y:auto">

{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! n
! style="position: sticky;top: 0;left: 0;" | en
!urls/refs
!lead<br>urls/refs
!'''


def match_p(refs, p_ref):
    # Find all the elements that are common between `p_ref` and `refs`
    same = [x for x in p_ref if x in refs]

    len_same = len(same)
    len_refs = len(refs)

    # If there are no common elements between `p_ref` and `refs`, return False and the length of `same`
    if len_same < 1:
        return False, len_same

    # If the length of `same` is less than 8 or less than half the length of `refs` minus 1,
    # return False and the length of `same`
    if 6 > len_same < ((len_refs / 2) - 1):
        return False, len_same

    # Otherwise, return True and the length of `same`
    return True, len_same


# ---
t_sections = {}
all_langs_states = {}


def get_t_sections():
    # This function generates a wikitext table of statistics for different sections
    # The table has the following columns: section, en, all langlinks, green, red

    # Initialize the table with headings for each column
    text = '\n{| class="wikitable sortable"\n|- \n! section\n! en\n! all langlinks\n! green\n! red\n|- \n'

    # Initialize variables to keep track of the total values for each column
    allen = 0
    allall = 0
    allgreen = 0
    allred = 0

    # Loop over each section and add a row to the table with statistics for that section
    for k, tt in t_sections.items():
        # Calculate the total number of green and red links for this section
        green = tt['green']
        red = tt['red']
        en = tt['en']
        # ---
        all = green + red
        allall += all

        # percentage from all
        g_p = round((green / all) * 100, 2)
        # ---
        r_p = round((red / all) * 100, 2)
        # ---
        # Add the values for this section to the total values for each column
        allen += en
        allgreen += green
        allred += red

        # Add a row to the table with statistics for this section
        text += f'! [[User:Mr. Ibrahem/prior/{k}|{k}]]\n'
        text += f'| {en:,}\n'
        text += f'| {all:,}\n'
        text += f'| {green:,} ({g_p}%) \n'
        text += f'| {red:,} ({r_p}%) \n'
        text += '|-\n'
    # ---
    # Add a final row to the table with the total values for each column
    green_p = round((allgreen / allall) * 100, 2)
    red_p = round((allred / allall) * 100, 2)
    # ---
    text += f'! total\n! {allen:,}\n! {allall:,}\n! {allgreen:,} ({green_p}%)\n! {allred:,} ({red_p}%)'
    # ---
    text += '\n|}'
    # ---
    te_langs = '\n== All languages =='
    te_langs += '\n<div style="width:100%;overflow-x:auto; overflow-y:auto">'
    te_langs += '\n{| class="wikitable sortable" style="width:100%;"'
    te_langs += '\n|- style="position: sticky;top: 0; z-index: 2;"'
    te_langs += '\n! style="position: sticky;top: 0;left: 0;" | key'
    te_langs += '\n!'
    # ---
    te_langs += " !! ".join(all_langs_states.keys())
    # ---
    all_line = ''
    green_line = ''
    red_line = ''
    # ---
    for l, ta in all_langs_states.items():
        # ---
        all_o = ta["green"] + ta["red"]
        # ---
        all_line += f'{all_o:,} || '
        # ---
        green_line += f'{ta["green"]:,} || '
        # ---
        red_line += f'{ta["red"]:,} || '
    # ---
    te_langs = f'\n{te_langs}\n\n'
    te_langs += '|- style="position: sticky;top: 0; z-index: 2;"\n! style="position: sticky;top: 0;left: 0;" | All'
    te_langs += f'\n| {all_line}\n\n'
    te_langs += '|- style="position: sticky;top: 0; z-index: 2;"\n! style="position: sticky;top: 0;left: 0;" | Green'
    te_langs += f'\n| {green_line}\n\n'
    te_langs += '|- style="position: sticky;top: 0; z-index: 2;"\n! style="position: sticky;top: 0;left: 0;" | Red'
    te_langs += f'\n| {red_line}'
    te_langs += '\n|}\n</div>'
    # ---
    text += te_langs
    # ---
    return text


def make_color(en_extlinks, en_refsname, p_ext, p_names, lead_extlinks, lead_refsname):
    # ---
    _sa_11 = False
    _sa_22 = False
    # ---
    # 1 match the en_extlinks
    _sa_1, same1 = match_p(en_extlinks, p_ext)
    # ---
    # 2 match the en_refsname
    _sa_2, same2 = match_p(en_refsname, p_names)
    # ---
    if not _sa_1 and not _sa_2 and 'nolead' not in sys.argv:
        # 3 match the lead_extlinks
        _sa_11, same11 = match_p(lead_extlinks, p_ext)
        # ---
        # 4 match the lead_refsname
        _sa_22, same22 = match_p(lead_refsname, p_names)
    # ---
    if _sa_1 or _sa_2 or _sa_11 or _sa_22:
        color = 'green'
    else:
        color = 'red'
        # ---
        for x, count in p_names.items():
            # print(f'{x}: {count}')
            if x.lower() in lead_refsname or x.lower() in en_refsname:
                if count > 6:
                    color = 'green'
                    same2 = count
                    print(f'ref {x}, count:{count}....')
                    break
        # ---
    # ---
    tab = {'same1': same1, 'same2': same2, 'color': color}
    # ---
    return tab


# ---
all_pages_states = {}


def log_all_pages_states():
    Dir = Path(__file__).parent
    file = f'{Dir}/all_pages_states.json'
    # ---
    if all_pages_states != {}:
        printe.output(f'<<lightyellow>> log_all_pages_states(): lenth: {len(all_pages_states.keys())}')
        json.dump(all_pages_states, codecs.open(file, 'w', encoding='utf-8'))

    # ---


# ---
log_all_pages_states()


def make_text(allo, ttt=''):
    # create wikitable from json
    # ---
    t_sections[ttt] = {}
    # ---
    t_sections[ttt]['en'] = len(allo.keys())
    # ---
    langs_keys = []
    # ---
    for en, ta in allo.items():
        if 'langs' in ta:
            langs_keys.extend(ta['langs'].keys())
        else:
            print(f'no langs for {en}, keys:{ta.keys()}')
    # ---
    langs_keys = [x.strip() for x in langs_keys if x.strip() != '']
    # ---
    langs_keys = sorted(set(langs_keys))
    # ---
    langs_keys_2 = {}
    # ---
    for en, ta in allo.items():
        for la in ta['langs']:
            la = la.strip()
            if la in ['en', '']:
                continue
            if la not in langs_keys_2:
                langs_keys_2[la] = 0
            langs_keys_2[la] += 1
    # ---
    # sort langs_keys_2 by number of references
    langs_keys_2 = sorted(langs_keys_2.items(), key=lambda x: x[1], reverse=True)
    # ---
    # print(langs_keys_2)
    # ---
    text = text_main

    # ---
    # Add the language keys to text separated by '!!'.
    # text += " !! ".join(langs_keys)

    def format_x(x):
        if len(x) < 4:
            return x
        # ---
        x2 = x.replace('-', '')
        x2 = x2[:3]
        # ---
        return "{{abbr|" + f"{x2}|{x}" + "}}"

    langs_keys_text = " !! ".join([format_x(x) for x in langs_keys])
    text += f" {langs_keys_text}"

    # ---
    n = 0
    # ---
    all_green = 0
    all_red = 0
    all_langlinks = 0
    # ---
    langs_green_red = {}
    # ---
    for en, ta in allo.items():
        # ---
        en_extlinks = [x.lower() for x in ta['extlinks']]
        en_refsname = [x.lower() for x in ta['refsname'].keys()]
        # ---
        lead = ta['lead']
        # ---
        lead_refsname = [x.lower() for x in lead['refsname'].keys()]
        lead_extlinks = [x.lower() for x in lead['extlinks']]
        # ---
        en = ta.get('en', en)
        langs = ta['langs']
        # ---
        if len(langs) == 0:
            print(f'{en}: no langs.....')
        # ---
        if en not in all_pages_states:
            all_pages_states[en] = {}
        # ---
        n += 1
        # ---
        if n > 100 and 'limit100' in sys.argv:
            break
        # ---
        lang_text = ''
        # ---
        for l in langs_keys:
            # ---
            if l not in all_langs_states:
                all_langs_states[l] = {'red': 0, 'green': 0}
            if l not in langs_green_red:
                langs_green_red[l] = {'red': 0, 'green': 0}
            # ---
            tit = langs.get(l, {}).get('title', '')
            # ---
            all_pages_states[en][l] = {'color': '', 'title': tit}
            # ---
            p_ext = langs.get(l, {}).get('extlinks', [])
            p_ext = [x.lower() for x in p_ext]
            # ---
            p_names = langs.get(l, {}).get('refsname', {})
            # ---
            tito = '|'
            # ---
            if l in langs:
                # ---
                all_langlinks += 1
                # ---
                color_tab = make_color(en_extlinks, en_refsname, p_ext, p_names, lead_extlinks, lead_refsname)
                # ---
                color = color_tab['color']
                # ---
                if color == 'red' and ta.get('old', {}) != {}:
                    # ---
                    old = ta['old']
                    # ---
                    old_lead = old['lead']
                    # ---
                    en_extlinks.extend([x.lower() for x in old['extlinks']])
                    en_extlinks = list(set(en_extlinks))
                    # ---
                    en_refsname.extend([x.lower() for x in old['refsname'].keys()])
                    en_refsname = list(set(en_refsname))
                    # ---
                    lead_refsname.extend([x.lower() for x in old_lead['refsname'].keys()])
                    lead_refsname = list(set(lead_refsname))
                    # ---
                    lead_extlinks.extend([x.lower() for x in old_lead['extlinks']])
                    lead_extlinks = list(set(lead_extlinks))
                    # ---
                    color_tab = make_color(en_extlinks, en_refsname, p_ext, p_names, lead_extlinks, lead_refsname)
                    # ---
                    color = color_tab['color']
                    # ---
                    if color == 'red':
                        # ---
                        en_extlinks_o = [x.lower() for x in old['extlinks']]
                        en_refsname_o = [x.lower() for x in old['refsname'].keys()]
                        lead_refsname_o = [x.lower() for x in old_lead['refsname'].keys()]
                        lead_extlinks_o = [x.lower() for x in old_lead['extlinks']]
                        # ---
                        color_tab2 = make_color(en_extlinks_o, en_refsname_o, p_ext, p_names, lead_extlinks_o, lead_refsname_o)
                        # ---
                        color = color_tab2['color']
                        # ---
                # ---
                if color == 'red':
                    translator = translators.tra_by_lang.get(l, {}).get(tit.lower(), '')
                    if translator != '':
                        color = 'green'
                        printe.output(f'<<purple>> change color for [[{l}:{tit}]] to green: {translator=}')
                # ---
                same1 = color_tab['same1']
                same2 = color_tab['same2']
                # ---
                all_pages_states[en][l]['color'] = color
                # ---
                if color == 'green':
                    color = '#c0fcc0'  # green
                    langs_green_red[l]['green'] += 1
                    all_langs_states[l]['green'] += 1
                    all_green += 1
                else:
                    langs_green_red[l]['red'] += 1
                    all_langs_states[l]['red'] += 1
                    all_red += 1
                    color = '#fcc0c0'  # red
                    # ---
                # ---
                same = f'{same1}/{same2}'
                # ---
                tito = f'[[:w:{l}:{tit}|{same}]]'
                # ---
                tito = f'| style="background-color:{color}" | {tito}'
            # ---
            # make background color
            # if
            lang_text += f'\n{tito}'
        # ---
        l_text = f'''
|-
! {n}
! style="position: sticky;left: 0;" | [[:en:{en}|{en}]]
! {len(en_extlinks)}/{len(en_refsname)}
! {len(lead_extlinks)}/{len(lead_refsname)}
{lang_text}
'''
        # ---
        text += l_text
        # ---
    text += '\n|}\n</div>'
    # ---
    te_langs = '''
<div style="width:100%;overflow-x:auto; overflow-y:auto">
{| class="wikitable sortable" style="width:100%;"
|- style="position: sticky;top: 0; z-index: 2;"
! style="position: sticky;top: 0;left: 0;" | key
!'''
    # ---
    te_langs += " !! ".join(langs_keys)
    # ---
    green_line = ''
    red_line = ''
    # ---
    for l, ta in langs_green_red.items():
        # ---
        green_line += f'{ta["green"]} || '
        # ---
        red_line += f'{ta["red"]} || '
    # ---
    te_langs = (
        f'''
{te_langs}

|- style="position: sticky;top: 0; z-index: 2;"
! style="position: sticky;top: 0;left: 0;" | green
| {green_line}

|- style="position: sticky;top: 0; z-index: 2;"
! style="position: sticky;top: 0;left: 0;" | red
| {red_line}
'''
        + '\n|}\n</div>'
    )
    # ---
    lrnn = len(allo.keys())
    # ---
    if all_langlinks == 0:
        all_langlinks = 1
    # ---
    faf = f'''
* all langlinks: {all_langlinks}
* all green: {all_green} ({round((all_green / all_langlinks) * 100, 2)}%)
* all red: {all_red} ({round((all_red / all_langlinks) * 100, 2)}%)

{te_langs}
=={ttt} ({lrnn})==
'''
    # ---
    t_sections[ttt]['green'] = all_green
    t_sections[ttt]['red'] = all_red
    # ---
    text = faf + text
    # ---
    if lrnn < 17:
        text = text.replace('height:580px;', '')
    # ---
    return text


# ---
