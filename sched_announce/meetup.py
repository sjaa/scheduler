#from models                   import AnnounceType, Announce
#from core.common              import DAY
import pdb
import time
import datetime
from   django.contrib.auth.models import User

from   sched_core.test            import TEST
from   sched_core.const           import DAY
from   sched_core.config          import local_time, local_time_str, local_date_now, local_time_now
from   sched_core.sched_log       import sched_log
from   pythonkc_meetups.client    import PythonKCMeetups
from   .secrets                   import api_key, meetup_organizer
from   .config                    import meetup_urlname, meetup_venue_id, how_to_find_us, \
                                         EPOCH_UTC, AnnounceChannel, channel_name, MEETUP_GROUP_URLNAME
from   .description               import gen_description
from   .event_owner               import get_event_owner
#from   sched_announce.emailer     import send_ann_confirm_email
#from   .emailer                   import send_ann_confirm_email

mu_api = None


def init(channel):
    global mu_api

    mu_api = PythonKCMeetups(meetup_urlname[channel], api_key[channel],
                             http_timeout=600, http_retries=4)


def calc_seconds_since_epoch(t):
    time_since_epoch = t - EPOCH_UTC
    return int(datetime.timedelta.total_seconds(time_since_epoch))


#def send_event(announce, name=None, description=None):
def send_event(announce, name=None):
    # if event_api_id = None, assume new event to Meetup
    event = announce.event
    if announce.channel != AnnounceChannel.Meetup.value:
        # announcement doesn't use Meetup channel
        sched_log.error('announce not for meetup {} {}'.
                        format(event.title, local_time_str(event.date_time)))
        return
    # get event parameters
#   pdb.set_trace()
    name        = name if name else event.name()
    owner       = get_event_owner(event)
    try:
        organizer = meetup_organizer_id(event, owner.id)
    except:
        # no Meetup organizer found.  Meetup defaults to owner of API key
        organizer = None
        sched_log.error('event owner/coordinator not Meetup organizer "{}"  --  {}'.
                       format(event.nickname, local_time_str(event.date_time)))
    # do label substitution in description
    description = gen_description(announce)
    venue       = meetup_venue_id[event.location] \
                      if event.location in meetup_venue_id else None
    find_us     = how_to_find_us[event.location] \
                      if event.location in how_to_find_us else None
#   pdb.set_trace()
    # create/modify event via Meetup API
    return mu_api.post_event(
                name           = name,
                time_start     = int(calc_seconds_since_epoch(event.date_time)),
                duration       = int(event.time_length.total_seconds()),
                venue          = venue,
                description    = description,
                find_us        = find_us,
                organizer      = organizer,
                question       = announce.question,
                rsvp_limit     = announce.rsvp_limit,
                publish_status = 'draft' if announce.draft else 'published',
                event_id       = announce.event_api_id)

# TODO: test - delete later
def foo():
    # hack to set days-to-event to 28 days
    pdb.set_trace()
    announces = Announce.objects.all()
    # update announce date for objects
    for an in announces:
        ev_date = local_time(an.event.date_time).date()
        an.date = ev_date - DAY*28
        an.save()
    announces = AnnounceType.objects.all()
    # update announce offset for objects
    for an in announces:
        an.days_offset = 28
        an.save()

def post(channel, queryset):
#   pdb.set_trace()
    # initialize channel
    init(channel)
    sent = 0
    count = len(queryset)
    # for each announcement
#   pdb.set_trace()
    time_start = time.clock()  # calculate elapsed time to send posts
    for announce in queryset:
        # Ensure 'announce' can be sent
#       if announce.channel != AnnounceChannel.Meetup.value or \
#          announce.event_api_id:  # or \
        if announce.event_api_id:  # or \
           # TODO: add next line later
