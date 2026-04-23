#!/bin/bash
# toolforge-jobs run updatepublishreports --image bookworm --command "~/shs/update_publish_reports.sh update" --wait

export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="publish_reports"
export CLEAN_INSTALL=1
export REMOVE_SRC_JSONS_BEFORE_COPY=1

BRANCH="${1:-main}"
REPO_NAME="publish"
REPO_PATH="public_html/publish_reports"

# Run deploy
$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"
