#!/bin/bash
# toolforge-jobs run installar --image python3.11 --command "~/shs/update_ArWikiCats.sh" --wait
# sed -i 's/\r$//' ~/shs/*.sh && chmod +x ~/shs/*.sh

# use bash strict mode
set -euo pipefail

REPO_NAME="$1"        # e.g. cats_maker
TARGET_DIR="$2"       # e.g. bots/cats_maker

BRANCH="${3:-main}"
SUB_DIR_COPY="${SUB_DIR_COPY:-}"
USER_NAME="${USER_NAME:-MrIbrahem}"
BASE_DIR="${BASE_DIR:-${HOME}}"

CLONE_DIR="${BASE_DIR}/${REPO_NAME}_tmp"
REPO_URL="https://github.com/${USER_NAME}/${REPO_NAME}.git"

# Navigate to the project directory
cd "$BASE_DIR" || exit

echo ">>> Deploying ${REPO_NAME} (branch: ${BRANCH})"

# Remove any existing clone directory
rm -rf "$CLONE_DIR"

echo ">>> clone --branch ${BRANCH}"
echo "${REPO_URL}"

git clone --branch "$BRANCH" "$REPO_URL" "$CLONE_DIR"

rm -rf "$CLONE_DIR/.git"

# Optional clean of TARGET_DIR
CLEAN_INSTALL="${CLEAN_INSTALL:-0}"

if [ "$CLEAN_INSTALL" = "1" ] && [ -d "$TARGET_DIR" ]; then
    echo ">>> Clean install enabled"
    chmod -R u+w "$TARGET_DIR" 2>/dev/null || true
    # rm -rf "$TARGET_DIR" 2>/dev/null || mv "$TARGET_DIR" "${TARGET_DIR}_old_$(date +%s)"
    mv "$TARGET_DIR" "${TARGET_DIR}_old_$(date +%s)"
fi

mkdir -p "$TARGET_DIR"

# Copy
SRC_DIR="$CLONE_DIR"

if [ -n "$SUB_DIR_COPY" ]; then
    SRC_DIR="$CLONE_DIR/$SUB_DIR_COPY"
    echo ">>> Copying sub-directory: $SRC_DIR"

    if [ ! -d "$SRC_DIR" ]; then
        echo ">>> ERROR: $SRC_DIR does not exist in repo"
        echo ">>> exit."
        exit 1
    fi
fi

cp -rf "$SRC_DIR/"* "$TARGET_DIR/" -v

# Compile all Python files to .pyc explicitly to avoid race conditions
export PYTHONDONTWRITEBYTECODE=1

# Compile all Python files in the TARGET_DIR
"$HOME/local/bin/python3" -m compileall -q -f "$TARGET_DIR"

unset PYTHONDONTWRITEBYTECODE

# Optional: Set permissions
# chmod -R 770 "$TARGET_DIR"
find "$TARGET_DIR" -type f ! -name "*.pyc" -exec chmod 770 {} \;

# Optional: Install dependencies
#"$HOME/local/bin/python3" -m pip install -r "$TARGET_DIR/requirements.in"

# Remove the "$CLONE_DIR" directory.
rm -rf "$CLONE_DIR"

echo ">>> ${REPO_NAME} deployed successfully"
