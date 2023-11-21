'''

python3 core8/pwb.py priorviews/bots/count_words

'''
import sys
import re
from urllib.parse import urlencode
import requests
import wikitextparser
from mdpy import printe

# ---
'''
# ---
from priorviews.bots import count_words
tt = count_words.get_words(title, lang)
# ---
'''
# ---


class InOldText:
    def __init__(self, title, lang="en"):
        # ---
        self.lang = lang
        self.title = title
        self.url = 'https://' + self.lang + '.wikipedia.org/w/api.php'
        self.oldtext = ''
        self.newtext = ''
        self.words = 0
        # ---
        self.session = requests.Session()
        # ---
        self.start()

    def start(self):
        self.get_oldtext()
        self.count(self.oldtext)
        # ---
        if self.words < 50:
            printe.output(f"\twords: {self.words} < 50 ")
            words = self.words
            self.get_newtext()
            self.count(self.newtext)
            # ---
            if words > self.words:
                self.words = words
            # ---
        # ---
        text = self.oldtext

    def count(self, text):
        text = text.replace("'''", "").replace("''", "")
        # ---
        tem_text = text
        # ---
        parsed = wikitextparser.parse(tem_text)
        # ---
        # remove cat links
        # for link in parsed.wikilinks:   if ":" in link.title:   tem_text = tem_text.replace(str(link), "")
        # parsed = wtp.parse(tem_text)
        # ---
        # remove tables
        # remove template
        # remove html tag include ref tags
        # remove all comments
        # remove all external links
        tem_text = parsed.plain_text()
        parsed = wikitextparser.parse(tem_text)
        # replace all wikilinks to be like  [from|some text ] to from
        # for wikilink in parsed.wikilinks:   tem_text = tem_text.replace(str(wikilink), str(wikilink.title))

        # remove tables like this "{| |}"
        tem_text = re.sub(r"{|\|[.|\w|\W]*?\|}", "", tem_text)

        # remove numbers in string"
        tem_text = re.sub(r"\d+", "", tem_text)

        # get counts of words
        lenth = len(re.findall(r'\w+', tem_text))
        # ---
        # print(f'count_text: {lenth}')
        self.words = lenth

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

    def get_oldtext(self):
        params = {"action": "parse", "format": "json", "prop": "wikitext", "page": self.title, "utf8": 1}
        # ---
        params = {"action": "query", "format": "json", "prop": "revisions", "titles": self.title, "redirects": 1, "formatversion": "2", "rvprop": "timestamp|content", "rvslots": "*", "rvlimit": "1", "rvstart": "2020-05-31T22:00:00.000Z", "rvdir": "older"}
        # ---
        json1 = self.post_to_json(params)
        # ---
        revisions = json1.get('query', {}).get('pages', [{}])[0].get('revisions', [{}])[0]
        self.timestamp = revisions.get('timestamp', '')
        # print(f'timestamp: {self.timestamp}')
        self.oldtext = revisions.get('slots', {}).get('main', {}).get('content', '')

    def get_newtext(self):
        params = {"action": "parse", "format": "json", "prop": "wikitext", "page": self.title, "redirects": 1, "utf8": 1, "formatversion": "2"}
        # ---
        json1 = self.post_to_json(params)
        # ---
        self.newtext = json1.get('parse', {}).get('wikitext', '')

    def Words(self):
        printe.output(f'\t\twords: {self.words}')
        return self.words


def get_words(title, lang):
    # ---
    bot = InOldText(title, lang=lang)
    # ---
    words = bot.Words()
    # ---
    return words


# ---
if __name__ == '__main__':
    # ---
    t = get_words('التهاب الفقار القسطي', "ar")
    print(f'words: {t}')
    sys.exit()
    # ---
