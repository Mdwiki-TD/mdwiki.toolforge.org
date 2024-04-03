#!/bin/bash

cd /data/project/mdwiki

rm -rf mdwikix

# Download the md-core repository from GitHub.
git clone https://github.com/MrIbrahem/mdwiki-python-files.git mdwikix

# Into a new directory called 'md_core/' in the current working directory
# cp -rf -v mdwikix/pybot/md_core/* md_core/
# cp -rf -v mdwikix/pybot/TDpynew/* TDpynew/
# cp -rf -v mdwikix/pybot/newupdater/* newupdater/

# sh shs/update_api.sh
rm -rf mdwikix/md_core/newapi

cp -rf -v mdwikix/* pybot/

find pybot -name "*.pyc" -exec rm -f {} +

chmod -R 6770 pybot

# Remove the `mdwikix` directory.
rm -rf mdwikix

$HOME/local/bin/python3 -m pip install -r pybot/requirements.in