#!/bin/bash

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."

cd "$HOME" || exit 1

rm -rf mdwikix

git clone --branch "$BRANCH" https://github.com/MrIbrahem/mdwiki-python-files.git mdwikix || { echo ">>> Failed to clone repository"; exit 1; }

rm -rf mdwikix/.git

rm -rf mdwikix/md_core/newapi

cp -rf -v mdwikix/* pybot/

rm -rf mdwikix

#$HOME/local/bin/python3 -m pip install -r pybot/requirements.in
#pip install --upgrade pip

#find pybot -type f ! -name "*.pyc" -exec chmod 6770 {} \;

echo ">>> Script execution completed successfully."
