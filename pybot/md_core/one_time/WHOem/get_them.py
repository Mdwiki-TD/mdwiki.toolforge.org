'''

'''
import sys
import re
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import urlencode
import requests
import wikitextparser
from mdpy import printe

# ---
'''
# ---
from WHOem import get_them
tt = get_them.work_in_one_lang_link()
# ---
'''
# ---
change_codes = {
    "bat_smg": "bat-smg",
    "be_x_old": "be-tarask",
    "be-x-old": "be-tarask",
    "cbk_zam": "cbk-zam",
    "fiu_vro": "fiu-vro",
    "map_bms": "map-bms",
    "nds_nl": "nds-nl",
    "roa_rup": "roa-rup",
    "zh_classical": "zh-classical",
    "zh_min_nan": "zh-min-nan",
    "zh_yue": "zh-yue",
}


def url_parser(url):
    parts = urlparse(url)
    directories = parts.path.strip('/').split('/')
    queries = parts.query.strip('&').split('&')
    # ---
    queries1 = {}
    # x.split('=')[0] : x.split('=')[1] for x in queries
    # ---
    for q in queries:
        if '=' not in q:
            continue
        k, sep, v = q.partition('=')
        queries1[k] = v
        # https://webcache.googleusercontent.com/search?hl=fr&q=cache:https://books.google.fr/books?id=faunzyqrhtgc&pg=pa47&vq=pancréas+mucoviscidose&dq=physiologie+humaine&source=gbs_search_r&cad=0_1&sig=564mkm4lqqdqy18ukodcuyffamm
    # ---
    elements = {
        'scheme': parts.scheme,
        'netloc': parts.netloc,
        'path': parts.path,
        'params': parts.params,
        'query': parts.query,
        'fragment': parts.fragment,
        'directories': directories,
        'queries': queries1,
    }

    return elements


def filter_urls(links):
    # ---
    liste1 = []
    # ---
    # delete link like web.archive.org
    for x in links:
        # ---
        if x.startswith('//'):
            x = 'https:' + x
        # ---
        x = x.replace('//www.', '//').replace('http://', 'https://')
        # ---
        # un urlencode
        # x = x.replace('%3A', ':').replace('%2F', '/').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
        x = urllib.parse.unquote(x)
        # ---
        x = x.replace('//www.', '//').replace('http://', 'https://')
        # https://web.archive.org/web/20100724032458/https://nlm.nih.gov/medlineplus/druginfo/natural/patient-riboflavin.html
        if 'web.archive.org' in x:
            # match https://web.archive.org/web/20230123155031 and delete it
            x = re.sub(r'^https://web\.archive\.org/web/[\d]+/', '', x)
        elif 'archive.org/details' in x:
            # https://archive.org/details/masterdentistry0000unse/page/180
            x = x.split('/page')[0]
        # ---
        if 'archive.is' in x:
            x = re.sub(r'^https://[\w]+\.archive\.is/[\d]+/', '', x)
        x = x.replace('//www.', '//').replace('http://', 'https://')
        # ---
        if 'googleusercontent' in x:
            x = re.sub(r'^https://.*?googleusercontent.*?http', 'http', x)
        # ---
        x = re.sub(r'^http.*?https://books', 'https://books', x)
        # ---
        # https://books.google.ca/books?id=JaOoXdSlT9sC&pg=PA11
        if 'books.google' in x and 'books' not in sys.argv:
            # ---
            prased = url_parser(x)
            # {'scheme': 'https', 'netloc': 'books.google.ca', 'path': '/books', 'queries': {'id': 'JaOoXdSlT9sC', 'pg': 'PA11'}}
            # ---
            x = re.sub(prased['netloc'], 'books.google.com', x)
            book_id = prased['queries'].get('id', '')
            if book_id != '':
                x2 = f'https://books.google.com/books?id={book_id}'
                if x2 != x:
                    # printe.output('<<yellow>> google books + 1')
                    x = x2
        # ---
        liste1.append(x.lower())
    # ---
    # remove duplicates
    liste1 = sorted(set(liste1))
    # ---
    # ---
    return liste1


# ---


