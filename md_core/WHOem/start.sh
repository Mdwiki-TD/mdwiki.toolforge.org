#!/bin/bash

# find all links
python3 core8/pwb.py WHOem/lists/md_links

# get all langlinks
python3 core8/pwb.py WHOem/lists/lang_links new

# get all langlinks_mdtitles
python3 core8/pwb.py WHOem/lists/lang_links_mdtitles

# find_views
# python3 core8/pwb.py WHOem/lists/find_views_by_lang lang:en

python3 core8/pwb.py WHOem/lists/find_views_by_lang new

python3 core8/pwb.py WHOem/make_text ask

cp md_core/WHOem/lists/views.json public_html/WHO/Tables/views.json