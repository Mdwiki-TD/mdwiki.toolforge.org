#!/bin/bash

# Create temporary files with lists of existing articles for all languages
$HOME/local/bin/python3 core8/pwb.py mdpages/cashwd

# apis/cat_cach
$HOME/local/bin/python3 core8/pwb.py apis/cat_cach

$HOME/local/bin/python3 core8/pwb.py copy_data/all_articles

$HOME/local/bin/python3 core8/pwb.py copy_data/exists_db

#
$HOME/local/bin/python3 core8/pwb.py wd_works/recheck

#
$HOME/local/bin/python3 core8/pwb.py db_work/check_titles
