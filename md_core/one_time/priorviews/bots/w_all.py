"""

python3 core8/pwb.py priorviews/langs -lang:ar ask
python3 core8/pwb.py priorviews/langs -lang:ar ask

"""
from priorviews.bots import helps
from new_api.mdwiki_page import MainPage as md_MainPage
from pathlib import Path

# ---
Dir = Path(__file__).parent
# ---
# ---
# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# helps.talk_url(lang, user, labl)


def make_by_lang(one_langs_only):
    tab2 = {}
    # ---
    for user, tab in one_langs_only.items():
        for lang, cunts in tab['by_lang'].items():
            if lang not in tab2:
                tab2[lang] = {
                    'list': {},
                    'all': 0
                }
            # ---
            tab2[lang]['all'] += cunts
            # ---
            # tab2[lang][user] = cunts
            # ---
            if cunts not in tab2[lang]['list']:
                tab2[lang]['list'][cunts] = []
            tab2[lang]['list'][cunts].append(user)
            # --
    # ---
    return tab2


def sect_text(lang, userstable):
    # ---
    sc2 = '{| class=wikitable sortable\n|-\n!count!!users\n|-\n'
    # ---
    lang_cunt = 0
    # ---
    for cunts, users in userstable.items():
        # ---
        for u in users:
            lang_cunt += cunts
        # ---
        users.sort()
        # ---
        usrs_line = ', '.join([helps.talk_url(lang, x, x) for x in users])
        # ---
        sc2 += f'\n! {cunts} \n| {usrs_line}\n|-'
        # ---
    # ---
    sc2 += '\n|}'
    seec = f'\n==={lang} ({lang_cunt})===\n{sc2}'
    # ---
    return seec


def work_all(translators_all):
    alllll = 0
    # ---
    # sort translators_all by count
    translators_a = {
        x: v
        for x, v in sorted(translators_all.items(), key=lambda item: item[1]['all'], reverse=True)
    }
    # ---
    all_usrs = len(translators_a.keys())
    # ---
    for x in translators_a.copy():
        # ---
        # skip user match ip address
        if helps.is_ip(x):
            del translators_a[x]
            continue
        # ---
        alllll += translators_a[x]['all']
    # ---
    one_langs_only = {
        x: v
        for x, v in translators_a.items() if len(v['by_lang']) == 1
    }
    multiple_langs = {
        x: v
        for x, v in translators_a.items() if len(v['by_lang']) > 1
    }
    # ---
    text = f"* all articles in the report: {alllll}\n"
    text += f"* all users in the report: {all_usrs}\n==multi langs==\n"
    # ---
    for x, v in multiple_langs.items():
        # ---
        text += f"\n# [[w:en:User talk:{x}|User:{x}]]: {v['all']}\n#*"
        bylang = v['by_lang']
        # sort by lang
        bylang = {
            o: v
            for o, v in sorted(bylang.items(), key=lambda item: item[1], reverse=True)
        }
        text += ", ".join([helps.talk_url(langg, x, langg) + f": {v}" for langg, v in bylang.items()])
        # ---
    # ---
    seec = '\n\n==by lang==\n\n'
    # ---
    langs_a = make_by_lang(one_langs_only)
    # ---
    # sort langs_a by count
    langs_a = {
        x: v
        for x, v in sorted(langs_a.items(), key=lambda item: item[1]['all'], reverse=True)
    }
    # ---
    for lang, users in langs_a.items():
        # ---
        seec += sect_text(lang, users['list'])
        # ---
    # ---
    text += seec
    # ---
    page = md_MainPage('User:Mr. Ibrahem/priorviews/translators', 'www', family='mdwiki')
    exists = page.exists()
    oldtext = page.get_text()
    if not exists:
        page.Create(text=text, summary='update')
    elif oldtext != text:
        # ---
        page.save(newtext=text, summary='update', nocreate=1, minor='')


# ---
