#!/bin/bash
# toolforge-jobs run updateauth --image python3.11 --command "~/shs/update_auth.sh" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME=auth-repo
REPO_PATH="public_html/auth"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"

# Additional cleanup (when not using src/ sub-directory)
# Remove composer files
rm -f "$REPO_PATH/composer.json" "$REPO_PATH/composer.lock"

# Remove vendor directory
rm -rf "$REPO_PATH/vendor"

# Delete all JSON files
find "$REPO_PATH" -name "*.json" -delete
