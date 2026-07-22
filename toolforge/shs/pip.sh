#!/bin/bash

# use bash strict mode
set -euo pipefail

$HOME/local/bin/python3 -m pip install --upgrade pip
$HOME/local/bin/python3 -m pip install -r pybot/requirements.in

# toolforge-jobs run pipup --image python3.11 --command ~/shs/pip.sh --wait
