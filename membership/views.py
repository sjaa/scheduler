import pdb

from   django.http                 import HttpResponseRedirect
from   django.shortcuts            import render, get_object_or_404
from   django.template.defaulttags import register
from   django.utils.safestring     import mark_safe
#from   django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from   django.views.generic        import ListView

from   sched_core.const            import FMT_YDATE
from   sched_core.config           import local_time_now
from   membership.models           import User
from   .forms                      import VerifyForm_Orion, VerifyForm_Membership
from   .config                     import MembershipStatus

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
    sorted(members, key=lambda member: member.user.last_name + '#' + \
                                       member.user.first_name)


def active_list(request):
    members = User.objects.filter(status=MemStatus.active.value)
    sort_members_by_name(members)
    today_str = local_time.today().strtfmt(FMT_DATE)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Current Active Members'],
                   'date'      : today_str,
                   'show_email': True,
                   'sections'  : [members]})

def associate_list(request):
    members = User.objects.filter(status=MemStatus.associate.value)
    sort_members_by_name(members)
    today_str = local_time.today().strtfmt(FMT_DATE)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Current Associate Members'],
                   'date'      : today_str,
                   'show_email': True,
                   'sections'  : [members]})

def expiring_list(request):
    first_renewal_days = min(RENEWAL_NOTICE_DAYS)
    today = local_time_now().date
    date_notice_start = today - DAY*first_renewal_days
    members = User.objects.filter(date_end__ge=date_notice_start,
                                        notices__gt=0)
    sort_members_by_name(members)
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
    sort_members_by_name(members)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Expiring Members'],
                   'date'      : period_str,
                   'show_email': True,
                   'sections'  : zip([''], [members])})

def renewed_list(request, period):
    start, end, period_str = parse_period(period, date=True)
    members = User.objects.filter(date_start__gte=start, date_start__lte=end)
    sort_members_by_name(members)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Renewing Members'],
                   'date'      : period_str,
                   'show_email': True,
                   'sections'  : zip([''], [members])})

def expired_list(request, period):
    start, end, period_str = parse_period(period, date=True)
    members = User.objects.filter(date_end__gte=start, date_end__lte=end)
    sort_members_by_name(members)
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Expiring Members'],
                   'date'      : period_str,
                   'show_email': True,
                   'sections'  : zip([''], [members])})

def report_summary(request, period):
    start, end, period_str = parse_period(period, date=True)
    new_members      = User.objects.filter(date_first__gte=start, date_first__lte=end)
    renewing_members = User.objects.filter(date_start__gte=start, date_start__lte=end)
    expired_members  = User.objects.filter(date_end__gte=start, date_end__lte=end)
    sections = ['New members', 'Renewing members', 'Expired members']
    members  = [len(new_members), len(renewing_members), len(expired_members)]
    return render(request,
                  'membership/member_summary.html',
                  {'title'     : ['Membership Summary'],
                   'date'      : period_str,
                   'show_email': False,
                   'sections'  : zip(sections, members)})

def report_details(request, period):
    start, end, period_str = parse_period(period, date=True)
    new_members      = User.objects.filter(date_first__gte=start, date_first__lte=end)
    renewing_members = User.objects.filter(date_start__gte=start, date_start__lte=end)
    expired_members  = User.objects.filter(date_end__gte=start, date_end__lte=end)
    sort_members_by_name(new_members)
    sort_members_by_name(renewing_members)
    sort_members_by_name(expired_members)
    sections = ['New members', 'Renewing members', 'expired members']
    members  = [new_members, renewing_members, expired_members]
    return render(request,
                  'membership/member_list.html',
                  {'title'     : ['Membership Report'],
                   'date'      : period_str,
                   'show_email': False,
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


    print('hi ho', local_time_now())
#   my_form = form()  # get email
#   members = Membership.objects.filter(email=email)
#   l_result = []
#   for member in members:
#       if first_name == member.firstname[:len(first_name)] and \
#          last_name  == member.last_name:
#           l_result.append(member.get_full_name())


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
                    expired = True
                elif member.status <= MembershipStatus.expiring.value:
                    expiring = True
                elif member.status <= MembershipStatus.active.value:
                    active = True
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


@register.filter()
def calc_years(member_since):
    now_year   = local_time().year
    since_year = member_since.year
    return str(now_year - since_year)