class work_in_one_lang_link:
    def __init__(self, lang, title):
        self.lang = change_codes.get(lang) or lang
        # ---
        self.title = title
        self.url = 'https://' + self.lang + '.wikipedia.org/w/api.php'
        self.text = ''
        self.section0 = ''
        self.lead = {'extlinks': [], 'refsname': {}}
        self.extlinks = []
        self.refsname = {}
        self.contents_all = {}
        # ---
        self.session = requests.Session()
        # ---
        self.start()

    def start(self):
        self.get_text()
        # ---
        self.get_extlinks()
        # ---
        parsed = wikitextparser.parse(self.text)
        tags = parsed.get_tags()
        # ---
        self.refsname = self.get_ref_names(tags)
        # ---
        self.get_expended()
        # ---
        if self.lang == 'en':
            self.get_lead()

    def post_to_json(self, params):
        json1 = {}
        # ---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        # ---
        return json1

    def expandtemplates(self, text):
        # ---
        params = {"action": "expandtemplates", "format": "json", "text": text, "prop": "wikitext", "formatversion": "2"}
        # ---
        data = self.post_to_json(params)
        # ---
        newtext = data.get("expandtemplates", {}).get("wikitext") or text
        # ---
        return newtext

    def get_expended(self):
        # ---
        text_pp = self.expandtemplates(self.text)
        parsed = wikitextparser.parse(text_pp)
        tags = parsed.get_tags()
        # ---
        refsn = self.get_ref_names(tags)
        # ---
        refsn = {k: v for k, v in refsn.items() if k not in self.refsname}
        # ---
        if len(refsn) > 0:
            printe.output(f' new refsn: {len(refsn)}')
            printe.output(refsn)
            # ---
            self.refsname.update(refsn)

    def get_ref_names(self, tags):
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
            # ---
            if name == '':
                continue
            # ---
            contents = x.contents
            # ---
            if contents != '':
                self.contents_all[name] = str(x)
            # ---
            if re.sub(r'[:\d\s]+', '', name) == '':
                continue
            # ---
            if name not in _tags_:
                _tags_[name] = 0
            # ---
            _tags_[name] += 1
        # ---
        return _tags_

    def get_text(self):
        params = {"action": "parse", "format": "json", "prop": "wikitext", "page": self.title, "utf8": 1}
        # ---
        json1 = self.post_to_json(params)
        # ---
        self.text = json1.get('parse', {}).get('wikitext', {}).get('*', '')

    def get_extlinks(self):
        params = {"action": "query", "format": "json", "prop": "extlinks", "titles": self.title, "formatversion": "2", "utf8": 1, "ellimit": "max"}
        # ---
        elcontinue = 'x'
        # ---
        links = []
        # ---
        while elcontinue != '':
            # ---
            if elcontinue not in ['x', '']:
                params['elcontinue'] = elcontinue
            # ---
            json1 = self.post_to_json(params)
            # ---
            elcontinue = json1.get('continue', {}).get('elcontinue', '')
            # ---
            linkso = json1.get('query', {}).get('pages', [{}])[0].get('extlinks', [])
            # ---
            links.extend(linkso)
        # ---
        links = [x['url'] for x in links]
        # ---
        # remove duplicates
        liste1 = sorted(set(links))
        # ---
        # ---
        if 'nofilter' not in sys.argv:
            liste1 = filter_urls(liste1)
        # ---
        self.extlinks = liste1

    def get_lead(self):
        # ---
        parsed = wikitextparser.parse(self.text)
        # ---
        section0 = parsed.get_sections(level=0)[0].contents
        self.section0 = section0
        # ---
        section0_pa = wikitextparser.parse(self.section0)
        # ---
        tags0 = section0_pa.get_tags()
        # ---
        self.make_new_text(tags0)
        # ---
        # printe.showDiff(section0, self.section0)
        # ---
        self.lead['refsname'] = self.get_ref_names(tags0)
        self.lead['extlinks'] = self.get_lead_extlinks()

    def get_lead_extlinks(self):
        params = {"action": "parse", "format": "json", "title": self.title, "text": self.section0, "prop": "externallinks", "utf8": 1, "formatversion": "2"}
        # ---
        json1 = self.post_to_json(params)
        # ---
        # printe.output(json1)
        # ---
        links = json1.get('parse', {}).get('externallinks', [])
        # ---
        # remove duplicates
        liste1 = sorted(set(links))
        # ---
        # ---
        if 'nofilter' not in sys.argv:
            liste1 = filter_urls(liste1)
        # ---
        return liste1

    def make_new_text(self, tags):
        # ---
        for x in tags:
            if not x or not x.name:
                continue
            if x.name != 'ref':
                continue
            # ---
            name = x.attrs.get('name', '').replace('/', '').lower().strip()
            if name == '':
                continue
            # ---
            contents = x.contents
            # ---
            new_co = self.contents_all.get(name, '')
            # ---
            if contents == '' and new_co != '':
                self.section0 = self.section0.replace(str(x), new_co)
        # ---


# ---


