#!/bin/bash
# toolforge-jobs run updatetd --image python3.11 --command "~/shs/update_td.sh" --wait
# toolforge-jobs run updatetd --image python3.11 --command "~/shs/update_td.sh update_new" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=0
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=Translation-Dashboard
REPO_PATH="public_html/Translation_Dashboard"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"
