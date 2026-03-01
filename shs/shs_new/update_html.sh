#!/bin/bash
# toolforge-jobs run updatehtml --image python3.11 --command "~/shs/update_html.sh" --wait
export SUB_DIR_COPY="public_html"
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=mdwiki.toolforge.org
REPO_PATH="public_html"

# Temporarily disable CLEAN_INSTALL for this special case
# because we need to handle the merge manually
export CLEAN_INSTALL=0

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

# Remove sub-directories that are managed by other repos
rm -rf "$REPO_PATH/Translation_Dashboard"
rm -rf "$REPO_PATH/publish"
rm -rf "$REPO_PATH/api"

# Delete all JSON files
find "$REPO_PATH" -name "*.json" -delete
