#!/bin/bash
# toolforge-jobs run updatetdapi --image  --command "~/shs/update_td_api.sh" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=TD_API
REPO_PATH="public_html/api"
$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

echo "Script execution completed successfully."
