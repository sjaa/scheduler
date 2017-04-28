from   enum        import Enum, unique

TEST_EMAIL_MODE = 'print'  # 'test email'
TEST_EMAIL_ADDR = 'Membership Chair <scehduler@sjaa.net>'

@unique
class MembershipStatus(Enum):
    expired   =   0  # 'expired' must be < 'expiring'
    expiring  =  10
    active    =  11
    admin     = 100
    coordator = 200


CHOICES_MEM_STATUS = (
        ( MembershipStatus.expired .value, 'expired' ),
        ( MembershipStatus.expiring.value, 'expiring'),
        ( MembershipStatus.active  .value, 'active'  )
)

# Send membership renewal notices:
#   30 and 7 days before and 1 day after expiration date
#   -n means 'n' days before, n means days after expiration
RENEWAL_NOTICE_DAYS         = (-30, -7, 1)
MEMBERSHIP_CHAIR_EMAIL_ADDR = 'Membership Chair <membership@sjaa.net>'

RENEWAL_NOTICE_TEXT = '''\
# To: {addr_to}
# From: {addr_from}
# Subject: {subject}

{first_name},

Your SJAA membership will expire in {days} days on {date}.  To renew your membership, please go to:
    https://www.sjaa.net/join-the-sjaa/

Sincerely,

Dave Ittner
SJAA Membership Chair'''

EXPIRED_NOTICE_TEXT = '''\
# To: {addr_to}
# From: {addr_from}
# Subject: {subject}

{first_name},

Your SJAA membership expired on {date}.  To renew your membership, please go to:
    https://www.sjaa.net/join-the-sjaa/

Sincerely,

Dave Ittner
SJAA Membership Chair'''

