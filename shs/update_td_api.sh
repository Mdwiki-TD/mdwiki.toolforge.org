#!/bin/bash

echo "Cd to home directory..."
cd "$HOME" || { echo "Failed to change directory to home directory"; exit 1; }

echo "Removing old TD_API directory if exists..."
rm -rf TD_API

BRANCH="${1:-main}"
echo ">>> clone --branch ${BRANCH} ."

echo "Cloning repository from GitHub..."
git clone --branch "$BRANCH" https://github.com/Mdwiki-TD/TD_API.git TD_API || { echo "Failed to clone repository"; exit 1; }

rm -rf TD_API/.git

cp -rf -v TD_API/* public_html/api/

echo "Removing TD_API directory..."
rm -rf TD_API

echo "Script execution completed successfully."

