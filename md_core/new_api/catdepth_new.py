# ---
# ---
def login_def(lang, family):
    return {}


# ---


class CategoryDepth:

    def __init__(self, title, sitecode, depth=0, family="wikipedia", ns="all", nslist=[], without_lang="", with_lang="", tempyes=[], no_gcmsort=False, **kwargs):
        # ---
        self.title = title
        self.no_gcmsort = no_gcmsort
        # ---
        self.log = login_def(sitecode, family=family)
        # ---
        self.tempyes = tempyes

        self.without_lang = without_lang
        self.with_lang = with_lang

        self.depth = depth
        self.ns = str(ns)
        self.nslist = nslist
        if not isinstance(self.depth, int):
            try:
                self.depth = int(self.depth)
            except ValueError:
                print(f'self.depth != int: {self.depth}')
                self.depth = 0
        # ---
        self.result_table = {}
        self.params = {}
        self.make_params()

        # return self._subcatquery_(title)

    def Login_to_wiki(self):
        self.log.Log_to_wiki()

    def post_params(self, params):
        return self.log.post(params, addtoken=True)

    def make_params(self):
        params = {
            "action": "query",
            "format": "json",
            "utf8": 1,
            "generator": "categorymembers",
            "gcmprop": "title",
            "prop": [],
            "gcmtype": "page|subcat",
            "gcmlimit": "max",
            "formatversion": "1",
            "gcmsort": "timestamp",
            "gcmdir": "newer"
        }
        if self.no_gcmsort:
            del params["gcmsort"]
            del params["gcmdir"]

        if self.tempyes != []:
            params["prop"].append("templates")
            params["tllimit"] = "max"
            params["tltemplates"] = "|".join(self.tempyes)
        if self.with_lang != "" or self.without_lang != '':  # مع وصلة لغة معينة
            params["prop"].append("langlinks")
            params["lllimit"] = "max"
        # ---
        if self.ns in ["0", "10", 0, 10]:
            params["gcmtype"] = "page"
        elif self.ns in [14, "14"]:
            params["gcmtype"] = "subcat"
        # ---
        print('gcmtype::', params["gcmtype"])
        # ---
        if len(self.nslist) > 0:
            if self.nslist == [14]:
                params["gcmtype"] = "subcat"
            elif 14 not in self.nslist and self.depth == 0:
                params["gcmtype"] = "page"
        # ---
        print('gcmtype::', params["gcmtype"])
        # ---
        if len(params['prop']) == 0:
            del params['prop']
        # ---
        self.params = params

    def get_cat(self, cac):
        # ---
        params = self.params
        params["gcmtitle"] = cac
        # ---
        continue_v = 'x'
        continue_p = ''
        # ---
        table = {}
        # ---
        while continue_v != '':
            if continue_v != 'x':
                params[continue_p] = continue_v
            # ---
            continue_v = ''
            # ---
            api = self.post_params(params)
            # ---
            if not api:
                print(f'api == false for {cac}')
                break
            # ---
            continue_d = api.get("continue", {})
            for p, v in continue_d.items():
                if p == 'continue':
                    continue
                continue_v = v
                continue_p = p
            # ---
            pages = api.get("query", {}).get("pages", {})
            # ---
            for category in pages:
                caca = pages[category] if isinstance(pages, dict) else category
                cate_title = caca["title"]
                # ---
                tablese = {}
                # ---
                if "ns" in caca:
                    tablese['ns'] = caca['ns']
                    if self.ns == "14" or self.nslist == [14]:
                        if str(caca['ns']) != "14":
                            continue
                # ---
                tablese['templates'] = [x['title'] for x in caca.get('templates', {})]
                tablese['langlinks'] = {
                    fo['lang']: fo.get('title') or fo.get('*') or ''
                    for fo in caca.get('langlinks', [])
                }
                # ---
                table[cate_title] = tablese
            # ---
        return table

    def add_to_result_table(self, x, tab):
        if x in self.result_table:
            return

        if self.without_lang != "":
            no_langs = tab.get('langlinks', {}).get(self.without_lang, '')
            if no_langs != "":
                return

        if self.with_lang != "":
            langs = tab.get('langlinks', {}).get(self.with_lang, '')
            if langs == "":
                return

        self.result_table[x] = tab

    def _subcatquery_(self):
        # ---
        print(f'catdepyh_new.py cat:{self.title}, ns:{self.ns}')
        # ---
        tablemember = self.get_cat(self.title)
        # ---
        for x in tablemember:
            self.add_to_result_table(x, tablemember[x])
        # ---
        new_list = [x for x in tablemember if int(tablemember[x]["ns"]) == 14]
        # ---
        depth_done = 0
        # ---
        while self.depth > depth_done:
            new_tab2 = []
            # ---
            depth_done += 1
            # ---
            for cat in new_list:
                # ---
                table2 = self.get_cat(cat)
                # ---
                for x in table2:
                    # ---
                    if int(table2[x]["ns"]) == 14:
                        new_tab2.append(x)
                    # ---
                    self.add_to_result_table(x, table2[x])
            # ---
            new_list = new_tab2
        # ---
        return self.result_table


# ---
