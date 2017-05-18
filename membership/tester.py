#########################################################################
#
#   Astronomy Club Membership
#   file: membership/tester.py
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
from   sched_core.const  import DAY
from   sched_core.config import set_local_date
from   .process          import cron_job


def tester(username, date_end, date_current, test_modes, advance_mode):
    did_something = True
    while True:
        # advance one day
#       print('tester: {}'.format(date_current))
        set_local_date(date_current)
        did_something, results = cron_job(username, test_modes)
        date_current += DAY
        if not check_next_date(date_end, date_current, advance_mode, did_something):
            break
    return (date_current, results)

    
def check_next_date(date_end, date_current, advance_mode, did_something):
    if advance_mode == '1day':
        return False
    elif advance_mode == 'next':
        if date_end < date_current or did_something:
            return False
        else:
            return True
    elif advance_mode == 'all':
        return date_end > date_current
    else:
        print('Error: bad advance_mode - {}'.format(advance_mode))
        return False
