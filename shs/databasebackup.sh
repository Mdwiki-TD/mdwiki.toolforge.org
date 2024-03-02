#!/bin/bash
export PATH=/data/project/mdwiki/local/bin:/usr/local/bin:/usr/bin:/bin
#umask o-r # dump should not be public (unless the database is)
mysqldump --defaults-file=~/replica.my.cnf --host=tools.db.svc.wikimedia.cloud s54732__mdwiki > ~/databasebackup/mdwiki-$(date -I).sql
#umask 0022 # restore default umask
