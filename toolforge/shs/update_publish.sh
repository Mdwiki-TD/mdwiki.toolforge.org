#!/bin/bash
# toolforge-jobs run updatepublish2 --image bookworm --command "~/shs/update_publish.sh update" --wait

# ============================
# deploy
# ============================
export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1

# Optional clean of jsons files before copy to avoid issues with old jsons files
export REMOVE_SRC_JSONS_BEFORE_COPY=1

# additional file to copy to TARGET_DIR
export COPY_TO_TARGET=""

REPO_NAME="publish"
TARGET_DIR="public_html/publish"
BRANCH="${1:-main}"

# Run deploy
$HOME/shs/deploy_php_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"

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
