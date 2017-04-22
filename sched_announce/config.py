import pdb
import datetime
from   enum             import Enum, unique
from   collections import defaultdict

from   sched_core.const      import FMT_HMP
from   sched_core.const      import TZ_UTC
from   sched_core.config     import TZ_LOCAL, EventLocation
# can't "import meetup" since "meetup" is an installed module
#from   sched_announce        import meetup

EPOCH     = datetime.datetime(1970, 1, 1, 0, 0)
EPOCH_UTC = TZ_UTC.localize(EPOCH)


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

func_announce = {
#        AnnounceChannel.Meetup      .value : meetup,
#       AnnounceChannel.SJAA_email  .value : None,
#       AnnounceChannel.member_email.value : None,
#       AnnounceChannel.Twitter     .value : None,
#       AnnounceChannel.Facebook    .value : None,
#       AnnounceChannel.Wordpress   .value : None
}

descr_month_dict = {
    'objects_month_talk' : {
         1 : "Tom, Dick, and Harry",
         2 : "Jane, May, and Jane Jr.",
         3 : "Mickey, Minnie, Donald",
         4 : "Bugs, Yosemite Sam, Daffy",
         5 : "Houge Park, Rancho, Mendoza",
         6 : "Grand Canyon, Zion, Bryce Canyon",
         7 : "Florida, Mississippi, Alabama",
         8 : "Cal, San Jose State, Stanford",
         9 : "Google, Yahoo, Bing",
        10 : "Mac, Microsoft, Linux",
        11 : "Soba, Spagehtti, Macaroni",
        12 : "partridge, doves, french hens"
    },

    'objects_month_observe' : {
         1 : "vanilla",
         2 : "chocolate",
         3 : "black cherry",
         4 : "rocky road",
         5 : "pecan",
         6 : "caramel swirl",
         7 : "strawberry",
         8 : "mango",
         9 : "fermented socks",
        10 : "dirt",
        11 : "earthworm",
        12 : "liver"
    }
}


# ---------------- for Meetup ---------------- 

MEETUP_GROUP_URLNAME = 'SJ-Astronomy'

meetup_venue_id = {
    EventLocation.HougeParkBld1.value : '914546',  # TODO: get from Meetup
    EventLocation.HougePark    .value : '914546',
    EventLocation.CampbellPark .value : '23756064',
    EventLocation.CupertinoCCtr.value : '23755360',
    EventLocation.DeAnzaCollege.value : '22341202',
    EventLocation.RanchoCanada .value : '916307', #'1469015', # old:'5163192',
#   EventLocation.MendozaRanch .value : 
    EventLocation.CoyoteValley .value : '24160227',
#   EventLocation.PinnaclesEast.value : 
    EventLocation.PinnaclesWest.value : '24044876',
#   EventLocation.YosemiteNPGP .value :
#   EventLocation.Other        .value : 
}

meetup_urlname = {
#   AnnounceChannel.GCal        .value: '',
    AnnounceChannel.Meetup      .value: 'SJ-Astronomy',
#   AnnounceChannel.Meetup_OSA  .value: 'OSA-Hiking-Enthusiasts',
#   AnnounceChannel.SJAA_email  .value: '',
#   AnnounceChannel.member_email.value: '',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
#   AnnounceChannel.Wordpress   .value: 'Wordpress',
}

channel_url_base = {
#   AnnounceChannel.GCal        .value: '',
    AnnounceChannel.Meetup      .value: 'https://www.meetup.com/SJ-Astronomy/events',
#   AnnounceChannel.Meetup_OSA  .value: 'https://www.meetup.com/OSA-Hiking-Enthusiasts/events',
#   AnnounceChannel.SJAA_email  .value: '',
#   AnnounceChannel.member_email.value: '',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
#   AnnounceChannel.Wordpress   .value: 'Wordpress',
}

how_to_find_us = {
    EventLocation.HougeParkBld1.value : 'Bld. 1, near the parking lot',
    EventLocation.HougePark    .value : 'Sidewalk between tennis courts and parking lot',
    EventLocation.CoyoteValley .value : 'near canyon',
    EventLocation.RanchoCanada .value : \
            'Take Hwy 85 to Hwy 101 South to Bailey Ave and ' +
            'turn Right (West). In 3 miles, Turn Left on McKean Rd. Go 2.4 mi ' +
            'to Casa Loma Rd. Turn Right. After a small white bridge (1.5mi), ' +
            'Parking for RCDO is on your Left. CU there.'
}


# ---------------- for GCal ---------------- 
gcal_id = {
    AnnounceChannel.GCal_Members   .value: 'sjaa.net_ad4o6j2q01jdigilruhhnvrc68@group.calendar.google.com',
    AnnounceChannel.GCal_Public    .value: 'sjaa.net_mi4jf0ai17pku03hgqh0p5tg28@group.calendar.google.com',
    AnnounceChannel.GCal_Houge_out .value: 'sjaa.net_b70r5am24c63o83i225sma8f5c@group.calendar.google.com',
    AnnounceChannel.GCal_Houge_Bld1.value: 'sjaa.net_u75uno2jo1boduiiceks7mgcqg@group.calendar.google.com',
    AnnounceChannel.GCal_OSA       .value: 'sjaa.net_44bomuhts64nsmsgg302hdun5c@group.calendar.google.com'
}

