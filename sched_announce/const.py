from   enum             import Enum, unique
import datetime

from   sched_core.const  import TZ_UTC


EPOCH     = datetime.datetime(1970, 1, 1, 0, 0)
EPOCH_UTC = TZ_UTC.localize(EPOCH)

MEETUP_GROUP_URLNAME = 'SJ-Astronomy'

@unique
class AnnounceChannel(Enum):
    GCal         = 1
    Meetup       = 2
    SJAA_email   = 3
    member_email = 4
#   Twitter      = 4
#   Facebook     = 5
#   Wordpress    = 6


channel_name = {
    AnnounceChannel.GCal        .value: 'Google Calendar',
    AnnounceChannel.Meetup      .value: 'Meetup',
    AnnounceChannel.SJAA_email  .value: 'SJAA Announce List',
    AnnounceChannel.member_email.value: 'Member email',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
#   AnnounceChannel.Wordpress   .value: 'Wordpress',
}

channel_public = {
    AnnounceChannel.GCal        .value: False,
    AnnounceChannel.Meetup      .value: True ,
    AnnounceChannel.SJAA_email  .value: True ,
    AnnounceChannel.member_email.value: False,
#   AnnounceChannel.Twitter     .value: True ,
#   AnnounceChannel.Facebook    .value: True ,
#   AnnounceChannel.Wordpress   .value: False
}
