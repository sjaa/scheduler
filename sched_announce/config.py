import pdb
import datetime
from   collections import defaultdict

from   sched_core.const     import FMT_HMP
from   sched_core.config    import TZ_LOCAL, EventLocation
from   sched_announce.const import AnnounceChannel, MEETUP_GROUP_URLNAME
# TODO: temporary
from   django.contrib.auth.models import User

meetup_venue_id = {
    EventLocation.HougeParkBld1.value : '914546',  # TODO: get from Meetup
    EventLocation.HougePark    .value : '914546',
    EventLocation.CampbellPark .value : '23756064',
    EventLocation.CupertinoCCtr.value : '23755360',
    EventLocation.DeAnzaCollege.value : '22341202',
    EventLocation.RanchoCanada .value : '1469015', # old:'5163192',
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
#   EventLocation.HougePark    .value : 'Near the tennis courts'
    EventLocation.HougePark    .value : 'Sidewalk between tennis courts and parkinglot',
    EventLocation.CoyoteValley .value : 'near canyon',
}


def header_dict(announce):
    event = announce.event
    start_time = event.date_time.astimezone(TZ_LOCAL).strftime(FMT_HMP).lstrip('0')
    end_time   = (event.date_time + event_time_lengt).astimezone(TZ_LOCAL).strftime(FMT_HMP).lstrip('0')
    # TODO: hack - remove next 4 lines later when events have owners
    if event.nickname == 'Astronomy 101':
        lead = User.objects.get(username='teruo').get_full_name()
    else:
        lead = ''
    sub_dict = defaultdict(lambda: '<*** LABEL NOT DEFINED ***>', {
        'title'          : event.name(),
        'date'           : event.date_time.astimzone(TZ_LOCAL).date,
        'time'           : '{} - {}'.format(start_time, end_time),
        'lead_title'     : announce.lead_title,
        'lead'           : lead
        # TODO: add later
#       'lead'           : event.owner.get_full_name(),
    })
    return sub_dict

objects_month_talk = {
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
}

objects_month_observe = {
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

def descr_dict(announce):
    month_objs = {
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
    }
    event = announce.event
    # TODO: hack - remove next 4 lines later when events have owners
    if event.nickname == 'Astronomy 101':
        lead = User.objects.get(username='teruo').get_full_name()
    else:
        lead = ''
    month      = event.date_time.astimezone(TZ_LOCAL).month
    before_end = (event.date_time + event.time_length -
                  datetime.timedelta(minutes=30)).astimezone(TZ_LOCAL)
    sub_dict = defaultdict(lambda: '<*** LABEL NOT DEFINED ***>', {
        'lead_title'     : announce.lead_title,
        'lead'           : lead,
        # TODO: add later
#       'lead'           : event.owner.get_full_name(),
        'month_objs'     : month_objs[month],
        '30MinBeforeEnd' : before_end.strftime(FMT_HMP).lstrip('0')
    })
    if announce.channel == AnnounceChannel.Meetup.value:
        sub_dict['meetup_url'] = 'www.meetup/{}/events/{}'.format(MEETUP_GROUP_URLNAME, announce.event_api_id)
#   pdb.set_trace()
    return sub_dict

