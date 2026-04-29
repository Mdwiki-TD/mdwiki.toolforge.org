#!/bin/bash
# toolforge-jobs run updatehtml --image python3.11 --command "~/shs/update_html.sh" --wait

export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="public_html"
export CLEAN_INSTALL=0

# Optional clean of jsons files before copy to avoid issues with old jsons files
export REMOVE_SRC_JSONS_BEFORE_COPY=1

# additional file to copy to TARGET_DIR
export COPY_TO_TARGET=""

REPO_NAME="mdwiki.toolforge.org"
TARGET_DIR="public_html"
BRANCH="${1:-main}"

# Run deploy
$HOME/shs/deploy_php_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"
