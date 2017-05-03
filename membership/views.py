import pdb
import datetime

from   django.http                 import HttpResponseRedirect
from   django.shortcuts            import render, get_object_or_404
from   django.forms                import formset_factory
from   django.template.defaulttags import register
from   django.utils.safestring     import mark_safe
#from   django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from   django.views.generic        import ListView

from   sched_core.const            import FMT_YDATE
from   sched_core.config           import local_date_now, current_year, end_of_month
from   sched_core.get_events       import parse_period
from   .models                     import User
from   .config                     import MembershipStatus
from   .forms                      import VerifyForm_Orion, \
                                          VerifyForm_Membership, \
                                          ReportSearchForm, RenewForm
'''
urlpatterns = [
    # membership views
    # list all
    # list active
    # list associate
    # list expired
    # list expiring
    url(r'^active$'   , views.active_list,
                        name='membership_active'),
    url(r'^associate$', views.associate_list,
                        name='membership_associate'),
    url(r'^expired=(?P<period>\d{8}-\d{8})',
                        views.expired_list,
                        name='membership_expired')
    url(r'^expiring$' , views.expiring_list,
                        name='membership_expiring'),
    url(r'^renewed=(?P<period>\d{8}-\d{8})',
                        views.renewed_list,
                        name='membership_renewed')
'''

class member_info():
    first_name = None
    last_name = None
    email     = None
    expires   = None


def sort_members_by_name(members):
    return sorted(members, key=lambda member: (member.last_name + ' # ' + \
                                               member.first_name).lower())

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
    sections = ['New members'         , 'Renewing members',
                'Total active members', 'Expired members']
    members  = [len(new_members   ), len(renewing_members),
                len(active_members), len(expired_members)]
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
                date   = member.date_end.strftime(FMT_YDATE)
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

'''
    renewals = len(memberships)
    RenewalFormSet = formset_factory(RenewSingleForm, min_num=renewals, max_num=renewals)
    formset = RenewalFormSet(initial=[
                {'title' : 'Membership Renewal',
                 'date'  : local_date_now()})
'''

def renew (modeladmin, request, queryset):
    count          = len(queryset)
    RenewalFormSet = formset_factory(RenewForm, min_num=count, max_num=count)
    if request.method == 'POST':
        # create a form instance and populate with data from request:
#       formset = RenewalFormSet(request.POST)
#       pdb.set_trace()
#   else:
        # generate 1st of present month, last day of month next year
        today             = local_date_now()
        term_start        = today.replace(day=1)
        next_year         = today.year + 1
        last_day_of_month = end_of_month(next_year, today.month)
        term_end          = datetime.date(next_year, today.month, last_day_of_month)
        # sort by name
        members = sort_members_by_name(queryset)
#       pdb.set_trace()
        # generate formset
        initial = []
#       i = 0
        for member in queryset:
            data = {}
            data['term_start'] = term_start
            data['term_end'  ] = term_end
            data['first_name'] = member.first_name
            data['last_name' ] = member.last_name
            data['email'     ] = member.email
            data['id'        ] = member.pk
            initial.append(data)
#           i += 1
#       pdb.set_trace()
        formset = RenewalFormSet(initial=initial)
    return render(request, 'membership/renew.html', {'formset': formset})




@register.filter()
def years_as_member(member):
    now_year   = local_date_now().year
    since_year = member.date_since.year
    return str(now_year - since_year)


@register.filter
def dict_lookup(value, arg):
    # 'arg' must be string
    return value[arg]

def renew_update(request):
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        RenewalFormSet = formset_factory(RenewForm)
        formset = RenewalFormSet(request.POST)
        renewal_users = []
#       pdb.set_trace()
        if formset.is_valid():
            for form in formset:
                user = User.objects.get(pk=form.cleaned_data['id'])
                user.date_start = form.cleaned_data['term_start']
                user.date_end   = form.cleaned_data['term_end'  ]
                renewal_users.append(user)
#               user.save()
                '''
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
                '''
            for user in renewal_users:
                print(user.get_full_name())
        return render(request, 'membership/renewal_result.html', {'users': renewal_users})
