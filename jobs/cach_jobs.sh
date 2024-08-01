#!/bin/bash

# Create temporary files with lists of existing articles for all languages
$HOME/local/bin/python3 core8/pwb.py mdpages/cashwd

# apis/cat_cach newlist
$HOME/local/bin/python3 core8/pwb.py apis/cat_cach newlist

#
$HOME/local/bin/python3 core8/pwb.py wd_works/recheck

#
$HOME/local/bin/python3 core8/pwb.py db_work/check_titles
