#!/bin/bash

echo "Cd to home directory..."
cd "$HOME" || { echo "Failed to change directory to home directory"; exit 1; }

echo "Removing old mdall directory if exists..."
rm -rf mdall

BRANCH="${1:-main}"
echo ">>> clone --branch ${BRANCH} ."

echo "Cloning repository from GitHub..."
git clone --branch "$BRANCH" https://github.com/Mdwiki-TD/mdwiki.toolforge.org.git mdall || { echo "Failed to clone repository"; exit 1; }

rm -rf mdall/.git

echo "Deleting all JSON files..."
find mdall/public_html -name "*.json" -delete && echo "JSON files deleted successfully" || echo "Failed to delete JSON files"

echo "Copying files to public_html..."
cp -rf -v mdall/public_html/* public_html/ || { echo "Failed to copy files to public_html directory"; exit 1; }

echo "Removing mdall directory..."
rm -rf mdall

echo "Script execution completed successfully."

