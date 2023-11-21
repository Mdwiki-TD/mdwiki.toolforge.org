'''

python3 core8/pwb.py priorviews/bots/get_translator

'''
from priorviews.bots import helps
import sys
from urllib.parse import urlencode
import requests
from mdpy import printe

# ---
'''
# ---
from priorviews.bots import get_translator
# tt = get_translator.get_au(title, lang)
# ---
'''
# ---
# v_comm = helps.isv(comment)
# _views = helps.views_url(title, lang, view)
# helps.is_ip(user)
# ---


class FindTranslator:
    def __init__(self, title, lang="en"):
        # ---
        self.lang = lang
        self.title = title
        self.url = 'https://' + self.lang + '.wikipedia.org/w/api.php'
        self.translator = ''
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
            printe.output(f"get_old:\t\t{unurl}")
        # ---
        try:
            req = self.session.post(self.url, data=params)
            json1 = req.json()
        except Exception as e:
            printe.output(f'except: lang:{self.lang} {e}')
        # ---
        return json1

    def start(self):
        params = {"action": "query", "format": "json", "prop": "revisions", "titles": self.title, "formatversion": "2", "rvprop": "comment|user", "rvdir": "newer", "rvlimit": "max"}
        # ---
        rvcontinue = 'x'
        # ---
        while rvcontinue != '':
            # ---
            if rvcontinue != 'x':
                params['rvcontinue'] = rvcontinue
            # ---
            json1 = self.post_to_json(params)
            # ---
            rvcontinue = json1.get("continue", {}).get("rvcontinue", '')
            # ---
            pages = json1.get('query', {}).get('pages', [{}])
            # ---
            for p in pages:
                revisions = p.get("revisions", [])
                for r in revisions:
                    # print(r)
                    user = r.get('user', '')
                    if user == '' or helps.is_ip(user):
                        continue
                    # ---
                    comment = r.get('comment', '').lower()
                    if helps.isv(comment):
                        # print(r)
                        self.translator = user
                        return

    def Translator(self):
        printe.output(f'\t\t Translator: {self.translator}')
        return self.translator


def get_au(title, lang):
    # ---
    bot = FindTranslator(title, lang=lang)
    # ---
    auu = bot.Translator()
    # ---
    return auu


# ---
if __name__ == '__main__':
    # ---
    t = get_au('نكاف', "ar")
    print(f'au: {t}')
    sys.exit()
    # ---
