#!/bin/bash
# toolforge-jobs run updatestats --image python3.11 --command "~/shs/update_editor_stats.sh" --wait
export SUB_DIR_COPY=""
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=editors_stats
REPO_PATH="pybot/editor_stats"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

echo "python3 pybot/editor_stats/start.py"
