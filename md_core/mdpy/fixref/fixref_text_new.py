
import re

import wikitextparser as wtp
from mdpy.bots import make_title_bot
# _title1_ = make_title_bot.make_title(url)


def change_lay_source(temp):
    # ---
    temp_name = "cite press release"
    # ---
    temp_name = str(temp.normal_name()).strip()
    # ---
    tab = {
        "url": ['layurl', 'lay-url'],
        "title": ['laytitle', 'lay-title'],
        "date": ['laydate', 'lay-date'],
        "source": ['laysource', 'lay-source']
    }
    # ---
    new_tab = {"url", "title", "date", "source"}
    # ---
    for x, ys in tab.items():
        for param in ys:
            if temp.has_arg(param):
                val = temp.get_arg(param).value
                if val.strip() != '':
                    new_tab[x] = val.strip()
                temp.del_arg(param)
    # ---
    title = new_tab["title"]
    url = new_tab["url"]
    Date = new_tab["date"]
    source = new_tab["source"]
    # ---
    if title == '' and url != '':
        title = make_title_bot.make_title(url)
    # ---
    lay_temp = ''
    # ---
    if url != '' or source != '':
        lay_temp = f'''|template = {temp_name}|url = {url}|title = {title}|date = {Date}|website = {source}'''
        lay_temp = "* {{lay source" + lay_temp + "}}"
    # ---
    return lay_temp, temp


def fix_ref_template(text, returnsummary=False):
    # ---
    summary = 'Normalize references'
    # ---
    newtext = text
    # ---
    parsed = wtp.parse(text)
    # ---
    for tag in parsed.tags("ref"):
        # ---
        content = tag.contents
        # ---
        if not content.strip():
            continue
        # ---
        templates = tag.templates
        # ---
        for temp in templates:
            # ---
            name = str(temp.normal_name()).strip()
            # ---
            temp_str = temp.string
            # ---
            laysource, temp = change_lay_source(temp)
            # ---
            temp_new = temp.string
            # ---
            temp_new = re.sub(r'\n', '', temp_new, flags=re.DOTALL)
            # ---
            if laysource != '':
                temp_new = temp_new + "\n" + laysource
                summary = 'Normalize references, move lay source params'
            # ---
            newtext = newtext.replace(temp_str, temp_new)
    # ---
    if returnsummary:
        return newtext, summary
    # ---
    return newtext
