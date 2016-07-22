import pdb
import datetime

from sched_core.const   import TZ_UTC, DAY, SUN
from sched_core.config  import TZ_LOCAL, sites
from sched_ev           import cal_ephemeris
from sched_ev.holidays  import gen_holidays
from .const             import RuleStartTime, EventRepeat
from .models            import EventType, Event
#from   sched_ev.cal_ephemeris import moon_phase

'''
All date/time are time zone unaware.  Local time is assumed.  The exception
is date/time is made time zone aware just before model instance is saved.
'''

moon_phase = []


def gen_events(start, end, event_types):
    global moon_phase

    year = start.year
    # generate all ephemeris data for year
    moon_phase = cal_ephemeris.cal_ephemeris(year)
    gen_holidays(year)
    # get all event templates currently in use
    for event_type in event_types:
        if event_type.repeat == EventRepeat.lunar.value:
            add_events_lunar(start, end, event_type)
        elif event_type.repeat == EventRepeat.monthly.value:
            add_events_monthly(start, end, event_type)
        elif event_type.repeat == EventRepeat.annual.value:
            add_events_annual(start, end, event_type)
        elif event_type.repeat == EventRepeat.onetime.value:
            add_events_onetime(event_type)


#def foo(event_title=''):
def foo(event_types):
    '''
    '''
    year = 2017
    start = datetime.datetime(year  , 1, 1)
    end   = datetime.datetime(year+1, 1, 1)
    gen_events(start, end, event_types)


def add_event(event_type, date_time):
    '''
    input
        event_type  .models.EventType
        date_time   datetime.date_time, time zone unaware

    output
        add 'Event' class object to database
    '''

    # make 'date_time' time zone aware for database save
    date_time = TZ_LOCAL.localize(date_time)
    ev = Event(event_type    = event_type,
               nickname      = event_type.nickname,
               title         = event_type.title,
               category      = event_type.category,
               date_time     = date_time,
               time_length   = event_type.time_length,
               time_setup    = event_type.time_setup,
               time_teardown = event_type.time_teardown,
               location      = event_type.location,
               verified      = event_type.verified,
               group         = event_type.group,
               url           = event_type.url,
               notes         = event_type.notes)
    ev.save()


def add_events_monthly(start, end, event_type):
    '''
    Generate list of datetime for monthly events on nth weekday given week
    and day of the week of each month.
    E.g., to calculate 2nd Tuesday of March, 1999:
        calc_monthly_dates(<start datetime>, <end datetime>, RuleWeek.week_2,
                           RuleWeekday.tuesday.value())
        (Note: the date must be between start and end datetimes

    Look for all dates in complete months.  Then throw away dates not
    between start and end, inclusive.

    Be sure time for 'start' and 'end' are '0:00'.
    'week': Zero means 1st week.

    input
        start       datetime.date_time   starting date of period to generate events
        end         datetime.date_time   ending   date of period to generate events
        event_type  EventType

    output
        add monthly repeat events to Event

    test:
        use above 'def a'
        input:
            start = datetime.datetime(2016, 2, 1)
            end   = datetime.datetime(2016, 9, 30)
            a(start, end, RuleWeek.week_5, RuleWeekday.tuesday) # 5th Tuesday
        output:
            2016-03-29 00:00:00
            2016-05-31 00:00:00
            2016-08-30 00:00:00
    '''

    date_time = start
    dates = []
    # set date to 1st of month
    date_time = date_time.replace(day=1)
    while date_time < end:
        weekday = event_type.weekday
        try:
            week    = event_type.week
        except:
            pdb.set_trace()
        # datetime.weekday - Monday=0, Sunday=6
        first_weekday_of_month = date_time.weekday()
        # calculate day of month
        if first_weekday_of_month > weekday:
            days = weekday - first_weekday_of_month + 7 + week*7
        else:
            days = weekday - first_weekday_of_month     + week*7
        # append date
        prev_month = date_time.month
        date_time = date_time + DAY*days
        new_month = date_time.month
        # reject date if additional days pushes date into next month
        if prev_month==new_month:
            # reject date before start and after end
            if start <= date_time < end:
                date_time = calc_start_time(date_time, event_type)
                add_event(event_type, date_time)
            # get month/year for following month
            next_month = date_time.month + 1
            next_year  = date_time.year
            if next_month > 12:
                next_month = 1
                next_year += 1
            date_time = date_time.replace(year=next_year, month=next_month, day=1)
        else:
            date_time = date_time.replace(day=1)


