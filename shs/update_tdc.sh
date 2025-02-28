#!/bin/bash
set -e

REPO_URL="https://github.com/Mdwiki-TD/tdc.git"
TARGET_DIR="public_html/tdc"
TARGET_DIR_2="public_html/tdc2"

# Navigate to the project directory
cd /data/project/mdwiki/ || exit 1

# Remove any existing backup directory
rm -rf "$TARGET_DIR_2"

# Clone the repository
if git clone "$REPO_URL" "$TARGET_DIR_2"; then
    cp "$TARGET_DIR_2/*" "$TARGET_DIR/"

    # Remove backup directory
    rm -rf "$TARGET_DIR_2"

    echo "Repository cloned successfully."
    chmod -R 6774 "$TARGET_DIR"
else
    echo "Failed to clone the repository." >&2
    exit 1
fi
