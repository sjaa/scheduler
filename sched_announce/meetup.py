#from models                   import AnnounceType, Announce
#from core.common              import DAY
import pdb
import datetime
from   sched_core.const        import local_time
from   sched_core.config       import TZ_LOCAL, coordinator
from   sched_core.sched_log    import sched_log
from   pythonkc_meetups.client import PythonKCMeetups
from   sched_announce.secrets  import MEETUP_API_KEY
from   sched_announce.const    import AnnounceChannel

mu_api = None


def init():
    global mu_api

    if not mu_api:
        mu_api = PythonKCMeetups(MEETUP_API_KEY,
                                 http_timeout=600, http_retries=4)


def post(queryset):
    # initialize channel
    init()
    sent = 0
    count = len(queryset)
    for announce in queryset:
        if announce.channel != AnnounceChannel.Meetup.value:
            # event doesn't use Meetup channel
            sched_log.error('announcement not for meetup {} {}'.
                            format(event.title, local_time(event.date_time)))
            count -= 1
            continue
        if announce.event_api_id:
            count -= 1
            continue
        event_id = mu_api.create_event(announce)
        if event_id:
            announce.event_api_id = event_id
            announce.date_posted = TZ_LOCAL.localize(datetime.datetime.now())
            announce.save()
            sent += 1
    if sent == count:
        sched_log.info('All Meetup events posted: {}'.format(len(queryset)))
    else:
        count = len(queryset)
        sched_log.error('Some Meetup events not sent: only {} out of {} posted'.
                         format(count - sent, count))


def edit(announce):
    # initialize channel
    init()
    if announce.channel != AnnounceChannel.Meetup.value:
        # event doesn't use Meetup channel
        sched_log.error('announcement not for meetup {} {}'.
                        format(event.title, local_time(event.date_time)))
        return
    if not announce.event_api_id:
        return
    status = mu_api.edit_event(announce)
    event  = announce.event
    if status:
        sched_log.info ('meetup event edited "{}"  --  {}  -- id:{}'.
                        format(event.title, local_time(event.date_time),
                               announce.event_api_id))
    else:
        sched_log.error('meetup event was NOT edited "{}"  --  {}  -- id:{}'.
                        format(event.title, local_time(event.date_time),
                               announce.event_api_id))

def announce(queryset):
    init()
    sent = 0
    for announce in queryset:
        status = mu_api.announce_event(announce)
        if status:
            sent += 1


def cancel(announce):
    init()
    # initialize channel
    if not announce.event_api_id:
        return
    status = mu_api.cancel_event(announce)
    event = announce.event
    pdb.set_trace()
    if status:
        announce.date_canceled = TZ_LOCAL.localize(datetime.datetime.now())
        announce.save()
        sched_log.info('meetup event canceled "{}"  --  {}  -- id:{}'.
                       format(event.title, local_time(event.date_time),
                              announce.event_api_id))
    else:
        sched_log.error('meetup event was NOT canceled "{}"  --  {}  -- id:{}'.
                       format(event.title, local_time(event.date_time),
                              announce.event_api_id))


