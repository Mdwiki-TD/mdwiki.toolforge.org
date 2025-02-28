#!/bin/bash
set -e

REPO_URL="https://github.com/mdwikicx/publish.git"
TARGET_DIR="public_html/publish"
TARGET_DIR_2="public_html/publish2"

# Navigate to the project directory
cd /data/project/mdwiki/ || exit 1

# Remove any existing backup directory
rm -rf "$TARGET_DIR_2"

# Clone the repository
if git clone "$REPO_URL" "$TARGET_DIR_2"; then
    # Copy JSON file if it exists
    if [ -f "$TARGET_DIR_2/all_pages_revids.json" ]; then
        rm "$TARGET_DIR_2/all_pages_revids.json"
    fi
    cp "$TARGET_DIR_2/*" "$TARGET_DIR/.json"

    # Remove backup directory
    rm -rf "$TARGET_DIR_2"

    echo "Repository cloned successfully."
    chmod -R 6774 "$TARGET_DIR"
else
    echo "Failed to clone the repository." >&2
    exit 1
fi
