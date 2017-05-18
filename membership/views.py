#########################################################################
#
#   Astronomy Club Membership
#   file: membership/views.py
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

from   django.http                 import HttpResponseRedirect
from   django.shortcuts            import render, get_object_or_404
from   django.forms                import formset_factory
from   django.template.defaulttags import register
from   django.utils.safestring     import mark_safe
from   django.views.generic        import ListView
from   django.contrib.auth.decorators import login_required

from   sched_core.const            import FMT_YDATE
from   sched_core.config           import local_date_now, current_year, end_of_month
from   sched_core.get_events       import parse_period
from   .models                     import User
from   .config                     import MembershipStatus
from   .forms                      import VerifyForm_Orion, \
                                          VerifyForm_Membership, \
                                          ReportSearchForm, \
                                          NewForm, RenewForm
from   .process                    import new_membership, renew_membership, gen_username

class member_info():
    first_name = None
    last_name = None
    email     = None
    expires   = None


def sort_members_by_name(members):
    return sorted(members, key=lambda member: (member.last_name + ' # ' + \
                                               member.first_name).lower())

@login_required
def search(request):
    global current_year
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        form = ReportSearchForm(request.POST)
        if form.is_valid():
            start_day   = int(form.cleaned_data['start_day'  ])
            start_month = int(form.cleaned_data['start_month'])
            start_year  =     form.cleaned_data['start_year' ]
            end_day     = int(form.cleaned_data['end_day'    ])
            end_month   = int(form.cleaned_data['end_month'  ])
            end_year    =     form.cleaned_data['end_year'   ]
            report_type =     form.cleaned_data['report_type']
            period = '{}{:02}{:02}-{}{:02}{:02}'.format(
                        start_year, start_month, start_day,
                        end_year  , end_month  , end_day)
            # update 'current_year' for this session
            if start_year != current_year:
                current_year = year
            if report_type == 'summary':
                return HttpResponseRedirect('/membership/report_summary/{}'
                                            .format(period))
            if report_type == 'details':
                return HttpResponseRedirect('/membership/report_details/{}'
                                            .format(period))
            if report_type == 'active':
                return HttpResponseRedirect('/membership/report/active')
            if report_type == 'expiring':
                return HttpResponseRedirect('/membership/report/expiring')
            if report_type == 'expired':
                return HttpResponseRedirect('/membership/report/expired/{}'
                                            .format(period))
    else:
        today_str = local_date_now().strftime(FMT_YDATE)
        today = local_date_now()
        print('today is {}'.format(today_str))
        # a GET - create blank form
        form = ReportSearchForm(initial={'end_day'   : today.day  ,
                                         'end_month' : today.month,
                                         'end_year'  : today.year})
    return render(request, 'membership/report_search.html', {'form': form})


def active_list(request):
    members = User.objects.filter(status=MemStatus.active.value)
    members = sort_members_by_name(members)
    today_str = local_time.today().strtfmt(FMT_DATE)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Current Active Members'],
                   'date'      : today_str,
                   'show_email': True,
                   'sections'  : [members]})

def associate_list(request):
    members = User.objects.filter(status=MemStatus.associate.value)
    members = sort_members_by_name(members)
    today_str = local_time.today().strtfmt(FMT_DATE)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Current Associate Members'],
                   'date'      : today_str,
                   'show_email': True,
                   'sections'  : [members]})

def expiring_list(request):
    first_renewal_days = min(RENEWAL_NOTICE_DAYS)
    today = local_date_now()
    date_notice_start = today - DAY*first_renewal_days
    members = User.objects.filter(date_end__ge=date_notice_start, notices__gt=0)
    members = sort_members_by_name(members)
    today_str = today.strtfmt(FMT_DATE)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Expiring Members'],
                   'date'      : today_str,
                   'show_email': True,
                   'sections'  : [members]})

def new_list(request, period):
    start, end, period_str = parse_period(period, date=True)
    members = User.objects.filter(date_first__gte=start, date_first__lte=end)
    members = sort_members_by_name(members)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Expiring Members'],
                   'date'      : period_str,
                   'show_email': True,
                   'sections'  : zip([''], [members])})

