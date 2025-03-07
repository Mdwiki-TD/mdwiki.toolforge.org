#!/bin/bash
set -e

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."

REPO_URL="https://github.com/Mdwiki-TD/publish.git"
TARGET_DIR="public_html/publish"
TARGET_DIR_2="public_html/publish2"

# Navigate to the project directory
cd $HOME || exit 1

# Remove any existing backup directory
rm -rf "$TARGET_DIR_2"

# Clone the repository
if git clone --branch "$BRANCH" "$REPO_URL" "$TARGET_DIR_2"; then
    # Copy JSON file if it exists
    if [ -f "$TARGET_DIR_2"/fix_refs ]; then
        rm "$TARGET_DIR_2"/fix_refs
    fi
    cp -rf "$TARGET_DIR_2"/publish_reports/*.* public_html/publish_reports/ -v
    rm -rf "$TARGET_DIR_2"/publish_reports
    cp -rf "$TARGET_DIR_2"/* "$TARGET_DIR/" -v
    # ln -s ~/public_html/fix_refs ~/public_html/publish/fix_refs
    # Remove backup directory
    rm -rf "$TARGET_DIR_2"

    echo "Repository cloned successfully."
    chmod -R 6774 "$TARGET_DIR"
else
    echo "Failed to clone the repository." >&2
    exit 1
fi
