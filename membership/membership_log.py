#########################################################################
#
#   Astronomy Club Membership
#   file: membership/membership_log.py
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

import logging
import logging.handlers

FILENAME_LOG = 'membership.log'
current_user = 'sam'

class ContextFilter(logging.Filter):
    """
    this is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.user = current_user
        return True

def setup_log():
    handler = logging.handlers.RotatingFileHandler(FILENAME_LOG, maxBytes=2**20, backupCount=5)
    filename_log     = 'membership.log'
    membership_log = logging.getLogger('Membership logger')
    membership_log.addFilter(ContextFilter())
    logging.basicConfig(level=logging.INFO,
                        filename = FILENAME_LOG,
#                       filemode = 'w',  # with 'w', start new file each time
#                       format   = '%(levelname)-7s  %(asctime)s  %(user)-10s %(message)s',
                        format   = '%(levelname)-7s  %(asctime)s  %(message)s',
                        datefmt  = '%Y/%m/%d  %H:%M:%S')
    membership_log.addHandler(handler)
    return membership_log

membership_log = setup_log()

# in files
# from membership_log import *
