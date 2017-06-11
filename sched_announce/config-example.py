import pdb
import datetime
from   enum             import Enum, unique
from   collections import defaultdict

from   sched_core.const      import FMT_HMP
from   sched_core.const      import TZ_UTC
from   sched_core.config     import TZ_LOCAL, EventLocation


EPOCH     = datetime.datetime(1970, 1, 1, 0, 0)
EPOCH_UTC = TZ_UTC.localize(EPOCH)


@unique
class AnnounceChannel(Enum):
#   GCal            =   1
    Meetup          =   2
    # email
    email_my_org    =  10  # email - announce
    # GCal
    GCal_my_org     = 100  # all public events
#   Twitter         = 200
#   Facebook        = 300

DEFAULT_CHANNEL = AnnounceChannel.Meetup.value

channel_name = {
    AnnounceChannel.email_my_org   .value: 'Email my org Announce List',
    AnnounceChannel.GCal_my_org    .value: 'GCal - my org',
    AnnounceChannel.Meetup         .value: 'Meetup my org',
#   AnnounceChannel.Twitter        .value: 'Twitter',
#   AnnounceChannel.Facebook       .value: 'Facebook',
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

MEETUP_GROUP_URLNAME = 'my-org'

meetup_venue_id = {
    EventLocation.my_location  .value : '111111',  # TODO: get from Meetup
}

meetup_urlname = {
#   AnnounceChannel.GCal        .value: '',
    AnnounceChannel.Meetup      .value: 'my-org',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
}

channel_url_base = {
#   AnnounceChannel.GCal        .value: '',
    AnnounceChannel.Meetup      .value: 'https://www.meetup.com/my-org',
#   AnnounceChannel.Twitter     .value: 'Twitter',
#   AnnounceChannel.Facebook    .value: 'Facebook',
}

how_to_find_us = {
    EventLocation.my_location  .value : 'my location',
}


# ---------------- for GCal ---------------- 
gcal_id = {
    AnnounceChannel.GCal_my_org    .value: 'my_org@group.calendar.google.com',
}
