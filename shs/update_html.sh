#!/bin/bash
cd $HOME
# cd /data/project/mdwiki/

rm -rf mdall

# Download the repository from GitHub.
git clone https://github.com/MrIbrahem/mdwiki.toolforge.org.git mdall

mv mdall/public_html htmlx

rm -rf mdall

rm -rf htmlx/Translation_Dashboard

# delete all json files in all subdirectories
find htmlx -name *.json -delete

# copy all files to public_html
cp -rf -v htmlx/* public_html/

# Remove the `htmlx` directory.
rm -rf htmlx
