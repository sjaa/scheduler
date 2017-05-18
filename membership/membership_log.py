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

import pdb
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
    formatter = logging.Formatter('%(levelname)-7s  %(asctime)s  %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    membership_log = logging.getLogger('Membership logger')
    membership_log.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)
    membership_log.addHandler(handler)
    return membership_log

membership_log = setup_log()

# in files
# from membership_log import *
