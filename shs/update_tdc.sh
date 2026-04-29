#!/bin/bash
# toolforge-jobs run updatetdc --image python3.11 --command "~/shs/update_tdc.sh" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=0
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME="tdc"
TARGET_DIR="public_html/tdc"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"

chmod -R 6774 "$TARGET_DIR"
