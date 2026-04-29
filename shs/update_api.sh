#!/bin/bash
# toolforge-jobs run update --image python3.11 --command "~/shs/update_api.sh" --wait
export SUB_DIR_COPY="newapi"
export CLEAN_INSTALL=1
export USER_NAME="WikiAr"
BRANCH="${1:-main}"
REPO_NAME=newapi
TARGET_DIR="pybot/new/newapi"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"
