#!/bin/bash
cd $HOME
# cd /data/project/mdwiki/

rm -rf newapi_x

# Download the wd-core repository from GitHub.
git clone https://github.com/MrIbrahem/newapi.git newapi_x

cp -rf newapi_x/* pybot/md_core/newapi -v

find pybot/md_core/newapi -name "*.pyc" -exec rm -f {} +

chmod -R 6770 pybot/md_core/newapi

rm -rf newapi_x
