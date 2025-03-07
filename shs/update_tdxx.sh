#!/bin/bash
cd "$HOME" || exit 1
# cd /data/project/mdwiki/

rm -rf tdx

# Download the wd-core repository from GitHub.
git clone --recurse-submodules https://github.com/MrIbrahem/Translation-Dashboard.git tdx

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
