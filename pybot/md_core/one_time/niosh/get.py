'''
python pwb.py niosh/get write ask

python3 core8/pwb.py niosh/get write ask

'''
from new_api.mdwiki_page import MainPage as md_MainPage
import sys
from pathlib import Path
import json
import codecs

# ---
from mdpy import printe

# ---
Dir = Path(__file__).parent
Dird = f"{Dir}/downloads/"
Dird_js = f"{Dir}/downloads_js/"
# ---
cite_file = f"{Dird_js}/cite_all_links.json"
both_file = f"{Dir}/jsons/both.json"
# ---
data = json.load(open(cite_file))
# ---
boths = json.load(open(both_file))
# ---
# ---
by_url_all = {}
by_title_all = {}

all_pages = {}


def write_main():
    title = 'User:Mr. Ibrahem/niosh'
    text = ''
    # ---
    # sort all_pages
    all_pa = {x: v for x, v in sorted(all_pages.items(), key=lambda item: item[0].lower(), reverse=False)}
    # ---
    for x, tt in all_pa.items():
        text += f'* [[{tt}]]\n'

    page = md_MainPage(title, 'www', family='mdwiki')

    # Get the current text of the page.
    oldtext = page.get_text()
    exists = page.exists()
    if not exists:
        page.Create(text=text, summary='update')
    elif oldtext != text:
        page.save(newtext=text, summary='update', nocreate=0, minor='')


def write_to_mdwiki(data, x):
    if 'write' not in sys.argv:
        return
    wikitext = '''{| class="wikitable sortable"\n|-\n'''
    wikitext += '! # !! title !! urls\n|-\n'
    n = 0
    for k, v in data.items():
        if v:
            n += 1
            v = list(set(v))
            v_li = "\n* ".join(v)
            wikitext += f'|-\n| {n} || [[:en:{k}|{k}]] || \n* {v_li}\n'
    wikitext += "\n|-\n|}"
    # ---
    title = f'User:Mr. Ibrahem/niosh/{x}'
    all_pages[x] = title
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')

    # Get the current text of the page.
    oldtext = page.get_text()
    exists = page.exists()
    if not exists:
        page.Create(text=wikitext, summary='update')
    elif oldtext != wikitext:
        page.save(newtext=wikitext, summary='update', nocreate=0, minor='')


def run(x, urls):
    by_title = {}
    by_url = {}
    # ---
    urls_ = [x.lower() for x in urls]
    # ---
    for title, links in boths.items():
        ya = []
        for link in links:
            if link.lower() in urls_:
                ya.append(link)
                # ---
                if link not in by_url:
                    by_url[link] = []
                if link not in by_url_all:
                    by_url_all[link] = []
                # ---
                if title not in by_url[link]:
                    by_url[link].append(title)
                if title not in by_url_all[link]:
                    by_url_all[link].append(title)
        # ---
        if len(ya) > 0:
            by_title[title] = ya
        if title not in by_title_all:
            by_title_all[title] = ya
        else:
            by_title_all[title].extend(ya)
    # ---
    for _u in urls:
        if _u not in by_url:
            by_url[_u] = []
    # ---
    # sort by_url keys
    by_url = {k: v for k, v in sorted(by_url.items(), key=lambda item: item[0].lower(), reverse=False)}
    # ---
    file1 = f"{Dir}/by_title/{x}.json"
    # ---
    json.dump(by_title, codecs.open(file1, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    # ---
    printe.output(f'wrote {file1}')
    # ---
    file2 = f"{Dir}/by_url/{x}.json"
    # ---
    json.dump(by_url, codecs.open(file2, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    printe.output(f'wrote {file2}')
    # ---
    write_to_mdwiki(by_title, x)

    # ---


# ---
for x, urls in data.items():
    run(x, urls)
    # break
# ---
file3 = f"{Dir}/by_url/all.json"
# ---
json.dump(by_url_all, codecs.open(file3, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
printe.output(f'wrote {file3}')
# ---
file4 = f"{Dir}/by_title/all.json"
# ---
json.dump(by_title_all, codecs.open(file4, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
printe.output(f'wrote {file4}')
# ---
write_to_mdwiki(by_title_all, 'all')
# ---
write_main()
# ---
