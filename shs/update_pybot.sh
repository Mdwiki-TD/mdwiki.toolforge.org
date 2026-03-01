#!/bin/bash
# toolforge-jobs run updatepybot --image python3.11 --command "~/shs/update_pybot.sh" --wait
export SUB_DIR_COPY=""
export CLEAN_INSTALL=0
export COMPILE_PYTHON_FILES=1
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
REPO_NAME="mdwiki-python-files"
REPO_PATH="pybot"

$HOME/shs/deploy_repo.sh "$REPO_NAME" "$REPO_PATH" "$BRANCH"
