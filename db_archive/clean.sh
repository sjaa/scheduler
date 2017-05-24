#! /bin/bash

for app in 'auth.group' 'sched_ev' 'sched_announce' 'sched_core' 'membership'
#for app in 'auth.group'
do
    # delete all days except 1st, 2nd of each month
    rm backup_${app}-2017-[01][0-9]-0[3-9]-*.json.gz
    rm backup_${app}-2017-[01][0-9]-[1-3]-*.json.gz
