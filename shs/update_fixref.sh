#!/bin/bash
# toolforge-jobs run updatefixref --image python3.11 --command "~/shs/update_fixref.sh update" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME="fix_refs"
TARGET_DIR="public_html/fix_refs"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"

chmod -R 6774 "$TARGET_DIR"
