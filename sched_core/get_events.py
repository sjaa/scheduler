import pdb
import datetime

from django.db.models  import Q

from sched_ev.models   import Event, L_MONTH
from .config           import TZ_LOCAL, site_names, end_of_month

def parse_period(period, month=False, date=False):
    # get starting date
    start_year  = int(period[ 0: 4])
    start_month = int(period[ 4: 6])
    if date:
        start_date = int(period[ 6: 8])
        period = period[9:]
    elif month:
        start_date = 1
        period = period[7:]
    start = TZ_LOCAL.localize(datetime.datetime(start_year, start_month, start_date))

    # get ending date, just before midnight
    end_year  = int(period[ 0: 4])
    end_month = int(period[ 4: 6])
    if date:
        end_date = int(period[ 6: 8])
    elif month:
        end_date = end_of_month(end_year, end_month)
    end = TZ_LOCAL.localize(datetime.datetime(end_year, end_month, end_date))
    if date:
        period_str = '{} {}, {}&nbsp -&nbsp {} {}, {}'.format(
                        L_MONTH[start_month-1][1], start_date, start_year,
                        L_MONTH[end_month  -1][1], end_date  , end_year)
    elif month:
        period_str = '{} {}&nbsp -&nbsp {} {}'.format(
                        L_MONTH[start_month-1][1], start_year,
                        L_MONTH[end_month  -1][1], end_year)
    return (start, end, period_str)


def get_events(period, location, event_type):
    start, end, period_str = parse_period(period, month=True)
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
    if start >= end:
        period = 'bad period'
    return (events, period_str)

