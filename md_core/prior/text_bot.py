import pywikibot
from prior import get_them
import sys
#---
text_main = '''
<div style="height:580px;width:100%;overflow-x:auto; overflow-y:auto">

{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! n
! style="position: sticky;top: 0;left: 0;" | en
!urls/refs
!lead<br>urls/refs
!'''
#---
def match_p(refs, p_ref):
    # Find all the elements that are common between `p_ref` and `refs`
    same = [x for x in p_ref if x in refs]

    len_same = len(same)
    len_refs = len(refs)

    # If there are no common elements between `p_ref` and `refs`, return False and the length of `same`
    if len_same < 1:    return False, len_same

    # If the length of `same` is less than 9 or less than half the length of `refs` minus 1,
    # return False and the length of `same`
    if 9 > len_same < ((len_refs/2)-1): 
        return False, len_same

    # Otherwise, return True and the length of `same`
    return True, len_same
#---
t_sections = {}
#---
def get_t_sections():
    # This function generates a wikitext table of statistics for different sections
    # The table has the following columns: section, en, all langlinks, green, red

    # Initialize the table with headings for each column
    text = '''
{| class="wikitable sortable"
|- 
! section
! en
! all langlinks
! green
! red
|- 
'''

    # Initialize variables to keep track of the total values for each column
    all_en = 0
    all_all = 0
    all_green = 0
    all_red = 0

    # Loop over each section and add a row to the table with statistics for that section
    for k, tt in t_sections.items():
        # Calculate the total number of green and red links for this section
        all = tt['green'] + tt['red']

        # Add the values for this section to the total values for each column
        all_en += tt['en']
        all_all += all
        all_green += tt['green']
        all_red += tt['red']

        # Add a row to the table with statistics for this section
        text += f'! [[User:Mr. Ibrahem/prior/{k}|{k}]]\n'
        text += '| ' + str(tt['en']) + '\n'
        text += '| ' + str(all) + '\n'
        text += '| ' + str(tt['green']) + '\n'
        text += '| ' + str(tt['red']) + '\n'
        text += '|-\n'

    # Add a final row to the table with the total values for each column
    text += f'''! total\n! {all_en}\n! {all_all}\n! {all_green}\n! {all_red}\n''' + '|}'

    # Return the completed table as a string
    return text
#---
def make_color(en_extlinks, en_refsname, p_ext, p_names, lead_extlinks, lead_refsname):
    #---
    _sa_11 = False
    _sa_22 = False
    #---
    # 1 match the en_extlinks
    _sa_1, same1 = match_p(en_extlinks, p_ext)
    #---
    # 2 match the en_refsname
    _sa_2, same2 = match_p(en_refsname, p_names)
    #---
    if not _sa_1 and not _sa_2 and not 'nolead' in sys.argv:
        # 3 match the lead_extlinks
        _sa_11, same11 = match_p(lead_extlinks, p_ext)
        #---
        # 4 match the lead_refsname
        _sa_22, same22 = match_p(lead_refsname, p_names)
    #---
    if _sa_1 or _sa_2 or _sa_11 or _sa_22:
        color = 'green'
    else:
        color = 'red'
        #---
        for x, count in p_names.items():
            # print(f'{x}: {count}')
            if x.lower() in lead_refsname or x.lower() in en_refsname:
                if count > 8:
                    color = 'green'
                    same2 = count
                    print(f'ref {x}, count:{count}....')
                    break
        #---
    #---
    tab = {'same1':same1, 'same2':same2, 'color':color}
    #---
    return tab
