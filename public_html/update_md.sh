#!/bin/bash
# diffine $PATH
export PATH=/data/project/mdwiki/local/bin:/usr/local/bin:/usr/bin:/bin

toolforge jobs run updatemd --command "/data/project/mdwiki/update_mdcore.sh" --image mariadb

echo "toolforge jobs run updatemd --command "/data/project/mdwiki/pybot/update_mdcore.sh" --image mariadb"

toolforge jobs list