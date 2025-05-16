#!/bin/bash
cd "$HOME" || exit 1
# cd /data/project/mdwiki/

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."


rm -rf newapi_x

mkdir  pybot/new
mkdir  pybot/new/newapi

# Download the wd-core repository from GitHub.
git clone --branch "$BRANCH" https://github.com/MrIbrahem/newapi.git newapi_x

rm -rf newapi_x/.git

cp -rf newapi_x/* pybot/new/newapi -v

find pybot/new/newapi -name "*.pyc" -exec rm -f {} +

#chmod -R 6770 pybot/new/newapi
find pybot/new/newapi -type f ! -name "*.pyc" -exec chmod 6770 {} \;

rm -rf newapi_x

$HOME/local/bin/python3 -m pip install -r pybot/new/newapi/requirements.in -U
