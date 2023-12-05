"""
A few small changes when we are greeting the starting text at User:Mr.
Ibrahem/Article name

1) Can we leave out the "{{short description|text here}}

2) Can we also leave out "{{TOC limit}}"

James
"""
import wikitextparser as wtp

# ---
temps_to_delete = ["short description", "toc limit", 'use american english', 'use dmy dates', 'about', 'redirect']


def work(text):
    # ---
    parsed = wtp.parse(text)
    for temp in parsed.templates:
        # ---
        name = str(temp.normal_name()).strip()
        if name.lower() in temps_to_delete:
            text = text.replace(temp.string.strip(), '')
    # ---
    return text.strip()


# ---
