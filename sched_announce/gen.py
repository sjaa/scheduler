import pdb
import datetime
from   .models               import AnnounceType, Announce
from   sched_core.sched_log  import sched_log
from   sched_core    .const  import DAY
from   sched_core    .config import TZ_LOCAL, local_time_str
from   .config               import AnnounceChannel, channel_name
from   .config_func          import func_announce


# When announcements are accepted (draft=True -> draft=False), process
# announcements.  Meetup is currently the only channel requiring
# pre-processing when announcements are accepted.
def announce_gen(modeladmin, request, queryset):
    # TODO: how to use modeladmin, request ??
#   pdb.set_trace()
    for event in queryset:
        if event.draft or not event.planned:
            # don't generate announcements for draft or unplanned events
            print("announce_gen: skipped - draft or unplanned")
            continue
        event_type = event.event_type
        date = event.date_time.astimezone(TZ_LOCAL).date()
        announce_types = AnnounceType.objects.filter(event_type=event_type)
        #
        # get event event_type.group
        group = event.group
        # get coordinator of event_type.group
#       owner = UserPermission.objects.filter(coordinator=ev.group)[0].user
        for announce_type in announce_types:
            a = Announce(event_type    = event_type,
                         event         = event,
                         announce_type = announce_type,
                         channel       = announce_type.channel,
                         send          = announce_type.send,
                         is_preface    = announce_type.is_preface,
                         use_header    = announce_type.use_header,
                         lead_title    = announce_type.lead_title,
#                        publish_later = announce_type.publish_later,
#                        allow_change  = announce_type.allow_later,
                         notes         = announce_type.notes,
                         question      = announce_type.question,
                         rsvp_limit    = announce_type.rsvp_limit,
#                        group         = announce_type.group,
                         date          = date - DAY*announce_type.days_offset,
                         draft         = True)
            a.save()

def send_post(modeladmin, request, queryset):
#   pdb.set_trace()
    for channel, announces in classify_channels(queryset).items():
        try:
            #func = func_post[channel]
            func = func_announce[channel]
        except:
            sched_log.error('no announce post function for channel {}'.
                            format(channel))
            continue
        func.post(channel, announces)

def send_update(modeladmin, request, queryset):
    for channel, announces in classify_channels(queryset).items():
        try:
            #func = func_update[channel]
            func = func_announce[channel]
        except:
            sched_log.error('no announce update function for channel {}'.
                            format(channel))
            continue
        func.update(channel, announces)

message = '''\
channel : {}
event   : {}
date    : {}
location: {}'''

def send_announce(modeladmin, request, queryset):
    for channel, announces in classify_channels(queryset).items():
        try:
            func = func_announce[channel]
        except:
            sched_log.error('no announce announce function for channel {}'.
                            format(channel))
            continue
        func.announce(channel, announces)


def send_cancel(modeladmin, request, queryset):
    pdb.set_trace()
    # TODO: need way to send separately to meetup and others
#   meetup.cancel(queryset)
    for channel, announces in classify_channels(queryset).items():
        try:
            func = func_announce[channel]
        except:
            sched_log.error('no announce announce function for channel {}'.
                            format(channel))
            continue
        func.cancel(channel, announces)

def send_delete(modeladmin, request, queryset):
    # TODO: need way to send separately to meetup and others
    pass
#   meetup.delete(queryset)


def classify_channels(queryset):
    '''
    Construct dictionary by announcements by channel
    '''
    channel_dict = {}
    for an in queryset:
        channel = an.channel
        if channel in channel_dict:
            channel_dict[channel].append(an)
        else:
            channel_dict[channel] = [an]
    return channel_dict

from sched_ev.models import Event

GCAL_TEST = True

# TODO: caller needs to trap on no 'announce_type" found
def gen_cal(announce_type, start, end):
    if announce_type.location:
        events = Event.objects.filter(date_time__gte=start, date_time__lte=end,
                                      location=announce_type.location, planned=True) \
                                     .order_by('date_time')
    elif announce_type.category:
        events = Event.objects.filter(date_time__gte=start, date_time__lte=end,
                                      category=announce_type.category, planned=True) \
                                     .order_by('date_time')
    else:
        # TODO: display error message
        events = None
#   elif announce_type.category:
#       events = Event.objects.filter(date_time__gte=start, date_time__lte=end, category=announce_type.category)
    for event in events:
        if GCAL_TEST:
            print('{:30}: {:30} - {}'.format(channel_name[announce_type.channel],
                                             event.name(), local_time_str(event.date_time)))
        else:
            gcal_insert(event, announce_type.channel)

