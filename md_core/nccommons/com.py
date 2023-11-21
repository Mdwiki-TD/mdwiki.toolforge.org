#!/usr/bin/python3
"""

create pages in nccommons

python3 nccommons/com.py -limitall:50000 -files:200 ask

"""
#
# (C) Ibrahem Qasim, 2023
#
# ---
from nccommons import api
import re
import sys
import json
import os
import codecs

# ---
project = "/data/project/mdwiki/"
# ---
if not os.path.isdir(project):
    project = "I:/mdwiki/md_core/nccommons"
# ---
# newpages = api.Get_All_pages(start="", namespace="0", limit="max", apfilterredir="", limit_all="")
# new = api.create_Page(text=, title)
# ---
files_len = 0
# ---
limitall = 0
limit_0 = 0
# ---
for arg in sys.argv:
    arg, sep, value = arg.partition(":")
    # ---
    if arg == "-limit0":
        limit_0 = int(value)
    if arg == "-limitall":
        limitall = int(value)
    if arg == "-files":
        files_len = int(value)
    # ---
# ---
file_dir = __file__.replace("com.py", "")
# ---
print(f"file_dir : {file_dir}")
# ---
if 'usefiles' in sys.argv:
    ns_0_pages = codecs.open(file_dir + "ns_0_pages.json", "r", "utf-8").read()
    all_files = codecs.open(file_dir + "all_files.json", "r", "utf-8").read()
else:
    ns_0_pages = api.Get_All_pages("", limit="max", namespace="0", limit_all=limit_0)
    all_files = api.Get_All_pages("", limit="max", namespace="6", limit_all=limitall)
    # ---
    codecs.open(file_dir + "ns_0_pages.json", "w", "utf-8").write(json.dumps(ns_0_pages, indent=4, ensure_ascii=False))
    codecs.open(file_dir + "all_files.json", "w", "utf-8").write(json.dumps(all_files, indent=4, ensure_ascii=False))
# ---
if 'onlyread' in sys.argv:
    sys.exit(0)
# ---
all_reg = {}
# all_reg['Abdominal_aortic_aneurysm_(Radiopaedia_10122-10660_Axial_C+_portal_venous_phase)'] = []


def make_page(x, tab):
    # ---
    lines = ""
    # ---
    gt = [(numb, hy) for numb, hy in tab.items()]
    gt.sort(reverse=False)
    # ---
    for _, title in gt:
        # ---
        lines += f"|File:{title}|\n"
    # ---
    x2 = x.split("(")[0].split("-")[0].strip()
    # ---
    if x2.strip() == "":
        x2 = x
    # ---
    text = "{{" + f"Imagestack\n|width=850\n|title={x2}\n|align=centre\n|loop=no\n{lines}"
    # ---
    text += "\n}}\n[[Category:Image set]]"
    # ---
    api.create_Page(text, x)


def work():
    # ---
    nomatch = 0
    # ---
    for title in all_files:
        # Abdominal_aortic_aneurysm_(Radiopaedia_10122-10660_Axial_C+_portal_venous_phase_30).jpg
        ra = r"^File\:(.*?\(.*?)[\s\-\w](\d+)\)\.(?:jpg|JPG|png|PNG|gif|GIF|svg|SVG)$"
        mate = re.match(ra, title)
        # ---
        title2 = title.replace("File:", "")
        # ---
        if mate:
            number = int(mate.group(2))
            page = mate.group(1) + ")"
            # ---
            if page in all_reg:
                all_reg[page][number] = title2
            else:
                all_reg[page] = {number: title2}
            # ---
        else:
            nomatch += 1
            print(f"title:{nomatch}/\t{title}.")
    # ---
    da = [(len(y), x) for x, y in all_reg.items() if len(y) > 1]
    da.sort(reverse=False)
    # ---
    for le, x in da:
        # ---
        if le >= files_len:
            print(f"x:{x}, len: {le}")
            tab = all_reg[x]
            # ---
            if x not in ns_0_pages:
                # ---
                make_page(x, tab)
            else:
                print(f"page:{x} already in ns_0_pages.")


# ---
# python3 core8/pwb.py mdwiki/mdpy/com test
# ---
if __name__ == "__main__":
    work()
# ---
