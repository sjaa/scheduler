#! /bin/bash
# dump Django SQL tables
# Generate JSON files and store under 'db_archive'
# Store old *.json.gz under 'db_archive/OLD'

old_archive="db_archive/OLD"
#echo $old_archive
if [ ! -d "db_archive" ]
then
    echo "directory 'db_archive' created"
    mkdir -p db_archive/OLD
fi

today=`date "+%Y_%m_%d_%H%M"`
for table in 'auth.group' 'sched_ev' 'sched_announce' 'membership' 'ipn'
do
    echo table: ${table}
    new_file="db_archive/backup-${today}-${table}.json"
    # Get filename of most recent backup file
    if ls db_archive/backup-*-${table}.json 1> /dev/null 2>&1
    then
        old_file=`ls -1t db_archive/backup-*-${table}.json | head -1`
        echo "  found old file:${old_file}:"
        no_old_file=0
    else
        old_file=""
        no_old_file=1
    fi
    # Generate dump of table
    echo "  generate new dump: " $new_file
    python3 ./manage.py dumpdata --indent 4 --natural-foreign $table > $new_file
    # Skip rest of loop if no old file
    if [ $no_old_file -eq 1 ]
    then
        # no old file
        echo "  no old file, skipping diff"
        continue
    fi
    # Compare with previous file, if applicable.
    python3 json_diff.py $old_file $new_file
    if [ $? -eq 0 ]
    then
        rm $new_file
        echo '  diff - no difference found, removing new file: ' $new_file
    else
        echo "  diff - files are different:" $old_file $new_file
        # If different, gzip previous file
        echo "  archive old file"
        gzip -9 $old_file
        # Archive old file to external archive
        # ??
        # move .gzip file to 'OLD' directory
        mv ${old_file}.gz $old_archive
    fi
done


