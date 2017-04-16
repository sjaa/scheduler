import pdb
from   email.utils          import formataddr
from   sched_core.sched_log import sched_log
from   sched_core.const     import FMT_YDATE
from   sched_core.config    import local_time, local_time_str, get_coord_email
from   sched_core.emailer   import init_email, send_email
from   .config              import channel_url_base


meetup_body = '''\
The following Meetup event has been announced:
    {}
    {}'''

def get_owner_coord_emails(foo):
    owner       = foo.owner
    group       = foo.group
    coord_email = get_coord_email(group)
    if owner:
        addr_to = formataddr((owner.get_full_name(), owner.email))
        addr_cc = coord_email
    else:
        addr_to = coord_email
        addr_cc = None
    return addr_to, addr_cc


def send_email_ann_confirm(queryset):
    init_email()
    for announce in queryset:
        event     = announce.event
        date      = local_time(event.date_time).strftime(FMT_YDATE)
        date_time = local_time_str(event.date_time)
        subject   = 'SJAA Meetup Announced - {} {}'.format(event.title, date)
        url_base  = channel_url_base[announce.channel]
        url       = url_base + '/' + announce.event_api_id
        addr_to,
        addr_cc   = get_owner_coord_emails(event)

        # show name of event, date/time, Meetup event URL
        meetup_body.format(event.nickname,
                           local_time_str(event.date_time),
                           url)
        try:
            send_email(to = addr_to,
                       cc = addr_cc,
                       subject = subject,
                       message = body)
        except Exception as ex:
            sched_log.error('Bad announce confirmation email: {}'.format(ex))


def send_email_task_reminder(queryset):
    init_email()
    for task in queryset:
        event     = task.event
        date      = local_time(event.date_time).strftime(FMT_YDATE)
        date_time = local_time_str(event.date_time)
        subject   = 'SJAA task - {} {} / "{}"'.format(event.title, task.date.strftime(FMT_YDATE), task.name)
        # TODO:
        # send URL of task
        # if task needs to be completed, send URL to indicate completion
        #   task webpage shown only to owner
        
        url_base  = channel_url_base[announce.channel]
        url       = url_base + '/' + announce.event_api_id
        addr_to,
        addr_cc   = get_owner_coord_emails(event)

        # show name of event, date/time, Meetup event URL
        body.format(event.nickname,
                    local_time_str(event.date_time),
                    url)
        try:
            send_email(to = addr_to,
                       cc = addr_cc,
                       subject = subject,
                       message = body)
        except Exception as ex:
            sched_log.error('Bad announce confirmation email: {}'.format(ex))
        addr_cc   = get_owner_coord_emails(event)