#---
def make_text(allo, ttt=''):
    # create wikitable from json
    #---
    t_sections[ttt] = {}
    #---
    t_sections[ttt]['en'] = len(allo.keys())
    #---
    langs_keys = []
    #---
    for en, ta in allo.items():
        if 'langs' in ta:
            langs_keys.extend(ta['langs'].keys())
        else:
            print(f'no langs for {en}, keys:{ta.keys()}')
    #---
    langs_keys = [ x.strip() for x in langs_keys if x.strip() != '']
    #---
    langs_keys = list(set(langs_keys))
    langs_keys.sort()
    #---
    langs_keys_2 = {}
    #---
    for en, ta in allo.items():
        for la in ta['langs']:
            la = la.strip()
            if la in ['en', '']: continue
            if not la in langs_keys_2: langs_keys_2[la] = 0
            langs_keys_2[la] += 1
    #---
    # sort langs_keys_2 by number of references
    langs_keys_2 = sorted(langs_keys_2.items(), key=lambda x: x[1], reverse=True)
    #---
    # print(langs_keys_2)
    #---
    text       = text_main
    #---
    text += " !! ".join(langs_keys)
    #text += " !! ".join([x for x, ta in langs_keys_2])
    #---
    n = 0
    #---
    all_green = 0
    all_red = 0
    #---
    langs_green_red = {}
    #---
    for en, ta in allo.items():
        #---
        en_extlinks  = [ x.lower() for x in ta['extlinks'] ]
        #---
        # if not 'nofilter' in sys.argv:  en_extlinks  = get_them.filter_urls(en_extlinks)
        #---
        en_refsname  = [ x.lower() for x in ta['refsname'].keys() ]
        # en_refsname  = ta['refsname']
        #---
        lead = ta['lead']
        #---
        lead_refsname = [ x.lower() for x in lead['refsname'].keys() ]
        # lead_refsname = lead['refsname']
        #---
        lead_extlinks = [ x.lower() for x in lead['extlinks'] ]
        #---
        en    = ta.get('en', en)
        langs = ta['langs']
        #---
        if len(langs) == 0 :
            print(f'{en}: no langs.....')
        #---
        n += 1
        #---
        # print(f'a {n}/{len(allo)}:')
        #---
        if n > 100 and 'limit100' in sys.argv: break
        #---
        lang_text = ''
        #---
        for l in langs_keys:
        #for l, ta in langs_keys_2:
            #---
            if not l in langs_green_red: langs_green_red[l] = {'red' : 0, 'green' : 0}
            #---
            tit     = langs.get(l, {}).get('title', '')
            #---
            p_ext   = langs.get(l, {}).get('extlinks', [])
            p_ext = [ x.lower() for x in p_ext ]
            #---
            # if not 'nofilter' in sys.argv:  p_ext  = get_them.filter_urls(p_ext)
            #---
            p_names = langs.get(l, {}).get('refsname', {})
            # p_names = [ x.lower() for x in p_names ]
            #---
            tito = '|'
            #---
            if l in langs:
                #---
                color_tab = make_color(en_extlinks, en_refsname, p_ext, p_names, lead_extlinks, lead_refsname)
                #---
                if color_tab['color'] == 'red' and ta.get('old', {}) != {}:
                    #---
                    old = ta['old']
                    #---
                    old_lead = old['lead']
                    #---
                    # en_extlinks  = [ x.lower() for x in old['extlinks'] ]
                    # en_refsname  = [ x.lower() for x in old['refsname'].keys() ]
                    # lead_refsname = [ x.lower() for x in old_lead['refsname'].keys() ]
                    # lead_extlinks = [ x.lower() for x in old_lead['extlinks'] ]
                    #---
                    en_extlinks.extend([ x.lower() for x in old['extlinks'] ])
                    en_extlinks = list(set(en_extlinks))
                    #---
                    en_refsname.extend([ x.lower() for x in old['refsname'].keys() ])
                    en_refsname = list(set(en_refsname))
                    #---
                    lead_refsname.extend([ x.lower() for x in old_lead['refsname'].keys() ])
                    lead_refsname = list(set(lead_refsname))
                    #---
                    lead_extlinks.extend([ x.lower() for x in old_lead['extlinks'] ])
                    lead_extlinks = list(set(lead_extlinks))
                    #---
                    color_tab = make_color(en_extlinks, en_refsname, p_ext, p_names, lead_extlinks, lead_refsname)
                #---
                same1 = color_tab['same1']
                same2 = color_tab['same2']
                color = color_tab['color']
                #---
                if color == 'green':
                    color = '#c0fcc0'   # green
                    langs_green_red[l]['green'] += 1
                    all_green += 1
                else:
                    langs_green_red[l]['red'] += 1
                    all_red += 1
                    color = '#fcc0c0'   # red
                    #---
                #---
                same = f'{same1}/{same2}'
                #---  
                tito = f'[[:{l}:{tit}|{same}]]'
                #---
                tito = f'| style="background-color:{color}" | {tito}'
            #---
            # make background color
            # if 
            lang_text += f'\n{tito}'
        #---
        l_text = f'''
|-
! {n}
! style="position: sticky;left: 0;" | [[:en:{en}|{en}]]
! {len(en_extlinks)}/{len(en_refsname)}
! {len(lead_extlinks)}/{len(lead_refsname)}
{lang_text}
'''
        #---
        text += l_text
        #---
    text += '\n|}\n</div>'
    #---
    te_langs = '''
<div style="width:100%;overflow-x:auto; overflow-y:auto">
{| class="wikitable sortable" style="width:100%;"
|- style="position: sticky;top: 0; z-index: 2;"
! style="position: sticky;top: 0;left: 0;" | key
!'''
#---
    te_langs += " !! ".join(langs_keys)
    #---
    green_line = ''
    red_line   = ''
    #---
    for l, ta in langs_green_red.items():
        #---
        green_line += f'{ta["green"]} || '
        #---
        red_line   += f'{ta["red"]} || '
    #---
    te_langs = f'''
{te_langs}

|- style="position: sticky;top: 0; z-index: 2;"
! style="position: sticky;top: 0;left: 0;" | green
| {green_line}

|- style="position: sticky;top: 0; z-index: 2;"
! style="position: sticky;top: 0;left: 0;" | red
| {red_line}
'''
    #---
    faf = f'''
* all_red: {all_red}
* all_green: {all_green}
'''
    #---
    t_sections[ttt]['green'] = all_green
    t_sections[ttt]['red']   = all_red
    #---
    text = faf + "\n" + te_langs + "\n|}\n</div>\n" + text
    #---
    return text
#---