def renewed_list(request, period):
    start, end, period_str = parse_period(period, date=True)
    members = User.objects.filter(date_start__gte=start, date_start__lte=end)
    members = sort_members_by_name(members)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Renewing Members'],
                   'date'      : period_str,
                   'show_email': True,
                   'sections'  : zip([''], [members])})

def expired_list(request, period):
    start, end, period_str = parse_period(period, date=True)
    members = User.objects.filter(date_end__gte=start, date_end__lte=end)
    members = sort_members_by_name(members)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Expiring Members'],
                   'date'      : period_str,
                   'show_email': True,
                   'sections'  : zip([''], [members])})

def report_summary(request, period):
    start, end, period_str = parse_period(period, date=True)
    new_members      = User.objects.filter(date_since__gte=start, date_since__lte=end)
    renewing_members = User.objects.filter(date_since__lte=start, date_start__gte=start, date_start__lte=end)
    expired_members  = User.objects.filter(date_end__gte=start  , date_end__lte=end)
    active_members   = User.objects.filter(date_end__gte=end)
    sections = ['New members'    , 'Renewing members',
                'Expired members', '<br>', 'Total active members']
    members  = [len(new_members    ), len(renewing_members),
                len(expired_members), '', len(active_members)]
    return render(request,
                  'membership/report_summary.html',
                  {'title'     : ['Membership Summary'],
                   'period'    : period_str,
                   'sections'  : zip(sections, members)})

def report_details(request, period):
    start, end, period_str = parse_period(period, date=True)
    print('hello')
    new_members      = User.objects.filter(date_since__gte=start, date_since__lte=end)
    renewing_members = User.objects.filter(date_since__lte=start, date_start__gte=start, date_start__lte=end)
    expired_members  = User.objects.filter(date_end__gte=start, date_end__lte=end)
    new_members      = sort_members_by_name(new_members)
    renewing_members = sort_members_by_name(renewing_members)
    expired_members  = sort_members_by_name(expired_members)
    sections = ['New members', 'Renewing members', 'Expired members']
    members  = [new_members, renewing_members, expired_members]
    return render(request,
                  'membership/report_details.html',
                  {'title'     : ['Membership Report'],
                   'period'    : period_str,
                   'sections'  : zip(sections, members)})


