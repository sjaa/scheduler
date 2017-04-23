import datetime

from django.db.models  import Q

from sched_ev.models   import Event, L_MONTH
from .config           import TZ_LOCAL, site_names, end_of_month


def get_events(period, location, event_type):
    # get starting date
    start_year  = int(period[ 0: 4])
    start_month = int(period[ 4: 6])
    start = TZ_LOCAL.localize(datetime.datetime(start_year, start_month, 1))
    # get ending date, just before midnight
    end_year    = int(period[ 7:11])
    end_month   = int(period[11:13])
    # get last day in month - monthrange returns (first day, last day)
    end   = TZ_LOCAL.localize(end_of_month(end_year, end_month))
    # detect bad period if start is after end
    bad_period = True if start > end else False
    # get events
    q = Q(date_time__gte=start) & Q(date_time__lte=end) & Q(planned=True)
    if location != '0':
        location = int(location)
        q &= Q(location=location)
    if event_type != '0':
        event_type = int(event_type)
        q &= Q(event_type=int(event_type))
    events = Event.objects.filter(q).order_by('date_time')
    if start < end:
        period = '{} {} - {} {}'.format(L_MONTH[start_month-1][1], start_year,
                                        L_MONTH[end_month  -1][1], end_year)
    else:
        period = 'bad period'
    return (events, period)