def add_events_lunar(start, end, event_type):
    '''
    Generate list of dates on a given weekday nearest the specified lunar
    phase in the period defined by (datetime) 'start' and 'end', inclusive.
    E.g.: 3Q Fridays @ nautical twilight

    input
        start       datetime.date_time   starting date of period to generate events
        end         datetime.date_time   ending   date of period to generate events
        event_type  EventType            default event template for type of event

    output
        add lunar repeat events to Event
    '''
    # set 'day' to 'weekday' at or after 'start'
    date_time = start
    dates = []
    weekday_of_date = date_time.weekday()
    event_weekday = event_type.weekday
    if weekday_of_date > event_weekday:
        days = event_weekday - weekday_of_date + 7
    else:
        days = event_weekday - weekday_of_date
    date_time = date_time + DAY*days
    while date_time < end:
        dayofyear = int(date_time.strftime("%j"))
        if moon_phase[dayofyear].value == event_type.lunar_phase:
            date_time = calc_start_time(date_time, event_type)
            if start < date_time:
                add_event(event_type, date_time)
        date_time = date_time + DAY*7


def add_events_annual(start, end, event_type):
    '''
    Generate one event on month specified by 'event_type'

    input
        start       datetime.date   starting date of period to generate events
        end         datetime.date   ending   date of period to generate events
        event_type  EventType       default event template for type of event

    output
        add annual event to Event
    '''
    # set 'date' to 'weekday' at or after 'start'
    date_time = start.replace(month=event_type.month, day=1)
    dates = []
    weekday_of_date = date_time.weekday()
    event_weekday = event_type.weekday
    if weekday_of_date > event_weekday:
        days = event_weekday - weekday_of_date + 7
    else:
        days = event_weekday - weekday_of_date
    date_time = date_time + DAY*days
    while date_time < end:
        dayofyear = int(date_time.strftime("%j"))
        if moon_phase[dayofyear].value == event_type.lunar_phase:
            date_time = calc_start_time(date_time, event_type)
            if start < date_time:
                add_event(event_type, date_time)
                # added event, no need to consider other dates
                break
        date_time = date_time + DAY*7


def add_events_onetime(event_type):
    '''
    Generate one-time event.  Set date_time back to Jan 1, midnight of current year
    Code to accept event will not unset 'draft' if date_time is not changed
    since date_time must be later than the current date/time.

    input
        event_type  EventType       default event template for type of event

    output
        add one-time event to Event
    '''
    # set date_time back to Jan. 1, midnight of current year
    year = datetime.datetime.now().year
    date_time = datetime.datetime(year, 1, 1, 0, 0)
    add_event(event_type, date_time)


def calc_start_time(date_time, event_type):
    '''
    Calculate start time of event based on twilight time for 'date_time'.

    input
        date_time   datetime.date_time   date/time of event
        event_type  EventType            default event template for type of event

    output
        return      datetime        calculated start time
    '''

    # start time rule is absolute time
    if event_type.rule_start_time == RuleStartTime.absolute.value:
        date_time = datetime.datetime.combine(date_time, event_type.time_start)
        return date_time

    # start time rule is relative to twilight
    date = datetime.datetime.combine(date_time, datetime.time(12, 0))
    date = TZ_UTC.localize(date)
    site      = sites[event_type.location]
    site.date = date
    
    try:
        site.horizon = rule_horizon[event_type.rule_start_time]
    except:
        pdb.set_trace()
    dusk = TZ_LOCAL.localize(ephem.localtime(site.next_setting(SUN)))
    old_h = dusk.hour
    old_m = dusk.minute
    new_h = old_h
    new_m = old_m
    # round minutes to nearest quarter hour
    if old_m <  5:
        new_m = 0
    elif old_m < 20:
        new_m = 15
    elif old_m < 35:
        new_m = 30
    elif old_m < 50:
        new_m = 45
    else:
        new_h += 1
        new_m  = 0
    time = datetime.time(new_h, new_m)
    date_time = datetime.datetime.combine(date_time, time)
    if event_type.time_start_offset:
        if event_type.neg_start_offset:
            date_time -= event_type.time_start_offset
        else:
            date_time += event_type.time_start_offset
    # don't start before "earliest" (e.g., 7pm)
    if event_type.time_earliest and date_time.time() < event_type.time_earliest:
        # 'combine' doesn't keep timezone info
        date_time = datetime.datetime.combine(date_time, event_type.time_earliest)
    # TODO: Hack to get ITSP to be scheduled after class
    if event_type.time_start_offset and not event_type.neg_start_offset:
        date_time += event_type.time_start_offset
    return date_time


if __name__ == '__main__':
    foo()
