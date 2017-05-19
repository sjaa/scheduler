## Use below for crontab

#! /bin/sh
PATH=/usr/bin:/usr/local/bin

0 2 * * *  cd /Users/teruo/Documents/Apps/scheduler && python3 manage.py membership_expiration
