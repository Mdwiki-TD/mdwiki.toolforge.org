#!/bin/bash
# toolforge-jobs run updatetdapi --image  --command "~/shs/update_td_api.sh" --wait

export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1

# Optional clean of jsons files before copy to avoid issues with old jsons files
export REMOVE_SRC_JSONS_BEFORE_COPY=0

# additional file to copy to TARGET_DIR
export COPY_TO_TARGET=""

REPO_NAME=TD_API
TARGET_DIR="public_html/api"
BRANCH="${1:-main}"

# Run deploy
$HOME/shs/deploy_php_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"

echo "Script execution completed successfully."
