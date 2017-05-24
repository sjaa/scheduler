#! /bin/bash

if [ ! -f backups/archive ]; then
    mkdir -p backups/archive
fi

for app in 'auth.group' 'sched_ev' 'sched_announce' 'sched_core' 'membership'
#for app in 'auth.group'
do
    echo app: $app
    today=`date "+%Y-%m-%d-%H%M"`
    new_backup=backups/backup_$app-$today.json
    python3 ./manage.py dumpdata --indent 4 --natural-foreign $app > $new_backup
    gzip -9 $new_backup
done
