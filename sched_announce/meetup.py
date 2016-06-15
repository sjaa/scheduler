#from models                   import AnnounceType, Announce
#from core.common              import DAY
import pdb
import time
import datetime
from   sched_core.const        import DAY, local_time
from   sched_core.config       import TZ_LOCAL, coordinator
from   sched_core.sched_log    import sched_log
from   pythonkc_meetups.client import PythonKCMeetups
from   sched_announce.secrets  import MEETUP_API_KEY
from   sched_announce.const    import EPOCH_UTC, AnnounceChannel
from   sched_announce.config   import meetup_venue_id, how_to_find_us, descr_dict
from   sched_announce.secrets  import meetup_organizer


mu_api = None


def init():
    global mu_api

    if not mu_api:
        mu_api = PythonKCMeetups(MEETUP_API_KEY,
                                 http_timeout=600, http_retries=4)


def calc_seconds_since_epoch(t):
    time_since_epoch = t - EPOCH_UTC
    return int(datetime.timedelta.total_seconds(time_since_epoch))


def organizer_member_id(event):
    # get event owner
    # if owner not Meetup organizer, get group
    if event.owner in meetup_organizer:
        return meetup_organizer[event.owner]
    else:
        group = event.group
        if group not in coordinator:
            return
        user  = coordinator[group]
        if user in meetup_organizer:
            return meetup_organizer[user]
    # no Meetup organizer found.  Meetup defaults to owner of API key
    sched_log.error('event owner/coordinator not Meetup organizer "{}"  --  {}'.
                   format(event.title, local_time(event.date_time)))
    return


def send_event(announce, name=None, description=None):
    # if event_api_id = None, assume new event to Meetup
    event = announce.event
    if announce.channel != AnnounceChannel.Meetup.value:
        # announcement doesn't use Meetup channel
        sched_log.error('Not Meetup announcement {} {}'.
                        format(event.title, local_time(event.date_time)))
        return
    # get event parameters
    name        = name if name else event.name()
    description = description if description else announce.description()
    description = description.format(**descr_dict(announce)) + \
                  '<br>For more info see: <a href={0} target="blank">{0}</a>'.format(event.url)

    venue       = meetup_venue_id[event.location] \
                      if event.location in meetup_venue_id else None
    find_us     = how_to_find_us[event.location] \
                      if event.location in how_to_find_us else None
    organizer   = organizer_member_id(event)
    # create Meetup event
    return mu_api.send_event(
                name        = name,
                time_start  = int(calc_seconds_since_epoch(event.date_time)),
                duration    = int(event.time_length.total_seconds()),
                venue       = venue,
                description = description,
                find_us     = find_us,
                organizer   = organizer,
                event_id    = announce.event_api_id)


def post(queryset):
#   pdb.set_trace()
    # initialize channel
    init()
    sent = 0
    count = len(queryset)
    # for each announcement
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
                            format(event.title, local_time(event.date_time), announce.days_offset))
            continue
        # post Meetup event
        event_id, ex = send_event(announce)
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


def update_event(announce):
    # initialize channel
    init()
    sent = 0
    count = len(queryset)
    # post edited Meetup event
    event_id, ex = send_event(announce)
    # update database
    if event_id:
        announce.event_api_id = event_id
        announce.date_posted = TZ_LOCAL.localize(datetime.datetime.now())
        announce.save()
        sent += 1
        sched_log.info('meetup event edited "{}"  --  {}  -- id: {}'.
           format(event.title, local_time(event.date_time),
                  event_api_id))
    else:
        sched_log.error('event meetup edit failed "{}"  --  {}  --  {}'.
             format(event.title, local_time(event.date_time), ex))
    return event_id


def cancel(queryset):
#   pdb.set_trace()
    # initialize channel
    init()
    sent = 0
    count = len(queryset)
    # for each announcement
    time_start = time.clock()
    for announce in queryset:
        cancel_event(announce)

def cancel_event(announce):
    event = announce.event
    event_date_time = event.date_time + event.time_length
    if event_date_time < TZ_LOCAL.localize(datetime.datetime.utcnow()):
        sched_log.error('event meetup cancel after event  "{}"  --  {}'.
                        format(event.title, local_time(event.date_time)))
        return
    # initialize channel
    init()
    name        = '**** C A N C E L E D   --   {} ****'.format(announce.event.name())
    description = '<b>[{}]</b><br>{}'\
                  .format(announce.text_cancel, announce.description())
    # post edited Meetup event
    event_id, ex = send_event(announce, name, description)
    # update database
    if event_id:
        announce.event_api_id = event_id
        announce.date_canceled  = TZ_LOCAL.localize(datetime.datetime.now())
        announce.save()
        sched_log.info('meetup event canceled "{}"  --  {}  -- id: {}'.
           format(event.title, local_time(event.date_time),
                  announce.event_api_id))
#       # TODO: move to code where cancel is initiated
#       subject = 'SJAA Event canceled "{}"  --  {}'.
#                 format(event.title, local_time(event.date_time),
#       body    = 'cancellation confirmed'
#       send_email(announce.event.owner, subject, body)
    else:
        sched_log.error('event meetup cancel failed "{}"  --  {}  --  {}'.
             format(event.title, local_time(event.date_time), ex))
    return event_id


def update_event(announce):
    # initialize channel
    init()
    event = announce.event
    if announce.channel != AnnounceChannel.Meetup.value:
        # event doesn't use Meetup channel
        sched_log.error('announcement not for meetup {} {}'.
                        format(event.title, local_time(event.date_time)))
        return
    if not announce.event_api_id:
        return
    status, ex = send_event(announce, name, description)
    if status:
        sched_log.info ('meetup event updated "{}"  --  {}  -- id:{}'.
                        format(event.title, local_time(event.date_time),
                               announce.event_api_id))
    else:
        sched_log.error('event meetup update failed "{}"  --  {}  --  {}'.
             format(event.title, local_time(event.date_time), ex))

def announce(queryset):
    init()
    sent = 0
    for announce in queryset:
        event = announce.event
        # announce event
        event_id, ex = mu_api.announce_event(announce)
        # update database
        if event_id:
            announce.date_announced  = TZ_LOCAL.localize(datetime.datetime.now())
            announce.save()
            print('meetup event announced "{}"  --  {}  -- id: {}'.
                           format(event.title, local_time(event.date_time),
                                  announce.event_api_id))
        else:
            print('event meetup announce failed "{}"  --  {}  --  {}'.
                            format(event.title, local_time(event.date_time), ex))
        # delay to prevent rate limit 
        # Meetup x-ratelimit is 30 requests / 10 sec
        time.sleep(0.3)


def cancel(queryset):
    # initialize channel
    init()
    for announce in queryset:
        cancel_event(announce)


def delete(queryset):
    # initialize channel
    init()
    # for each announcement
    for announce in queryset:
        # post Meetup event
        result, ex = mu_api.delete_event(announce.event_api_id)
        event = announce.event
        # update database
        if result:
            announce.date_posted   = None
            announce.date_canceled = None
            announce.event_api_id  = ''
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
