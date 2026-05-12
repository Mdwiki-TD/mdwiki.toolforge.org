#!/bin/bash
$HOME/local/bin/python3 core8/pwb.py td_core/mdcount/countref newpages
$HOME/local/bin/python3 core8/pwb.py td_core/mdcount/countref sql
$HOME/local/bin/python3 core8/pwb.py td_core/mdcount/words newpages

