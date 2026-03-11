#!/bin/bash
# toolforge-jobs run updatepublish --image python3.11 --command "~/shs/update_publish.sh" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=publish
REPO_PATH="public_html/publish"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

# Copy publish_reports separately
cp -rf "$REPO_PATH/publish_reports/*.*" public_html/publish_reports/ -v
rm -rf "$REPO_PATH/publish_reports"

chmod -R 6774 "$REPO_PATH"
