#!/bin/bash
# toolforge-jobs run updatetdc --image python3.11 --command "~/shs/update_tdc.sh" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=tdc
REPO_PATH="public_html/tdc"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

chmod -R 6774 "$REPO_PATH"
