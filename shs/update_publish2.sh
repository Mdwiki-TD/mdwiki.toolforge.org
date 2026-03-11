#!/bin/bash
# toolforge-jobs run updatepublish2 --image bookworm --command "~/shs/update_publish2.sh update" --wait

# ============================
# copy all_pages_revids.json
# ============================

# copy `~/public_html/publish/all_pages_revids.json` to `~/data` before start deploy, overwrite, make sure `~/data` exist
ALL_PAGES_REVIDS_PATH="$HOME/public_html/publish/all_pages_revids.json"
DATA_PATH="$HOME/data/all_pages_revids.json"

# Ensure ~/data directory exists
mkdir -p "$HOME/data"

# If file exists and is NOT a symlink, copy it
if [ -e "$ALL_PAGES_REVIDS_PATH" ] && [ ! -L "$ALL_PAGES_REVIDS_PATH" ]; then
    cp "$ALL_PAGES_REVIDS_PATH" "$HOME/data/" -v
fi

# ============================
# deploy
# ============================

export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=0
export REMOVE_SRC_JSONS_BEFORE_COPY=1

BRANCH="${1:-main}"
REPO_NAME="publish"
REPO_PATH="public_html/publish"

# Run deploy
$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

# ============================
# recreate symlink for all_pages_revids.json
# ============================
# After deploy, recreate symlink if needed
if [ ! -L "$ALL_PAGES_REVIDS_PATH" ] && [ -f "$DATA_PATH" ]; then
    rm -f "$ALL_PAGES_REVIDS_PATH"
    ln -s "$DATA_PATH" "$ALL_PAGES_REVIDS_PATH"
fi
