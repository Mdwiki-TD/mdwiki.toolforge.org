# ---
import re
import pywikibot
import wikitextparser as wtp

# ---
from mdpy.bots import mdwiki_api


def count_text(text):
    # ---
    text = text.replace("'''", "").replace("''", "")
    # ---
    tem_text = text
    # ---
    parsed = wtp.parse(tem_text)
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
    parsed = wtp.parse(tem_text)
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
    return tem_text, lenth


def count_lead(x):
    # ---
    page_text = mdwiki_api.GetPageText(x)
    # ---
    parsed = wtp.parse(page_text)
    section = parsed.get_sections(level=0)[0].contents
    # ---
    te_1, lenth1 = get_lead_text(page_text)
    te_2, lenth2 = count_text(page_text)
    # ---
    pywikibot.showDiff(te_1, f'count_text:\n{te_2}')
    # ---
    return lenth1


def count_all(title='', text=''):
    # ---
    if text == '' and title != '':
        text = mdwiki_api.GetPageText(title)
    # ---
    parsed = wtp.parse(text)
    # ---
    _te_, pageword = count_text(text)
    # ---
    section = parsed.get_sections(level=0)[0].contents
    # ---
    _te_, leadword = count_text(section)
    # ---
    return leadword, pageword


# ---
if __name__ == '__main__':
    # ---
    x = 'Spondyloperipheral dysplasia'
    # ---
    leadword, pageword = count_all(title=x)
    print(f'leadword: {leadword}, pageword: {pageword}')
    # ---
    pageword2 = mdwiki_api.wordcount(x)
    print(f'pageword2: {pageword2}')
