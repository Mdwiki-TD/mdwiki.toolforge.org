#!/bin/bash

BRANCH="${1:-main}"

echo ">>> clone --branch ${BRANCH} ."

REPO_URL="https://github.com/WikiAr/newapi.git"
TARGET_DIR="pybot/new/newapi"
CLONE_DIR="newapi_x"

# Remove any existing clone directory
rm -rf "$CLONE_DIR"

# Clone the repository
if git clone --branch "$BRANCH" "$REPO_URL" "$CLONE_DIR"; then
    echo "Repository cloned successfully."
else
    echo "Failed to clone the repository." >&2
    exit 1
fi

rm -rf "$CLONE_DIR"/.git

# Optional: remove any non-Python files
# find "$CLONE_DIR" -type f ! -name "*.py" -exec rm -rf {} \;

# Copy the required files to the target directory
# cp -rf "$CLONE_DIR/"* "$TARGET_DIR/" -v
# if [ -d "$CLONE_DIR/newapi" ]; then

if [ -d "$CLONE_DIR/newapi/super" ]; then
    cp -rf "$CLONE_DIR/newapi/"* "$TARGET_DIR/" -v
else
    cp -rf "$CLONE_DIR/"* "$TARGET_DIR/" -v
fi

find "$TARGET_DIR" -name "*.pyc" -exec rm -f -v {} +

# Optional: Set permissions
# chmod -R 6770 "$TARGET_DIR"
find "$TARGET_DIR" -type f ! -name "*.pyc" -exec chmod 6770 {} \;

# Optional: Install dependencies
#"$HOME/local/bin/python3" -m pip install -r "$TARGET_DIR/requirements.in"

# Remove the "$CLONE_DIR" directory.
rm -rf "$CLONE_DIR"
