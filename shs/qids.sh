#!/bin/bash
# Find the Wikidata qid for items without qid from English
$HOME/local/bin/python3 c8/pwb.py mdpages/find_qids redirects addthem

# Fix Wikidata item conversions and add articles to qids spreadsheet
$HOME/local/bin/python3 c8/pwb.py mdpages/fixqids fix
$HOME/local/bin/python3 c8/pwb.py mdpages/get_red
