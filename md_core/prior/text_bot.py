import pywikibot
import sys
#---
text_main = '''
<div style="height:580px;width:100%;overflow-x:auto; overflow-y:auto">

{| class="wikitable sortable" style="width:100%;background-color:#dedede"
|- style="position: sticky;top: 0; z-index: 2;"
! n
! style="position: sticky;top: 0;left: 0;" | en
!urls/refs
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
def make_text(allo):
    # create wikitable from json
    #---
    langs_keys = []
    #---
    for en, ta in allo.items():  langs_keys.extend(ta['langs'].keys())
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
    text = text_main
    #---
    text += " !! ".join(langs_keys)
    #text += " !! ".join([x for x, ta in langs_keys_2])
    #---
    n = 0
    #---
    for en, ta in allo.items():
        extlinks  = [ x.lower() for x in ta['extlinks'] ]
        refsname  = [ x.lower() for x in ta['refsname'] ]
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
        l_text = f'''
|-
! {n}
! style="position: sticky;left: 0;" | [[:en:{en}|{en}]]
! {len(extlinks)}/{len(refsname)}
'''
        #---
        for l in langs_keys:
        #for l, ta in langs_keys_2:
            #---
            tit     = langs.get(l, {}).get('title', '')
            #---
            p_ref   = langs.get(l, {}).get('extlinks', [])
            p_ref = [ x.lower() for x in p_ref ]
            #---
            p_names = langs.get(l, {}).get('refsname', [])    
            p_names = [ x.lower() for x in p_names ]
            #---
            tito = '|'
            #---
            if l in langs:
                #---
                color = '#fcc0c0'   # red
                #---
                _sa_, same1 = match_p(extlinks, p_ref)
                _sa_2, same2 = match_p(refsname, p_names)
                #---
                if _sa_ or _sa_2:
                    color = '#c0fcc0'   # green
                #---
                same = f'{same1}/{same2}'
                #---  
                tito = f'[[:{l}:{tit}|{same}]]'
                #---
                tito = f'| style="background-color:{color} | {tito}'
            #---
            # make background color
            # if 
            l_text += f'\n{tito}'
        #---
        text += l_text
        #---
    text += '\n|}\n</div>'
    #---
    return text
#---