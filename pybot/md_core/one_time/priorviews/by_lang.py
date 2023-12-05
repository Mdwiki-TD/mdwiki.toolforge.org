"""

python3 core8/pwb.py priorviews/by_lang ask

"""
from priorviews.lists import translators
from priorviews.lists.creators_to_translators import creators_as_translators
from pathlib import Path

# ---
from priorviews.lists import words
from priorviews.lists import views
from new_api.mdwiki_page import MainPage as md_MainPage

# ---
Dir = Path(__file__).parent
# ---
# translators.tra_by_lang
# ---
total_views = 0
# ---
te_langs = '''
== All languages ==
{| class="wikitable sortable"
! style="position: sticky;top: 0;left: 0;" | #
! style="position: sticky;top: 0;left: 0;" | Language
! style="position: sticky;top: 0;left: 0;" | Translations
! style="position: sticky;top: 0;left: 0;" | With Translator
! style="position: sticky;top: 0;left: 0;" | Views
! style="position: sticky;top: 0;left: 0;" | Words
'''
# ---
by_lang_tra = views.count_tra_by_lang
by_lang = views.count_views_by_lang.copy()
# ---
# sort by_lang
keys_1 = {x: v for x, v in sorted(by_lang.items(), key=lambda item: item[1], reverse=True)}
# ---
total_tra = 0
with_trator = 0
total_wrds = 0
# ---
mm = 0
# ---
for l, vv in keys_1.items():
    # ---
    if l == "en":
        continue
    # ---
    mm += 1
    # ---
    total_views += vv
    # ---
    # with translators
    # ---
    trator = translators.counts_by_lang.get(l, 0) + len(creators_as_translators.get(l, {}))
    with_trator += trator
    # ---
    tra = by_lang_tra.get(l, 0)
    total_tra += tra
    # ---
    wrds = words.count_words_by_lang.get(l, 0)
    total_wrds += wrds
    # ---
    te_langs += f'\n|-\n| {mm} || [[/{l}|{l}]] || {tra:,}  || {trator:,} || {vv:,} || {wrds:,}'
# ---
te_langs += f"\n|-\n! || Total || {total_tra:,} || {with_trator:,} || {total_views:,} || {total_wrds:,} \n|-"
te_langs += "\n|}"
# ---
en_views = keys_1.get("en", 0)
# ---
newtext = ''
# ---
'''
newtext += f';Views (from July 2015 to June 2023):\n'
newtext += f'* Total views: {total_views:,}\n'
newtext += f'* Total words: {total_wrds:,}\n'
newtext += f'* Total translations: {total_tra:,}\n'
newtext += f'* Enwiki Views: {en_views:,}\n'
newtext += te_langs
'''
# ---
newtext += te_langs
# ---
if __name__ == "__main__":
    page = md_MainPage('User:Mr. Ibrahem/priorviews/bylang', 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        create = page.Create(text=newtext, summary='update')
    else:
        # ---
        text = page.get_text()
        save_page = page.save(newtext=newtext, summary='update', nocreate=1, minor='')
    # ---
