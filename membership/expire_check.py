
from sched_core import FMT_DATE, DAY
from .models    import Membership
from .config    import RENEWAL_NOTICE_DAYS, MEMBERSHIP_CHAIR_EMAIL_ADDR, \
                       RENEWAL_NOTICE_TEXT, EXPIRED_NOTICE_TEXT, \
                       MemStatus
from .emailer   import send_email
#   for notice_days in RENEWAL_NOTICE_DAYS:

def expire_check():
    for notice in range(len(RENEWAL_NOTICE_DAYS)):
        notice_date = local_time_now().date - DAY*RENEWAL_NOTICE_DAYS[notice]
        # TODO for 1.9/1.10 -- ~Q(status=ASSOCIATE)
        members = Membership.objects.filter(date_end__lte=notice_date, notices=notice).exclude(status=ASSOCIATE)
        send_renewal_notice(members)
    # ensure notices = 0 for non-expiring members
    correct_notices()


def send_renewal_notice(members):
    addr_from = MEMBERSHIP_CHAIR_EMAIL_ADDR 
    # all members in 'members' has 
    expired = True if now > members[0].date_end else False
    for member in members:
        # format email message
        user = member.user
        notice_date     = (member.date_end - local_time_now().date).days
        notice_date_str = format(member.date_end.strtfmt(FMT_DATE))
        addr_to = '{} <{}>'.format(user.email, user.get_full_name())
        if expired:
            subject = 'Your SJAA membership expires on {}'.format(notice_date)
        else:
            subject = 'Your SJAA membership expired'
        subst_dict = { 'first_name' : user.first_name,
                       'days'       : days,
                       'date'       : date,
                       'addr_to'    : addr_to,    ## TODO: remove later
                       'addr_from'  : addr_from,  ## TODO: remove later
                       'subject'    : subject     ## TODO: remove later
        }
        if expired:
            text = RENEWAL_NOTICE_TEXT.format(**subst_dict)
            # TODO: Add code to turn off member privileges
        else:
            text = EXPIRED_NOTICE_TEXT.format(**subst_dict)
        # attempt email transmission
        try:
            send_email(msg)
        except:
            # something went wrong
            print('bad email transmission')
        else:
            if expired:
                member.status = MemStatus.expired.value
                # TODO: Add code to turn off member privileges
            else:
                member.status = MemStatus.expiring.value
            member.notices += 1
            member.save()


def correct_notices():
    # find members whose membership is current
    # if 'notices' > 0, then set to zero
    first_renewal_days = min(RENEWAL_NOTICE_DAYS)
    today = local_time_now().date
    date_notice_start = today - DAY*first_renewal_days
    members = Membership.objects.filter(date_end__ge=date_notice_start,
                                        notices__gt=0)
    for member in members:
        member.notice = 0
        member.save()
