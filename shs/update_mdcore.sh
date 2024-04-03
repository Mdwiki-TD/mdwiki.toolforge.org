#!/bin/bash

echo ">>> Cd to home directory..."
cd "$HOME" || { echo ">>> Failed to change directory to home directory"; exit 1; }


if [ -d "mdwikix" ]; then
	echo ">>> Removing old mdwikix directory:"
    rm -rf mdwikix || { echo "Failed to remove mdwikix directory"; exit 1; }
fi

echo ">>> Cloning repository from GitHub..."
git clone https://github.com/MrIbrahem/mdwiki-python-files.git mdwikix || { echo ">>> Failed to clone repository"; exit 1; }


if [ -d "mdwikix/md_core/newapi" ]; then
	echo ">>> Removing mdwikix/md_core/newapi directory..."
    rm -rf mdwikix/md_core/newapi || { echo "Failed to remove mdwikix/md_core/newapi directory";}
fi

echo ">>> Copying files to pybot..."

cp -rf -v mdwikix/* pybot/ || { echo ">>> Failed to copy files to pybot directory"; exit 1; }


if [ -d "mdwikix" ]; then
	echo ">>> Removing mdwikix directory..."
    rm -rf mdwikix || { echo "Failed to remove mdwikix directory"; }
fi

$HOME/local/bin/python3 -m pip install -r pybot/requirements.in
pip install --upgrade pip

find pybot -type f ! -name "*.pyc" -exec chmod 6770 {} \;

echo ">>> Script execution completed successfully."
