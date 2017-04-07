import pdb
from   email.utils          import formataddr
from   sched_core.sched_log import sched_log
from   sched_core.const     import FMT_YDATE
from   sched_core.config    import local_time, local_time_str, get_coord_email
from   sched_core.emailer   import send_email
from   .config              import channel_url_base


'''
def send_monitor_email(subject, msg, sender, recipient):
    sendmail(subject, text, sender, recipeient,
             fail_silently=False)
'''


def send_ann_confirm_email(announce):
    event       = announce.event
    date        = local_time(event.date_time).strftime(FMT_YDATE)
    date_time   = local_time_str(event.date_time)
    subject     = 'Meetup Announced - {} {}'.format(event.title, date)
    url_base    = channel_url_base[announce.channel]
    url         = url_base + '/' + announce.event_api_id
    owner       = event.owner
    group       = event.group
    coord_email = get_coord_email(group)
    if owner:
        addr_to = formataddr((owner.get_full_name(), owner.email))
        addr_cc = coord_email
    else:
        addr_to = coord_email
        addr_cc = '' # [] # None ??

    body = '''\
    The following Meetup event has been announced:
        {}
        {}
        {}'''.format(announce.event.nickname,
                     local_time_str(announce.event.date_time),
                     url)
    try:
        send_email(addr_to = addr_to,
                   addr_cc = addr_cc,
                   subject = subject,
                   message = body)
    except Exception as ex:
        sched_log.error('Bad announce confirmation email: {}'.format(ex))
