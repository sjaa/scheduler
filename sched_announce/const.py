from   enum             import Enum, unique
import datetime

from   sched_core.const  import TZ_UTC


EPOCH     = datetime.datetime(1970, 1, 1, 0, 0)
EPOCH_UTC = TZ_UTC.localize(EPOCH)

MEETUP_GROUP_URLNAME = 'SJ-Astronomy'

@unique
class AnnounceChannel(Enum):
    Meetup       = 1
    SJAA_email   = 2
    member_email = 3
#   Twitter      = 4
#   Facebook     = 5
#   Wordpress    = 6


channel_name = {
    AnnounceChannel.Meetup      .value: 'Meetup',
    AnnounceChannel.SJAA_email  .value: 'SJAA Announce List',
    AnnounceChannel.member_email.value: 'Member email',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
#   AnnounceChannel.Wordpress   .value: 'Wordpress',
}

