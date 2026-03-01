#!/bin/bash
# toolforge-jobs run updatehtml --image python3.11 --command "~/shs/update_html.sh" --wait
export SUB_DIR_COPY="public_html"
export CLEAN_INSTALL=0
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME="mdwiki.toolforge.org"
REPO_PATH="public_html"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"
