'''
# ---
from priorviews.lists import words
# words.words_by_lang
# words.count_words_by_lang
# ---
python3 core8/pwb.py priorviews/words

'''
import json
import os
from pathlib import Path
import codecs

# ---
Dir = Path(__file__).parent
# ---
file = f'{Dir}/words_mdwiki_langs.json'
# ---
if not os.path.exists(file):
    with open(file, 'w') as f:
        json.dump({}, f)
# ---
words_by_lang = json.load(codecs.open(file, 'r', 'utf-8'))
# ---
_data = {"ar": {"artitle": 0, "artitle2": 0}}
# ---
count_words_by_lang = {}
# ---
# Iterate through each markdown file and language in `words_by_lang`
for lang, titles in words_by_lang.items():
    # ---
    if lang not in count_words_by_lang:
        count_words_by_lang[lang] = 0
    # ---
    for title, words in titles.items():
        count_words_by_lang[lang] += words
# ---
if __name__ == '__main__':
    for x, wo in count_words_by_lang.items():
        print(x, wo)
    # ---
    print(f'len of count_words_by_lang: {len(count_words_by_lang)}')
    # ---
    print(f'len of words_by_lang: {len(words_by_lang)}')
    for lang, titles in words_by_lang.items():
        for title, words in titles.items():
            print(lang, title, words)

# ---
