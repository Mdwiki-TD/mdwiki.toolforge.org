#!/bin/bash
# toolforge-jobs run updatestats --image python3.11 --command "~/shs/update_editor_stats.sh" --wait
export USER_NAME="Mdwiki-TD"
export SUB_DIR_COPY=""
export CLEAN_INSTALL=1

# Optional clean of jsons files before copy to avoid issues with old jsons files
export REMOVE_SRC_JSONS_BEFORE_COPY=0

# Ensure the Python3 binary exists before compiling
export PYTHON_BIN="$HOME/local/bin/python3"
export COMPILE_PYTHON_FILES=1

# additional file to copy to TARGET_DIR
export COPY_TO_TARGET=""

REPO_NAME=editors_stats
TARGET_DIR="pybot/editor_stats"
BRANCH="${1:-main}"

# Run deploy
$HOME/shs/deploy_repo.sh "$REPO_NAME" "$TARGET_DIR" "$BRANCH"

echo "python3 pybot/editor_stats/start.py"
