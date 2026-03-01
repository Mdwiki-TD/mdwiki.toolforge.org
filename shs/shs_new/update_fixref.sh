#!/bin/bash
# toolforge-jobs run updatefixref --image python3.11 --command "~/shs/update_fixref.sh" --wait
export SUB_DIR_COPY=""
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=fix_refs
REPO_PATH="public_html/fix_refs"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

# Remove specific JSON file if exists
rm -f "$REPO_PATH/all_pages_revids.json"

chmod -R 6774 "$REPO_PATH"
