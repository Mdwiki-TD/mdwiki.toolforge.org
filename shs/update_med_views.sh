#!/bin/bash
# toolforge-jobs run updateviews --image python3.11 --command "~/shs/update_med_views.sh" --wait
export SUB_DIR_COPY=""
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=med_views
REPO_PATH="pybot/med_views"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

rm -rf pybot/med_views/dumps -v

echo "python3 pybot/med_views/start.py"