class get_old:
    def __init__(self, title, lang="en"):
        # ---
        self.lang = lang
        self.title = title
        self.url = 'https://' + self.lang + '.wikipedia.org/w/api.php'
        self.oldtext = ''
        self.text = ''
        self.section0 = ''
        self.lead = {'extlinks': [], 'refsname': {}}
        self.extlinks = []
        self.refsname = {}
        self.contents_all = {}
        # ---
        self.session = requests.Session()
        # ---
        self.start()

    def start(self):
        self.get_oldtext()
        # ---
        parsed = wikitextparser.parse(self.oldtext)
        tags = parsed.get_tags()
        # ---
        self.refsname = self.get_ref_names(tags)
        # ---
        self.extlinks = self.get_extlinks_from_text(self.oldtext)
        # ---
        self.get_expended()
        # ---
        self.get_lead()

    def post_to_json(self, params):
        json1 = {}
        # ---
        unurl = f"{self.url}?{urlencode(params)}"
        # ---
        if "printurl" in sys.argv and "text" not in params:
            printe.output(f"get_old:\t\t{unurl}")
        # ---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        # ---
        return json1

    def expandtemplates(self, text):
        # ---
        params = {"action": "expandtemplates", "format": "json", "text": text, "prop": "wikitext", "formatversion": "2"}
        # ---
        data = self.post_to_json(params)
        # ---
        newtext = data.get("expandtemplates", {}).get("wikitext") or text
        # ---
        return newtext

    def get_expended(self):
        # ---
        text_pp = self.expandtemplates(self.oldtext)
        parsed = wikitextparser.parse(text_pp)
        tags = parsed.get_tags()
        # ---
        refsn = self.get_ref_names(tags)
        # ---
        refsn = {k: v for k, v in refsn.items() if k not in self.refsname}
        # ---
        if len(refsn) > 0:
            printe.output(f' new refsn: {len(refsn)}')
            printe.output(refsn)
            # ---
            self.refsname.update(refsn)

    def get_ref_names(self, tags):
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
            # ---
            if name == '':
                continue
            # ---
            contents = x.contents
            # ---
            if contents != '':
                self.contents_all[name] = str(x)
            # ---
            if re.sub(r'[:\d\s]+', '', name) == '':
                continue
            # ---
            if name not in _tags_:
                _tags_[name] = 0
            # ---
            _tags_[name] += 1
        # ---
        return _tags_

    def get_oldtext(self):
        params = {"action": "parse", "format": "json", "prop": "wikitext", "page": self.title, "utf8": 1}
        # ---
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": self.title,
            "formatversion": "2",
            "rvprop": "timestamp|content",
            "rvslots": "*",
            "rvlimit": "1",
            "redirects": 1,
            # "rvstart": "2020-05-31T22:00:00.000Z",
            "rvdir": "older",
        }
        # ---
        json1 = self.post_to_json(params)
        # ---
        revisions = json1.get('query', {}).get('pages', [{}])[0].get('revisions', [{}])[0]
        self.timestamp = revisions.get('timestamp', '')
        print(f'timestamp: {self.timestamp}')
        self.oldtext = revisions.get('slots', {}).get('main', {}).get('content', '')

    def get_lead(self):
        # ---
        parsed = wikitextparser.parse(self.oldtext)
        # ---
        section0 = parsed.get_sections(level=0)[0].contents
        self.section0 = section0
        # ---
        section0_pa = wikitextparser.parse(self.section0)
        # ---
        tags0 = section0_pa.get_tags()
        # ---
        self.make_new_text(tags0)
        # ---
        # printe.showDiff(section0, self.section0)
        # ---
        self.lead['refsname'] = self.get_ref_names(tags0)
        self.lead['extlinks'] = self.get_extlinks_from_text(self.section0)

    def get_extlinks_from_text(self, text):
        params = {"action": "parse", "format": "json", "title": self.title, "text": text, "prop": "externallinks", "utf8": 1, "formatversion": "2"}
        # ---
        json1 = self.post_to_json(params)
        # ---
        # printe.output(json1)
        # ---
        links = json1.get('parse', {}).get('externallinks', [])
        # ---
        # remove duplicates
        liste1 = sorted(set(links))
        # ---
        # ---
        if 'nofilter' not in sys.argv:
            liste1 = filter_urls(liste1)
        # ---
        return liste1

    def make_new_text(self, tags):
        # ---
        for x in tags:
            if not x or not x.name:
                continue
            if x.name != 'ref':
                continue
            # ---
            name = x.attrs.get('name', '').replace('/', '').lower().strip()
            if name == '':
                continue
            # ---
            contents = x.contents
            # ---
            new_co = self.contents_all.get(name, '')
            # ---
            if contents == '' and new_co != '':
                self.section0 = self.section0.replace(str(x), new_co)

        # ---


# ---
if __name__ == '__main__':
    # ---
    t = work_in_one_lang_link('he', 'עששת')
    sys.exit()
    # ---
    t = work_in_one_lang_link('en', 'Deep_vein_thrombosis')
    old = get_old('Deep_vein_thrombosis')
    # print
    orex = t.extlinks
    oldex = old.extlinks
    print(f'orex: {len(orex)}')
    print(f'oldex: {len(oldex)}')
    printe.showDiff("\n".join(orex), "\n".join(oldex))
    # ---
    print('=============')
    # ---
    refsname = t.refsname
    oldrefsname = old.refsname
    print(f'refsname: {len(refsname)}')
    print(f'oldrefsname: {len(oldrefsname)}')
    printe.showDiff("\n".join(refsname), "\n".join(oldrefsname))
    # ---
    print('=============')
    # ---
    lead = t.lead
    oldlead = old.lead
    for x in ['extlinks', 'refsname']:
        print('=============')
        # ---
        print(f'{x}: {len(lead[x])}')
        print(f'old{x}: {len(oldlead[x])}')
        printe.showDiff("\n".join(lead[x]), "\n".join(oldlead[x]))
    # ---
