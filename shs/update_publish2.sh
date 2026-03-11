#!/bin/bash
# toolforge-jobs run updatepublish2 --image bookworm --command "~/shs/update_publish2.sh update" --wait

# ============================
# deploy
# ============================
export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1
export REMOVE_SRC_JSONS_BEFORE_COPY=1

BRANCH="${1:-main}"
REPO_NAME="publish"
REPO_PATH="public_html/publish"

# Run deploy
$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

# ============================
# recreate symlink for all_pages_revids.json
# ============================
# After deploy, create symlink if needed
ALL_PAGES_REVIDS_PATH="$HOME/public_html/publish/all_pages_revids.json"
DATA_PATH="$HOME/data/all_pages_revids.json"

if [ ! -L "$ALL_PAGES_REVIDS_PATH" ] && [ -f "$DATA_PATH" ]; then
    rm -f "$ALL_PAGES_REVIDS_PATH"
    ln -s "$DATA_PATH" "$ALL_PAGES_REVIDS_PATH"
fi
