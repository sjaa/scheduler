#from models                   import AnnounceType, Announce
#from core.common              import DAY
import pdb
import time
import datetime
from   sched_core.const           import DAY
from   sched_core.config          import TZ_LOCAL, local_time
from   sched_core.sched_log       import sched_log
from   pythonkc_meetups.client    import PythonKCMeetups
from   sched_announce.description import gen_description
#from   sched_announce.event_owner import get_event_owner, get_event_coordinator
from   sched_announce.event_owner import get_event_owner
#from   sched_announce.secrets     import MEETUP_API_KEY
from   sched_announce.secrets     import api_key, meetup_organizer
from   sched_announce.const       import EPOCH_UTC, AnnounceChannel, channel_name
from   sched_announce.config      import meetup_urlname, meetup_venue_id, how_to_find_us, descr_dict
from   .email                     import send_ann_confirm_email
from   django.contrib.auth.models import User


mu_api = None


def init(channel):
    global mu_api

    mu_api = PythonKCMeetups(meetup_urlname[channel], api_key[channel],
#   mu_api = PythonKCMeetups(MEETUP_GROUP_URLNAME, api_key[channel],
                             http_timeout=600, http_retries=4)


def meetup_organizer_id(owner_id):
    if owner_id in meetup_organizer:
        return meetup_organizer[owner_id]
    # no Meetup organizer found.  Meetup defaults to owner of API key
    sched_log.error('event owner/coordinator not Meetup organizer "{}"  --  {}'.
                   format(event.title, local_time(event.date_time)))
    return


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
                        format(event.title, local_time(event.date_time)))
        return
    # get event parameters
#   pdb.set_trace()
    name        = name if name else event.name()
    owner       = get_event_owner(event)
    organizer   = meetup_organizer_id(owner.id)

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

def foo():
    # hack to set days-to-event to 28 days
    pdb.set_trace()
    announces = Announce.objects.all()
    for an in announces:
        ev_date = an.event.date_time.astimezone(TZ_LOCAL).date()
        now_date = datetime.datetime.now.astimezone(TZ_LOCAL).date()
        an.date = now_date - datetime.timedelta(days=28)
        an.save()
    announces = AnnounceType.objects.all()
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
    time_start = time.clock()
    for announce in queryset:
        if announce.channel != AnnounceChannel.Meetup.value or \
           announce.event_api_id:  # or \
           # TODO: add next line later
#          announce.draft:
            # don't send announcement
            count -= 1
            continue
        announce_date = announce.event.date_time.astimezone(TZ_LOCAL).date()
        if announce_date < datetime.date.today():
            sched_log.error('event meetup publish date past offset "{}"  --  {},  days: {}'.
                            format(announce.event.title, local_time(event.date_time), announce.days_offset))
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
            announce.date_posted = TZ_LOCAL.localize(datetime.datetime.now())
            announce.save()
            sent += 1
            sched_log.info('meetup event posted "{}"  --  {}  -- id: {}'.
                           format(event.title, local_time(event.date_time),
                                  event_id))
        else:
            count -= 1
            sched_log.error('event meetup post failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time(event.date_time), ex))
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
        sched_log.error('Some Meetup events not sent: only {} out of {} posted'.
                        format(count - sent, count, interval))


def update(channel, queryset):
    # initialize channel
    init(channel)
    for announce in queryset:
        event = announce.event
        if not announce.event_api_id:
            sched_log.error('event meetup announce: event not yet published  "{}"  --  {}'.
                            format(event.title, local_time(event.date_time)))
            continue
        # update Meetup post
        status, ex = send_event(announce)
        if status:
            sched_log.info ('meetup event updated "{}"  --  {}  -- id:{}'.
                            format(event.title, local_time(event.date_time),
                                   announce.event_api_id))
        else:
            sched_log.error('event meetup update failed "{}"  --  {}  --  {}'.
                 format(event.title, local_time(event.date_time), ex))


def announce(channel, queryset):
#   pdb.set_trace()
    init(channel)
    sent = 0
    for announce in queryset:
        event = announce.event
        event_api_id = announce.event_api_id
        if not event_api_id:
            sched_log.error('event meetup announce: event not yet published  "{}"  --  {}'.
                            format(event.title, local_time(event.date_time)))
            continue
        if announce.date_announced:
            sched_log.error('event meetup announce: event already announced  "{}"  --  {}'.
                            format(event.title, local_time(event.date_time)))
            continue
        if not announce.send:
            sched_log.info ('meetup event not to be published "{}"  --  {}'.
                            format(event.title, local_time(event.date_time)))
            continue
        # announce event via Meetup API
        send_ann_confirm_email(announce)
        pdb.set_trace()
        ex = mu_api.announce_event(event_api_id)
        if ex:
            sched_log.error('event meetup announce error: "{}" {} --  {}'.
                            format(event.title, local_time(event.date_time), ex))
        else:
            announce.date_announced  = TZ_LOCAL.localize(datetime.datetime.now())
            announce.save()
            # TODO: add next line later
            #send_ann_confirm_email(announce)
            sched_log.info ('meetup announcement sent:  "{}" {} --  {}'.
                            format(event.title, channel_name[channel], local_time(event.date_time).strftime(FMT_YEAR_DATE_HM)))
        # delay to prevent rate limit 
        # Meetup x-ratelimit is 30 requests / 10 sec
        time.sleep(0.3)


def cancel(channel, queryset):
    init(channel)
    for announce in queryset:
        event = announce.event
        if not announce.event_api_id:
            sched_log.error('event meetup announce: event not yet published  "{}"  --  {}'.
                            format(event.title, local_time(event.date_time)))
            return
        event_date_time = event.date_time + event.time_length
        if event_date_time < TZ_LOCAL.localize(datetime.datetime.now()):
            sched_log.error('event meetup cancel: attempted after event  "{}"  --  {}'.
                            format(event.title, local_time(event.date_time)))
            return
        description = '<b>[{}]</b><br>{}'\
                      .format(announce.text_cancel, announce.description())
        # cancel Meetup event
        ex = mu_api.cancel_event(announce.event_api_id)
        if ex:
            sched_log.error('event meetup cancel: post failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time(event.date_time), ex))
            return
        else:
            # update database
            announce.date_canceled  = datetime.datetime.now()
            announce.save()
            sched_log.info('meetup event canceled "{}"  --  {}  -- id: {}'.
               format(event.title, local_time(event.date_time),
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
                           format(event.title, local_time(event.date_time),
                                  announce.event_api_id))
        else:
            print('event meetup delete failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time(event.date_time), ex))
        # delay to prevent rate limit 
        # Meetup x-ratelimit is 30 requests / 10 sec
        time.sleep(0.3)

