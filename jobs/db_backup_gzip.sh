#!/bin/bash
export PATH=/data/project/mdwiki/local/bin:/usr/local/bin:/usr/bin:/bin

# tfj run db1 --image mariadb --command "$HOME/jobs/db_backup_gzip.sh"

dbs=("s54732__mdwiki" "s54732__mdwiki_new")
backup_dir=~/databasebackup

mkdir -p "$backup_dir"

today=$(date -I)

for db_name in "${dbs[@]}"; do
    # استخراج اسم القاعدة المختصر (بدون s54732__)
    short_name="${db_name#s54732__}"
    base_name="${short_name}-${today}"
    suffix=""
    counter=1

    # توليد اسم فريد إذا كان الملف موجودًا
    while [ -e "$backup_dir/${base_name}${suffix}.sql.gz" ]; do
        suffix="_$counter"
        ((counter++))
    done

    backup_file="${base_name}${suffix}.sql.gz"
    full_path="$backup_dir/$backup_file"

    echo "Backing up $db_name to $full_path..."

    mysqldump --defaults-file=~/replica.my.cnf --host=tools.db.svc.wikimedia.cloud "$db_name" | gzip -9 > "$full_path"

    if [ $? -eq 0 ]; then
        echo "✅ Backup of $db_name completed: $full_path"
    else
        echo "❌ Backup of $db_name failed."
    fi
done
