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
    #---
    same = [ x for x in p_ref if x in refs ]
    len_same = int(len(same))
    #---
    len_refs = int(len(refs))
    #---
    if len_same < 1: return False, len_same
    if 9 > len_same < ((len_refs/2)-1): return False, len_same
    #---
    return True, len_same
#---
t_sections = {}
#---
def get_t_sections():
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
    #---
    all_en = 0
    all_all = 0
    all_green = 0
    all_red = 0
    #---
    for k, tt in t_sections.items():
        #---
        all = tt['green'] + tt['red']
        #---
        all_en += tt['en']
        all_all += all
        all_green += tt['green']
        all_red += tt['red']
        #---
        text += f'! [[User:Mr. Ibrahem/prior/{k}|{k}]]\n'
        text += '| ' + str(tt['en']) + '\n'
        text += '| ' + str(all) + '\n'
        text += '| ' + str(tt['green']) + '\n'
        text += '| ' + str(tt['red']) + '\n'
        text += '|-\n'
    #---
    text += f'''! total\n! {all_en}\n! {all_all}\n! {all_green}\n! {all_red}\n''' + '|}'
    #---
    return text
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
        extlinks  = [ x.lower() for x in ta['extlinks'] ]
        #---
        # if not 'nofilter' in sys.argv:  extlinks  = get_them.filter_urls(extlinks)
        #---
        refsname  = [ x.lower() for x in ta['refsname'].keys() ]
        #---
        lead = ta['lead']
        lead_refsname = [ x.lower() for x in lead['refsname'].keys() ]
        lead_extlinks = [ x.lower() for x in lead['extlinks'] ]
        #---
        en    = ta.get('en', en)
        langs = ta['langs']
        #---
        if len(langs) == 0 :
            pywikibot.output(f'{en}: no langs.....')
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
            p_ref   = langs.get(l, {}).get('extlinks', [])
            p_ref = [ x.lower() for x in p_ref ]
            #---
            # if not 'nofilter' in sys.argv:  p_ref  = get_them.filter_urls(p_ref)
            #---
            p_names = langs.get(l, {}).get('refsname', {})
            p_names = [ x.lower() for x in p_names ]
            #---
            tito = '|'
            #---
            if l in langs:
                #---
                color = '#fcc0c0'   # red
                #---
                _sa_11 = False
                _sa_22 = False
                #---
                _sa_1, same1 = match_p(extlinks, p_ref)
                _sa_2, same2 = match_p(refsname, p_names)
                #---
                if not _sa_1 and not _sa_2 and not 'newnew' in sys.argv:
                    _sa_11, same11 = match_p(lead_extlinks, p_ref)
                    _sa_22, same22 = match_p(lead_refsname, p_names)
                #---
                if _sa_1 or _sa_2 or _sa_11 or _sa_22:
                    color = '#c0fcc0'   # green
                    langs_green_red[l]['green'] += 1
                    all_green += 1
                else:
                    langs_green_red[l]['red'] += 1
                    all_red += 1
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
! {len(extlinks)}/{len(refsname)}
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