def verify_orion(request):
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        #   first name, first 3 letters, last name
        #   case insensitive
        form = VerifyForm_Orion(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name' ]
            # search for memberships matching name
            members = User.objects.filter(first_name__icontains=first_name,
                                          last_name__iexact    =last_name)
            # create list of strings of membership status matching name,
            #   one membership per line
            l_result = []
            for member in members:
                if first_name == member.first_name[:len(first_name)].lower() and \
                   last_name  == member.last_name.lower():
                    # check status, lowest values first
                    if member.status < MembershipStatus.expiring.value:
                        status = 'expired - '
                        date   = member.date_end.strftime(FMT_YDATE)
                    elif member.status == MembershipStatus.active.value:
                        status = 'active'
                        date   = ''
                    else:
                        continue
                    result = '{:25} : {:10}{}'.format(
                                member.get_full_name()[:25], status, date)
                    l_result.append(result)
            if members:
                no_match = ''
            else:
                no_match = first_name + ' / ' + last_name
            return render(request, 'membership/verify_orion_result.html',
                          {'members'  : l_result,
                           'no_match' : no_match})
    else:
        # a GET - create blank form
        form = VerifyForm_Orion()
    return render(request, 'membership/verify_orion.html', {'form': form})


@login_required
def verify_membership(request):
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        #   first name, first 3 letters, last name
        #   case insensitive
        form = VerifyForm_Membership(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            members = User.objects.filter(email=email)
            # create list of strings of membership status matching name,
            #   one membership per line
            if len(members) > 1:
                print('*** error: More than one member has email: {}'.format(email))
            name     = ''
            expired  = False
            expiring = False
            active   = False
            date     = ''
            no_match = ''
            if len(members) >= 1:
                member = members[0]
                name = member.get_full_name()
                if member.date_end:
                    date = member.date_end.strftime(FMT_YDATE)
                else:
                    date = ''
                # email matched
                # check status, lowest values first
                if member.status < MembershipStatus.expiring.value:
                    expired  = True
                elif member.status <= MembershipStatus.expiring.value:
                    expiring = True
                elif member.status <= MembershipStatus.active.value:
                    active   = True
                else:
                    name = ''
                    no_match = email
            else:
                no_match = email
            return render(request, 'membership/verify_membership_result.html',
                          {'name'     : name,
                           'email'    : email,
                           'expired'  : expired,
                           'expiring' : expiring,
                           'active'   : active,
                           'date'     : date,
                           'no_match' : no_match})
    else:
        # a GET - create blank form
        form = VerifyForm_Membership()
    return render(request, 'membership/verify_membership.html', {'form': form})


@login_required
def new (request):
#   pdb.set_trace()
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            user = User()
            user.username   = gen_username(form.cleaned_data['first_name'],
                                           form.cleaned_data['last_name' ])
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name' ]
            user.date_start = form.cleaned_data['date_start']
            user.date_end   = form.cleaned_data['date_end'  ]
            user.date_since = form.cleaned_data['date_since']
            user.email      = form.cleaned_data['email'     ]
            user.addr1      = form.cleaned_data['addr1'     ]
            user.addr2      = form.cleaned_data['addr2'     ]
            user.city       = form.cleaned_data['city'      ]
            user.state      = form.cleaned_data['state'     ]
            user.zip_code   = form.cleaned_data['zip_code'  ]
            user.phone1     = form.cleaned_data['phone1'    ]
            user.phone2     = form.cleaned_data['phone2'    ]
            user.notes      = form.cleaned_data['notes'     ]
            new_membership(request.user.username, user)
            return render(request, 'membership/new.html', {'form': user, 'input_form': False})
        else:
            return render(request, 'membership/new.html', {'form': form, 'input_form': True})
    else:
        today = local_date_now()
        eom_nxt_year = end_of_month(today.year+1, today.month)
        form = NewForm(initial=
                {'date_start': today.replace(day=1),
                 'date_end'  : datetime.datetime(today.year+1, today.month, eom_nxt_year),
                 'date_since': today})
        return render(request, 'membership/new.html', {'form': form, 'input_form': True})


@login_required
def renew (modeladmin, request, queryset):
    count          = len(queryset)
    RenewalFormSet = formset_factory(RenewForm, min_num=count, max_num=count)
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        # generate 1st of present month, last day of month next year
        today             = local_date_now()
        term_start        = today.replace(day=1)
        next_year         = today.year + 1
        last_day_of_month = end_of_month(next_year, today.month)
        term_end          = datetime.date(next_year, today.month, last_day_of_month)
        # sort by name
        members = sort_members_by_name(queryset)
        # generate formset
        initial = []
        for member in queryset:
            if today < member.date_end:
                term_start = member.date_end
                term_end   = member.date_end.replace(year=member.date_end.year + 1)
                term_start_future = True
            else:
                term_start_future = False
            data = {}
            data['old_start' ] = member.date_start
            data['old_end'   ] = member.date_end
            data['new_start' ] = term_start
            data['new_end'   ] = term_end
            data['future'    ] = term_start_future
            data['first_name'] = member.first_name
            data['last_name' ] = member.last_name
            data['email'     ] = member.email
            data['id'        ] = member.pk
            initial.append(data)
        formset = RenewalFormSet(initial=initial)
    return render(request, 'membership/renew.html', {'formset': formset})

def renew_update(request):
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        RenewalFormSet = formset_factory(RenewForm)
        formset = RenewalFormSet(request.POST)
        renewal_users = []
        if formset.is_valid():
            for form in formset:
                user = User.objects.get(pk=form.cleaned_data['id'])
                old_start       = form.cleaned_data['old_start']
                old_end         = form.cleaned_data['old_end'  ]
                user.date_start = form.cleaned_data['new_start']
                user.date_end   = form.cleaned_data['new_end'  ]
                renewal_users.append(user)
                renew_membership(request.user.username, user, old_start, old_end)
        return render(request, 'membership/renewal_result.html', {'users': renewal_users})


@register.filter()
def years_as_member(member):
    now_year   = local_date_now().year
    since_year = member.date_since.year
    return str(now_year - since_year)


@register.filter
def dict_lookup(value, arg):
    # 'arg' must be string
    return value[arg]

