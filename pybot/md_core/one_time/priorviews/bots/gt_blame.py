'''

python3 core8/pwb.py priorviews/bots/gt_blame

'''
import sys
import re
from urllib.parse import urlencode
import requests
import wikitextparser
from mdpy import printe

# ---
# ---
from prior.json_langs.lists import json_langs_by_langs

# tab = json_langs_by_langs.get(lang, {}).get(title, {})# {'extlinks': extlinks, 'refsname': refsname}
# ---
from prior.json_en.lists import json_en_all

# tab = json_en_all.get(en, {})# {'extlinks': extlinks, 'refsname': refsname}
# ---
from priorviews.bots import helps

# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)


def match_ref_names(r, refnames, lang):
    # dict_keys(['revid', 'parentid', 'user', 'timestamp', 'contentformat', 'contentmodel', 'content', 'comment'])
    text_pp = r.get('content')
    user = r.get('user')
    # ---
    if not text_pp:
        return ''
    if not user:
        return ''
    # ---
    parsed = wikitextparser.parse(text_pp)
    tags = parsed.get_tags()
    # ---
    _tags_ = {}
    # ---
    for x in tags:
        if not x or not x.name:
            continue
        if x.name != 'ref':
            continue
        # ---
        attrs = x.attrs
        name = attrs.get('name', '').replace('/', '').lower().strip()
        if name == '':
            continue
        # ---
        contents = x.contents
        # ---
        if re.sub(r'[:\d\s]+', '', name) == '':
            continue
        # ---
        if name not in _tags_:
            _tags_[name] = 0
        # ---
        _tags_[name] += 1
    # ---
    # sort by count
    _tags_ = {k: v for k, v in sorted(_tags_.items(), key=lambda item: item[1], reverse=True)}
    for k, v in _tags_.items():
        if k in refnames:
            printe.output(f'<<green>> find: {k=} count: {v=}| main: {refnames[k]=}')
            printe.output(f'https://{lang}.wikipedia.org/w/index.php?diff=prev&oldid={r["revid"]}')
            printe.output(f'new user: {user}')
            return user
    # ---
    return ''


# ---


class FindInHistory:
    def __init__(self, title, lang="en", refname=[], extlinks=[]):
        # ---
        self.lang = lang
        self.title = title
        self.url = 'https://' + self.lang + '.wikipedia.org/w/api.php'
        self.author = ''
        # ---
        self.revisions = []
        self.refname = refname
        self.extlinks = extlinks
        # ---
        self.session = requests.Session()
        # ---
        self.start()

    def post_to_json(self, params):
        json1 = {}
        # ---
        unurl = f"{self.url}?{urlencode(params)}"
        # ---
        if "printurl" in sys.argv and "text" not in params:
            printe.output(f"post_to_json:\t\t{unurl}")
        # ---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        # ---
        return json1

    def post_continue(self, params, action, _p_, p_empty):
        # ---
        continue_params = {}
        # ---
        results = p_empty
        # ---
        while continue_params != {} or len(results) == 0:
            # ---
            if continue_params:
                params = {**params, **continue_params}
            # ---
            json1 = self.post_to_json(params)
            # ---
            if not json1 or json1 == {}:
                break
            # ---
            continue_params = json1.get("continue", {})
            # ---
            data = json1.get(action, {}).get(_p_, p_empty)
            # ---
            if not data:
                break
            # ---
            printe.output(f'post_continue, len:{len(data)}, all: {len(results)}')
            # ---
            if isinstance(results, list):
                results.extend(data)
            else:
                results = {**results, **data}
        # ---
        return results

    def get_revisions(self, title):
        params = {"action": "query", "format": "json", "prop": "revisions", "titles": title, "utf8": 1, "formatversion": "2", "rvprop": "comment|timestamp|user|content|ids", "rvdir": "newer", "rvstart": "2011-01-01T00:00:00.000Z", "rvend": "2018-01-01T00:00:00.000Z", "rvlimit": "max"}
        # ---
        pages = self.post_continue(params, "query", "pages", [])
        # ---
        return pages

    def start(self):
        pages = self.get_revisions(self.title)
        for p in pages:
            for r in p.get("revisions", []):
                if r.get('anon'):
                    continue
                self.revisions.append(r)


def search_history(title, lang, en='', refname=[], extlinks=[]):
    # ---
    tab = {"lang": lang, "article": title, "needle": ""}
    # ---
    if refname == [] or extlinks == []:
        infos = json_langs_by_langs.get(lang, {}).get(title)  # {'extlinks': extlinks, 'refsname': refsname}
        # ---
        if not infos:
            return ''
        # ---
        en = infos.get('en', '')
        refname = infos.get('refsname')
        extlinks = infos.get('extlinks')
    # ---
    en_refname = []
    en_extlinks = []
    # ---
    if en != '':
        tab = json_en_all.get(en, {})
        en_refname = tab.get('refsname', [])
        en_extlinks = tab.get('extlinks', [])
    # ---
    bot = FindInHistory(title, lang, refname, extlinks)
    revisions = bot.revisions
    # ---
    # sort revisions by timestamp
    revisions.sort(key=lambda r: r.get('timestamp', ''))
    # ---
    lenth_before = len(revisions)
    # ---
    # skip bots
    revisions = [rev for rev in revisions if not rev.get('user', '').lower().endswith('bot')]
    # ---
    bots_lenth = lenth_before - len(revisions)
    # ---
    print(f'len of revisions: {len(revisions)}, bots_lents: {bots_lenth}')
    # ---
    for r in revisions:
        # print(r.keys())
        # dict_keys(['revid', 'parentid', 'user', 'timestamp', 'contentformat', 'contentmodel', 'content', 'comment'])
        # ---
        timestamp = r.get('timestamp', '')
        text_pp = r.get('content')
        user = r.get('user')
        # ---
        if not text_pp:
            continue
        if not user:
            continue
        # print(timestamp)
        # ---
        if user.lower().endswith('bot'):
            print(f'skip bots {user}...')
            continue
        # ---
        comment = r.get('comment')
        if comment:
            comment_v = helps.isv(comment)
            if comment_v:
                printe.output(f'<<green>> find: {comment_v=}')
                return user
        # ---
        rs = match_ref_names(r, refname, lang)
        # ---
        if rs != '':
            return rs
    # ---
    # print(f'len of revisions: {len(revisions)}')
    # ---
    return ''


# ---
if __name__ == '__main__':
    # ---
    t = search_history('نكاف', "ar")
    print(f'au: {t}')
    sys.exit()
    # ---
