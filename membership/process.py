#########################################################################
#
#   Astronomy Club Event Scheduler
#   file: membership/process.py
#
#   Copyright (C) 2017  Teruo Utsumi, San Jose Astronomical Association
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Contributors:
#       2017-06-01  Teruo Utsumi, initial code
#
#########################################################################

import pdb
import datetime
from   django.contrib        import admin
from   sched_core.sched_log  import sched_log
from   sched_core.filters    import AdminDateTimeYearFilter
from   .config               import MembershipStatus
from   .models               import User


def new_membership(user):
    user.status = MembershipStatus.active.value
    user.notice = 0  # reset # of renewal notices
#   user.save()
#   send_email_new(user)
    membership_log.info('New member: {} {} - {} / {} to {} / since: {}'.format(
                        user.first_name, user.last_name, user.email,
                        user.date_start.strftime(FMT_YDATE),
                        user.date_end  .strftime(FMT_YDATE),
                        user.date_since.strftime(FMT_YDATE)))

def renew_membership(user):
    user.status = MembershipStatus.active.value
    user.notice = 0  # reset # of renewal notices
#   user.save()
#   send_email_renew(user)
    membership_log.info('Renewed: {} {} - {} / {} to {}'.format(
                        user.first_name, user.last_name, user.email,
                        user.date_start.strftime('%Y %M %d'),
                        user.date_end  .strftime('%Y %M %d')))

def gen_username(first_name, last_name):
    '''
    make user name
     - lower case
     - replace space with '_'
     - allowable characters:
       - lower case letters
       - digits
       - '@.+=_'
    '''
    name = (first_name + '.' + last_name).lower().replace(' ', '_')
    allowable = '@.+=_'
    new_name = ''
    for c in name:
        if c.isdigit() or c in allowable:
            new_name += c
    count = 1
    tmp_name = new_name[:]
    while User.objects.filter(username=tmp_name):
        tmp_name = new_name + '_' + str(count)
        count += 1
    return tmp_name
