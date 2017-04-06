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
    Meetup_OSA   = 5
#   Twitter      = 6
#   Facebook     = 7
#   Wordpress    = 8


channel_name = {
    AnnounceChannel.GCal        .value: 'Google Calendar',
    AnnounceChannel.Meetup      .value: 'Meetup SJAA',
    AnnounceChannel.Meetup_OSA  .value: 'Meetup OSA',
    AnnounceChannel.SJAA_email  .value: 'SJAA Announce List',
    AnnounceChannel.member_email.value: 'Member email',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
#   AnnounceChannel.Wordpress   .value: 'Wordpress',
}

channel_public = {
    AnnounceChannel.GCal        .value: False,
    AnnounceChannel.Meetup      .value: True ,
    AnnounceChannel.Meetup_OSA  .value: True ,
    AnnounceChannel.SJAA_email  .value: True ,
    AnnounceChannel.member_email.value: False,
#   AnnounceChannel.Twitter     .value: True ,
#   AnnounceChannel.Facebook    .value: True ,
#   AnnounceChannel.Wordpress   .value: False
}
