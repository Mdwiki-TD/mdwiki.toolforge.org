#!/bin/bash
set -e

REPO_URL="https://github.com/Mdwiki-TD/fix_refs.git"
TARGET_DIR="public_html/fix_refs"
TARGET_DIR_2="public_html/fix_refs2"

# Navigate to the project directory
cd $HOME || exit 1

# Remove any existing backup directory
rm -rf "$TARGET_DIR_2"

# Clone the repository
if git clone "$REPO_URL" "$TARGET_DIR_2"; then
    # Copy JSON file if it exists
    if [ -f "$TARGET_DIR_2/all_pages_revids.json" ]; then
        rm "$TARGET_DIR_2/all_pages_revids.json"
    fi

    rm -rf "$TARGET_DIR_2"/.git
    cp -rf "$TARGET_DIR_2"/* "$TARGET_DIR/" -v

    # Remove backup directory
    rm -rf "$TARGET_DIR_2" -v

    echo "Repository cloned successfully."
    chmod -R 6774 "$TARGET_DIR"
else
    echo "Failed to clone the repository." >&2
    exit 1
fi
