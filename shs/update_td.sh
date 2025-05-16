#!/bin/bash

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."

cd "$HOME" || exit 1
# cd /data/project/mdwiki/

rm -rf tdx

# Download the wd-core repository from GitHub.
git clone --branch "$BRANCH" --recurse-submodules https://github.com/Mdwiki-TD/Translation-Dashboard.git tdx

rm -rf tdx/.git

# delete composer.json and composer.lock
rm -rf tdx/composer.json tdx/composer.lock

# delete all json files in all subdirectories
find tdx -name *.json -delete

# delete vendor
rm -rf tdx/vendor

# copy all files to public_html
cp -rf -v tdx/* public_html/Translation_Dashboard

# Remove the `tdx` directory.
rm -rf tdx

echo "Repository cloned and cleaned successfully."
