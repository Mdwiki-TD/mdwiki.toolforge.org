#!/bin/bash
# toolforge-jobs run updateauth --image python3.11 --command "~/shs/update_auth.sh" --wait
export SUB_DIR_COPY="src"
export CLEAN_INSTALL=0
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME="auth-repo"
TARGET_DIR="public_html/auth"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"
