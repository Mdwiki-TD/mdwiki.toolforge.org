#!/bin/bash

echo "Cd to home directory..."
cd "$HOME" || { echo "Failed to change directory to home directory"; exit 1; }

echo "Removing old mdall directory if exists..."
rm -rf mdall

echo "Cloning repository from GitHub..."
git clone https://github.com/Mdwiki-TD/mdwiki.toolforge.org.git mdall || { echo "Failed to clone repository"; exit 1; }

echo "Moving files to htmlx directory..."
mv mdall/public_html htmlx || { echo "Failed to move files to htmlx directory"; exit 1; }

echo "Removing mdall directory..."
rm -rf mdall

echo "Removing Translation_Dashboard directory..."
rm -rf htmlx/Translation_Dashboard
rm -rf htmlx/publish

cp -rf -v htmlx/api/* public_html/api/

echo "Deleting all JSON files..."
find htmlx -name "*.json" -delete && echo "JSON files deleted successfully" || echo "Failed to delete JSON files"

echo "Copying files to public_html..."
cp -rf -v htmlx/* public_html/ || { echo "Failed to copy files to public_html directory"; exit 1; }

echo "Removing htmlx directory..."
rm -rf htmlx

echo "Script execution completed successfully."

