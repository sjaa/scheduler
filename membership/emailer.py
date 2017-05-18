#########################################################################
#
#   Astronomy Club Membership
#   file: membership/emailer.py
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
from   sched_core.test  import TestModes
from   sched_core.gmail import send_gmail
from   .config          import MEMBERSHIP_EMAIL_ADDR

def send_email(addr_from, addr_to, subject, body, test_modes):
    if TestModes.Email_To_Tester.value in test_modes:
        addr_to = MEMBERSHIP_EMAIL_ADDR
    send_gmail('me', addr_to, subject, body, test_modes)
