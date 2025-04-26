#!/bin/bash
export PATH=/data/project/mdwiki/local/bin:/usr/local/bin:/usr/bin:/bin

# tfj run dbbackup --image mariadb --command "$HOME/jobs/db_backup.sh"

db_name="s54732__mdwiki"
backup_dir="databasebackup"
backup_base="mdwiki-$(date -I).sql"
backup_file="$backup_dir/$backup_base"

echo "backup_file: $backup_file"

# check if the backup directory exists, if not create it
if [ -f ~/"$backup_file" ]; then
    random_suffix=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 6)
    backup_file="${backup_dir}/mdwiki-$(date -I)-$random_suffix.sql"
    echo "File already exists. Using new name: $backup_file"
fi

echo "Starting backup..."

mysqldump --defaults-file=~/replica.my.cnf --host=tools.db.svc.wikimedia.cloud "$db_name" > ~/"$backup_file"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully"
else
    echo "Backup failed."
fi
