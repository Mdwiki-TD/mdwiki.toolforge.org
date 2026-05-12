#!/bin/bash

# Create temporary files with lists of existing articles for all languages
$HOME/local/bin/python3 c9/pwb.py td_core/mdpages/cashwd

$HOME/local/bin/python3 c9/pwb.py td_core/copy_data/by_qid/sitelinks

# apis/cat_cach
$HOME/local/bin/python3 c9/pwb.py md_core_helps/apis/cat_cach

$HOME/local/bin/python3 c9/pwb.py td_core/copy_data/by_title/all_articles
$HOME/local/bin/python3 c9/pwb.py td_core/copy_data/by_title/exists_db

#
$HOME/local/bin/python3 c9/pwb.py td_core/wd_works/recheck

#
$HOME/local/bin/python3 c9/pwb.py td_core/db_work/check_titles
