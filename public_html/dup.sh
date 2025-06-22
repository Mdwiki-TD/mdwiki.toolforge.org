#!/bin/bash
export PATH=/data/project/mdwiki/local/bin:/usr/local/bin:/usr/bin:/bin

toolforge jobs run fixduplict --image python3.9 --command "/data/project/mdwiki/local/bin/python3 core8/pwb.py mdpy/fix_duplicate save"

