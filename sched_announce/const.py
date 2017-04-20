from   enum             import Enum, unique
import datetime

from   sched_core.const  import TZ_UTC


EPOCH     = datetime.datetime(1970, 1, 1, 0, 0)
EPOCH_UTC = TZ_UTC.localize(EPOCH)

MEETUP_GROUP_URLNAME = 'SJ-Astronomy'

@unique
class AnnounceChannel(Enum):
#   GCal            =    1
    Meetup          =    2
    # email
    email_SJAA      =   10  # email - SJAA announce
    email_member    =   11  # email - SJAA members
    email_leaders   =   12  # email - SJAA leaders
    # GCal
    GCal_Public     =  100  # all public events
    GCal_Members    =  101  # all members-only events
    GCal_Houge_Bld1 =  110  # For external - City of San Jose, Youth Shakespeare Group
    GCal_Houge_out  =  111  # For external - City of San Jose, Youth Shakespeare Group
    GCal_OSA        =  120  # OSA
    # external
    Meetup_OSA      = 1000  # For OSA Meetup account
#   Ext_Houge_park  = 2000  # For external - City of San Jose, Youth Shakespeare Group
#   Twitter      = 6
#   Facebook     = 7
#   Wordpress    = 8

DEFAULT_CHANNEL = AnnounceChannel.Meetup.value

channel_name = {
    AnnounceChannel.email_SJAA     .value: 'Email SJAA Announce List',
    AnnounceChannel.email_member   .value: 'Email Member',
    AnnounceChannel.email_leaders  .value: 'Email Leaders',
    AnnounceChannel.GCal_Public    .value: 'GCal - SJAA Public',
    AnnounceChannel.GCal_Members   .value: 'GCal - SJAA Member',
    AnnounceChannel.GCal_Houge_Bld1.value: 'GCal - Houge Park Bld. 1',
    AnnounceChannel.GCal_Houge_out .value: 'GCal - Houge Park outdoor',
    AnnounceChannel.GCal_OSA       .value: 'GCal - OSA',
    AnnounceChannel.Meetup         .value: 'Meetup SJAA',
    AnnounceChannel.Meetup_OSA     .value: 'Meetup OSA',
#   AnnounceChannel.Twitter        .value: 'Twitter',
#   AnnounceChannel.Facebook       .value: 'Facebook',
#   AnnounceChannel.Wordpress      .value: 'Wordpress',
}

'''
# TODO: what is this for??
channel_public = {
    AnnounceChannel.GCal        .value: False,
    AnnounceChannel.Meetup      .value: True ,
    AnnounceChannel.Meetup_OSA  .value: True ,
    AnnounceChannel.email_SJAA  .value: True ,
    AnnounceChannel.email_member.value: False,
#   AnnounceChannel.Twitter     .value: True ,
#   AnnounceChannel.Facebook    .value: True ,
#   AnnounceChannel.Wordpress   .value: False
}
'''