#          announce.draft:
            # don't send announcement
            count -= 1
            continue
        announce_date = local_time(announce.event.date_time).date()
        if announce_date < local_date_now():
            sched_log.error('event meetup publish date past offset "{}"  --  {},  days: {}'.
                            format(announce.event.title,
                                   local_time_str(event.date_time), announce.days_offset))
            continue
        # post Meetup event
        event_id, ex = send_event(announce)
        if ex:
            sched_log.error('event meetup post exception "{}"  --  {}'.
                            format(announce.event.title, ex))
            continue
        # update database
        event = announce.event
        if event_id:
            announce.event_api_id = event_id
            announce.date_posted = local_time_now()
            announce.save()
            sent += 1
            sched_log.info('meetup event posted "{}"  --  {}  -- id: {}'.
                           format(event.title, local_time_str(event.date_time),
                                  event_id))
        else:
            count -= 1
            sched_log.error('event meetup post failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time_str(event.date_time), ex))
        # delay to prevent rate limit 
        # Meetup x-ratelimit is 30 requests / 10 sec
        time.sleep(0.3)
    # Log results
    time_end = time.clock()
    interval = time_end - time_start
    if sent == count:
        sched_log.info('All new Meetup events posted: {}  -  {:.3f} sec'.
                       format(count, interval))
    else:
        count = len(queryset)
        sched_log.error('Some Meetup events not sent: only {} out of {} posted -  {:.3f} sec'.
                        format(count - sent, count, interval))


def update(channel, queryset):
    # initialize channel
    init(channel)
    for announce in queryset:
        event = announce.event
        if not announce.event_api_id:
            sched_log.error('event meetup announce: event not yet published  "{}"  --  {}'.
                            format(event.title, local_time_str(event.date_time)))
            continue
        # update Meetup post
        status, ex = send_event(announce)
        if status:
            sched_log.info ('meetup event updated "{}"  --  {}  -- id:{}'.
                            format(event.title, local_time_str(event.date_time),
                                   announce.event_api_id))
        else:
            sched_log.error('event meetup update failed "{}"  --  {}  --  {}'.
                 format(event.title, local_time_str(event.date_time), ex))


def announce(channel, queryset):
#   pdb.set_trace()
    init(channel)
    sent = 0
    for announce in queryset:
        event = announce.event
        event_api_id = announce.event_api_id
        if not event_api_id:
            sched_log.error('event meetup announce: event not yet published  "{}"  --  {}'.
                            format(event.title, local_time_str(event.date_time)))
            continue
        if announce.date_announced:
            sched_log.error('event meetup announce: event already announced  "{}"  --  {}'.
                            format(event.title, local_time_str(event.date_time)))
            continue
        if not announce.send:
            sched_log.info ('meetup event not to be published "{}"  --  {}'.
                            format(event.title, local_time_str(event.date_time)))
            continue
        # announce event via Meetup API
#       pdb.set_trace()
        if TEST:
            ex = None
        else:
            ex = mu_api.announce_event(event_api_id)
        if ex:
            sched_log.error('event meetup announce error: "{}" {} --  {}'.
                            format(event.title, local_time_str(event.date_time), ex))
        else:
            if not TEST:
                announce.date_announced = local_time_now()
                announce.save()
# TODO: 4/14
#           send_ann_confirm_email(announce)
            sched_log.info ('meetup announcement sent:  "{}" {} --  {}'.
                            format(event.title, channel_name[channel], local_time_str(event.date_time)))
        # delay to prevent rate limit 
        # Meetup x-ratelimit is 30 requests / 10 sec
        time.sleep(0.3)


def cancel(channel, queryset):
    init(channel)
    for announce in queryset:
        event = announce.event
        if not announce.event_api_id:
            sched_log.error('event meetup announce: event not yet published  "{}"  --  {}'.
                            format(event.title, local_time_str(event.date_time)))
            return
        event_date_time = event.date_time + event.time_length
        if event_date_time < local_time_now():
            sched_log.error('event meetup cancel: attempted after event  "{}"  --  {}'.
                            format(event.title, local_time_str(event.date_time)))
            return
        description = '<b>[{}]</b><br>{}'\
                      .format(announce.text_cancel, announce.description())
        # cancel Meetup event
        ex = mu_api.cancel_event(announce.event_api_id)
        if ex:
            sched_log.error('event meetup cancel: post failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time_str(event.date_time), ex))
            return
        else:
            # update database
            announce.date_canceled  = local_time_now()
            announce.save()
            sched_log.info('meetup event canceled "{}"  --  {}  -- id: {}'.
               format(event.title, local_time_str(event.date_time),
                      announce.event_api_id))
    return


def delete(channel, queryset):
    # initialize channel
    init(channel)
    # for each announcement
    for announce in queryset:
        # delete Meetup event via Meetup API
        result, ex = mu_api.delete_event(announce.event_api_id)
        event = announce.event
        # update database
        if result:
            # TODO: need to decide how to show event was deleted
            announce.date_posted   = None
            announce.date_canceled = None
#           announce.event_api_id  = ''
            announce.save()
            print('meetup event deleted "{}"  --  {}  -- id: {}'.
                           format(event.title, local_time_str(event.date_time),
                                  announce.event_api_id))
        else:
            print('event meetup delete failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time_str(event.date_time), ex))
        # delay to prevent rate limit 
        # Meetup x-ratelimit is 30 requests / 10 sec
        time.sleep(0.3)

