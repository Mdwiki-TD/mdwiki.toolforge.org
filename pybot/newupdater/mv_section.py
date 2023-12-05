import re
import sys

from pathlib import Path
import codecs
import wikitextparser


def printn(s):
    return


# ---


class move_External_links_section:
    def __init__(self, text):
        self.text = text
        # ---
        self.new_text = self.text
        self.text_to_work = self.text
        # ---
        self.parser = wikitextparser.parse(self.text)
        # ---
        self.sections = self.parser.get_sections(include_subsections=True)
        # ---
        self.ext_sec = ''
        self.new_ext_sec = ''
        self.last_sec = ''
        # ---
        self.run()

    def run(self):
        # ---
        self.get_sects()
        # ---
        if self.ext_sec == '':
            return
        # ---
        if str(self.ext_sec) == str(self.last_sec):
            return
        # ---
        self.add_ext_section()

    def add_ext_section(self):
        # ---
        categoryPattern = r'\[\[\s*(Category)\s*:[^\n]*\]\]\s*'
        interwikiPattern = r'\[\[([a-zA-Z\-]+)\s?:([^\[\]\n]*)\]\]\s*'
        templatePattern = r'\r?\n{{((?!}}).)+?}}\s*'
        commentPattern = r'<!--((?!-->).)*?-->\s*'
        # ---
        # metadataR = re.compile(fr'(\r?\n)?({categoryPattern}|{interwikiPattern}|{commentPattern})$', re.DOTALL)
        metadataR = re.compile(fr'(\r?\n)?({categoryPattern}|{interwikiPattern}|{templatePattern}|{commentPattern})$', re.DOTALL)
        # ---
        tmpText = self.text_to_work
        # ---
        while True:
            match = metadataR.search(tmpText)
            if match:
                tmpText = tmpText[: match.start()]
            else:
                break
        # ---
        index = len(tmpText)
        # ---
        newtext = self.text_to_work[:index].rstrip() + f'\n\n{self.new_ext_sec.strip()}\n\n' + self.text_to_work[index:].strip()
        # ---
        self.new_text = newtext

    def get_sects(self):
        # ---
        n = -1
        # ---
        last = ''
        # ---
        for s in self.sections:
            # ---
            n += 1
            # ---
            t = s.title
            c = s.contents
            # ---
            if t and t.strip().lower() == 'external links':
                self.ext_sec = str(s)
                self.new_ext_sec = str(s)
                # ---
            # ---
            last = s
            # ---
        # ---
        if self.ext_sec == '':
            return
        # ---
        self.text_to_work = self.text_to_work.replace(str(self.ext_sec), '')
        # ---
        self.last_sec = last
        # ---
        if self.last_sec.title.lower().strip() == 'references':
            l_c = self.last_sec.contents
            # ---
            printn(f'title: {self.last_sec.title}')
            printn(f'contents: {l_c}')
            # ---
            mata = re.search(r'^{{reflist(?:[^{]|{[^{]|{{[^{}]+}}|)+}}', l_c, flags=re.IGNORECASE)
            # ---
            if mata:
                # ---
                # ---
                index = len(l_c[: mata.end()])
                # ---
                l_c2 = l_c[index:]
                # ---
                # printn(f'index : {index}')
                # printn(f'l_c2 : {l_c2}')
                # ---
                g = mata.group()
                g_to = f'== {self.last_sec.title.strip()} ==\n{g}\n'
                # ---
                printn(f'g_to: {g_to}')
                # ---
                self.ext_sec = f'{g_to}\n{self.ext_sec}'
                self.new_ext_sec = self.ext_sec
                # ---
                self.text_to_work = self.text_to_work.replace(str(self.last_sec).strip(), l_c2.strip())

    def make_new_txt(self):
        # ---
        self.new_text = re.sub(r'\n\s*\[\[Category', '\n[[Category', self.new_text, flags=re.DOTALL | re.MULTILINE)
        # ---
        return self.new_text


# ---
if __name__ == "__main__":
    # python3 pwb.py newupdater/mv_section Alcohol_septal_ablation
    import pywikibot

    # ---
    printn = print
    # ---
    Dir = Path(__file__).parent
    from newupdater.med import GetPageText

    # ---
    text = GetPageText(sys.argv[1])
    # ---
    # text = codecs.open(Dir+ "/texts/section.txt", "r", "utf-8").read()
    # ---
    codecs.open(Dir + "/texts/section.txt", "w", "utf-8").write(text)
    # ---
    bot = move_External_links_section(str(text))
    # ---
    new_text = bot.make_new_txt()
    # ---
    pywikibot.showDiff(text, new_text)
    codecs.open(Dir + "/texts/secnew.txt", "w", "utf-8").write(new_text)
