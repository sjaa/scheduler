#########################################################################
#
#   Astronomy Club Event Scheduler
#   file: membership/process.py
#
#   Copyright (C) 2017  Teruo Utsumi, San Jose Astronomical Association
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Contributors:
#       2017-06-01  Teruo Utsumi, initial code
#
#########################################################################

import pdb
import datetime
from   django.contrib       import admin
from   sched_core.const     import FMT_YDATE, FMT_DATE_Y, DAY
from   sched_core.config    import local_date_now
from   sched_core.sched_log import sched_log
from   sched_core.filters   import AdminDateTimeYearFilter
from   .config              import MembershipStatus, \
                                   EMAIL_TEST_HEADER, \
                                   RENEWAL_NOTICE_DAYS, MEMBERSHIP_EMAIL_ADDR, \
                                   EXPIRED_NOTICE_SUBJECT, RENEWAL_NOTICE_SUBJECT, \
                                   RENEWAL_NOTICE_TEXT, EXPIRED_NOTICE_TEXT, \
                                   MembershipStatus
from   .models              import User
from   .emailer             import send_email
from   .membership_log      import membership_log


def new_membership(username, member):
    member.status = MembershipStatus.active.value
    member.notice = 0  # reset # of renewal notices
    member.save()
#   send_email_new(user)
    membership_log.info('{} - New member: {} {} - {} / {} to {} / since: {}'.format(
                        username[:15],
                        member.first_name, member.last_name, member.email,
                        member.date_start.strftime(FMT_YDATE),
                        member.date_end  .strftime(FMT_YDATE),
                        member.date_since.strftime(FMT_YDATE)))


def renew_membership(username, member, old_start, old_end):
    member.status = MembershipStatus.active.value
    member.notice = 0  # reset # of renewal notices
    member.save()
#   send_email_renew(user)
    membership_log.info('{} - Renewal: {} {} - {} / old: {} to {} / new : {} to {}'.format(
                        username[:15],
                        member.first_name, member.last_name, member.email,
                        old_start        .strftime(FMT_YDATE),
                        old_end          .strftime(FMT_YDATE),
                        member.date_start.strftime(FMT_YDATE),
                        member.date_end  .strftime(FMT_YDATE)))


def gen_username(first_name, last_name):
    '''
    make user name
     - lower case
     - replace space with '_'
     - allowable characters:
       - lower case letters
       - digits
       - '@.+=_'
    '''
    name = (first_name + '.' + last_name).lower().replace(' ', '_')
    allowable = '@.+=_'
    new_name = ''
    for c in name:
        if c.isalnum() or c in allowable:
            new_name += c
    count = 1
    tmp_name = new_name[:]
    while User.objects.filter(username=tmp_name):
        tmp_name = new_name + '_' + str(count)
        count += 1
    return tmp_name


def cron_job(username, test_modes):
    did_something = False

    for notice in range(len(RENEWAL_NOTICE_DAYS)):
        notice_date = local_date_now() - DAY*RENEWAL_NOTICE_DAYS[notice]
        # TODO for 1.9/1.10 -- ~Q(status=ASSOCIATE)
        members = User.objects.filter(date_end__lte=notice_date, notices=notice)
        for member in members:
            did_something = True
            if notice == 0:
                member.status == MembershipStatus.expiring.value
            elif notice == RENEWAL_NOTICE_DAYS[-1]:
                # Change status to expired at last notice
                member.status == MembershipStatus.expired.value
            member.notices += 1
            try:
                send_renewal_notice(member, notice+1, test_modes)
                # email sent, update membership status
                member.save()
                membership_log.info('{:15} - Renewal notice #{} sent to {}'.
                               format(username, notice+1, member.email))
            except Exception as error:
                membership_log.error('{:15} - Renewal notice #{} sent to {}'.
                               format(username, notice+1, member.email))
    if not did_something:
        membership_log.info('{:15} - no renewal activity'.format(username))
    return did_something


def send_renewal_notice(member, notice, test_modes):
    expired = local_date_now() > member.date_end

    # format email message
    days       = (member.date_end - local_date_now()).days
    date_str   = member.date_end.strftime('%b %d')  # Sep 05
    addr_to    = '{} <{}>'.format(member.get_full_name(), member.email)
    addr_from  = MEMBERSHIP_EMAIL_ADDR
    if expired:
        subject = EXPIRED_NOTICE_SUBJECT.format(notice)
        body    = EXPIRED_NOTICE_TEXT
    else:
        subject = RENEWAL_NOTICE_SUBJECT.format(date_str, notice)
        body    = RENEWAL_NOTICE_TEXT
    if test_modes:
        body = EMAIL_TEST_HEADER + body
    subst_dict = { 'name'      : member.get_full_name(),
                   'days'      : days,
                   'date'      : date_str,
                   'addr_to'   : addr_to,    ## TODO: remove later
                   'addr_from' : addr_from,
                   'subject'   : subject,
                   'today'     : local_date_now().strftime(FMT_DATE_Y)
    }
    body = body.format(**subst_dict)
    send_email(addr_to=addr_to,
               addr_from=addr_from,
               subject=subject,
               body=body,
               test_modes=test_modes)
    
