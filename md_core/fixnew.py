"""
python3 core8/pwb.py fixnew

bot to find errors like:
* https://mdwiki.org/w/index.php?diff=1370771
* https://mdwiki.org/w/index.php?diff=1371108

"""
import re
import sys

# ---
from mdpy import printe
from new_api.mdwiki_page import MainPage as md_MainPage, NEW_API

# ---
api_new = NEW_API('www', family='mdwiki')
api_new.Login_to_wiki()

with_err = {}


def search_history(page):
    # ---
    revisions = page.get_revisions(rvprops=['content'])
    # ---
    print(f'len revisions: {len(revisions)}')
    # ---
    # sort revisions by timestamp
    revisions.sort(key=lambda r: r.get('timestamp', ''), reverse=True)
    # ---
    for r in revisions:
        # ---
        # print(r.keys())
        # dict_keys(['revid', 'parentid', 'user', 'anon', 'timestamp', 'slots', 'comment'])
        # ---
        revid = r.get('revid', '')
        # timestamp = r.get('timestamp', '')
        # ---
        content = r.get("slots", {}).get("main", {}).get("content", '')
        # ---
        # {'revid': 1372622, 'parentid': 1356296, 'user': 'Mr. Ibrahem', 'timestamp': '2023-10-14T17:58:14Z', 'comment': ''}
        # ---
        if not content:
            continue
        # ---
        fi = re.search(r'\{\{\s*\|', content)
        if fi:
            # ---
            del r["slots"]
            print(r)
            # ---
            printe.output(f'<<red>> {page.title} has err')
            return revid
    # ---
    return ''


def work_on_title(title):
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        return
    # ---
    text = page.get_text()
    # ---
    if text == "":
        printe.output("<<red>> notext")
        return
    # ---
    # find if text has {{|
    # ---
    fi = re.search(r'\{\{\s*\|', text)
    if fi:
        printe.output(f'<<red>> {title} has err')
        with_err[title] = search_history(page)


def main(listen=[]):
    # ---
    user = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        if arg == "-user":
            user = value
    # ---
    if not listen:
        if user != "":
            listen = api_new.UserContribs(user, limit=5000, namespace="0", ucshow="new")
        else:
            listen = api_new.Get_All_pages(start='!', namespace='0')
    # ---
    for n, page in enumerate(listen):
        printe.output(f'<<yellow>> n:{n}, title:{page}')
        work_on_title(page)
    # ---
    if with_err:
        page = md_MainPage('User:Mr. Ibrahem/err', 'www', family='mdwiki')
        text = '\n'.join([f'# [[{title}]]: [[Special:diff/{rev}|Diff]]' for title, rev in with_err.items()])
        page.save(newtext=text, summary='err', nocreate=0, minor='')


if __name__ == "__main__":
    listen = []
    # ---
    if 'test' in sys.argv:
        listen = ['User:Mr. Ibrahem/sandbox']
    # ---
    main(listen)
