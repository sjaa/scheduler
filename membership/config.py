#########################################################################
#
#   Astronomy Club Membership
#   file: membership/config.py
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

from   enum        import Enum, unique


@unique
class MembershipStatus(Enum):
    expired     =   0  # 'expired' must be < 'expiring'
    expiring    =  10
    active      =  11
    admin       = 100
    coordinator = 200


CHOICES_MEM_STATUS = (
        ( MembershipStatus.expired .value, 'expired' ),
        ( MembershipStatus.expiring.value, 'expiring'),
        ( MembershipStatus.active  .value, 'active'  )
)

# Send membership renewal notices:
#   30 and 7 days before and 1 day after expiration date
#   -n means 'n' days before, n means days after expiration
RENEWAL_NOTICE_DAYS   = (-30, -7, 1)
#MEMBERSHIP_EMAIL_ADDR = 'SJAA Membership <membership@sjaa.net>, scheduler@sjaa.net'
#MEMBERSHIP_EMAIL_ADDR = 'SJAA Membership <president@sjaa.net>'
#MEMBERSHIP_EMAIL_ADDR = 'SJAA Membership <schedule_master@sjaa.net>'
MEMBERSHIP_EMAIL_ADDR = 'schedule_master@sjaa.net'

EMAIL_TEST_HEADER = '''\
# To: {addr_to}
# From: {addr_from}
# Subject: {subject}
# Date: {today}
#
'''

RENEWAL_NOTICE_SUBJECT = 'Your SJAA membership expires {}, notice #{}'
RENEWAL_NOTICE_TEXT = '''\
Hello {name},

Your SJAA membership will expire in {days} days on {date}.  To renew your membership, please go to:
    https://www.sjaa.net/join-the-sjaa/

If your membership expires, I will confiscate your telescope!

Sincerely,

Dave Ittner
SJAA Membership Chair'''


EXPIRED_NOTICE_SUBJECT = 'Your SJAA membership expired, notice #{}'
EXPIRED_NOTICE_TEXT = '''\
Hello {name},

Your SJAA membership expired on {date}.  To renew your membership, please go to:
    https://www.sjaa.net/join-the-sjaa/

I will be arriving shortly to confiscate your telescope!

Sincerely,

Dave Ittner
SJAA Membership Chair'''

