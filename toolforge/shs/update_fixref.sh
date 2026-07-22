#!/bin/bash
# toolforge-jobs run updatefixref --image python3.11 --command "~/shs/update_fixref.sh update" --wait
export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1

# Optional clean of jsons files before copy to avoid issues with old jsons files
export REMOVE_SRC_JSONS_BEFORE_COPY=0

# additional file to copy to TARGET_DIR
export COPY_TO_TARGET=""

REPO_NAME="fix_refs"
TARGET_DIR="public_html/fix_refs"
BRANCH="${1:-main}"

# Run deploy
$HOME/shs/deploy_php_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"

chmod -R 6774 "$TARGET_DIR"
