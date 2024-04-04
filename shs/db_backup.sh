#!/bin/bash
export PATH=/data/project/mdwiki/local/bin:/usr/local/bin:/usr/bin:/bin

db_name="s54732__mdwiki"

backup_file="databasebackup/mdwiki-$(date -I).sql"
echo "backup_file: $backup_file"

#umask o-r # dump should not be public (unless the database is)

echo "Starting backup..."

mysqldump --defaults-file=~/replica.my.cnf --host=tools.db.svc.wikimedia.cloud "$db_name" > ~/"$backup_file"

#umask 0022 # restore default umask

if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
else
    echo "Backup failed."
fi
