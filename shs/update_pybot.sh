#!/bin/bash
# toolforge-jobs run update --image python3.11 --command "~/shs/update_api.sh" --wait
export SUB_DIR_COPY=""
export CLEAN_INSTALL=0
export USER_NAME="Mdwiki-TD"
BRANCH="${1:-main}"
$HOME/shs/deploy_repo.sh "mdwiki-python-files" pybot "$BRANCH"
