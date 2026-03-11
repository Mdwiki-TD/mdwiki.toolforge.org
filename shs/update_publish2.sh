#!/bin/bash
# toolforge-jobs run updatepublish2 --image bookworm --command "~/shs/update_publish2.sh update" --wait
export USER_NAME="Mdwiki-TD"

export SUB_DIR_COPY="src"
export CLEAN_INSTALL=0
export REMOVE_SRC_JSONS_BEFORE_COPY=1

BRANCH="${1:-main}"
REPO_NAME="publish"
REPO_PATH="public_html/publish"

# copy `~/public_html/publish/all_pages_revids.json` to `~/data` before start deploy, overwrite, make sure `~/data` exist
ALL_PAGES_REVIDS_PATH="$HOME/public_html/publish/all_pages_revids.json"

# Ensure ~/data directory exists
mkdir -p "$HOME/data"

# Copy all_pages_revids.json to ~/data (overwrite if exists)
if [ -f "$ALL_PAGES_REVIDS_PATH" ]; then
    cp "$ALL_PAGES_REVIDS_PATH" "$HOME/data/"
fi

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

