#!/bin/bash

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."

cd "$HOME" || exit 1
# cd /data/project/mdwiki/

rm -rf authx

# Download the wd-core repository from GitHub.
git clone --branch "$BRANCH" https://github.com/Mdwiki-TD/auth-repo.git authx

# delete composer.json and composer.lock
rm -rf authx/composer.json authx/composer.lock

# delete all json files in all subdirectories
find authx -name *.json -delete

# delete vendor
rm -rf authx/vendor

# copy all files to public_html
cp -rf -v authx/* public_html/auth

# Remove the `authx` directory.
rm -rf authx
