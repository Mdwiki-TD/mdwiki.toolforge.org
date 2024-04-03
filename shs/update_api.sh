#!/bin/bash
cd $HOME
# cd /data/project/mdwiki/

rm -rf newapi_x

# Download the wd-core repository from GitHub.
git clone https://github.com/MrIbrahem/newapi.git newapi_x

cp -rf newapi_x/* pybot/md_core/newapi -v

find pybot/md_core/newapi -type f ! -name "*.pyc" -exec chmod 6770 {} \;

rm -rf newapi_x

$HOME/local/bin/python3 -m pip install -r pybot/md_core/newapi/requirements.in
