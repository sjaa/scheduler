import pdb
import datetime

from ev_sched.cal_const     import *
from .models                import EventType, Event
import ev_sched.cal_ephemeris
#from   ev_sched.cal_ephemeris import moon_phase

'''
All date/time are time zone unaware.  Local time is assumed.  The exception
is date/time is made time zone aware just before model instance is saved.
'''

moon_phase = []

def chk_event_type_valid(et):
    '''
    Note: et.week can be zero, so a test for a null field must be explicit:
        et.week!=None
    '''
#   print(0, et.title)
    err_msg = []
#   pdb.set_trace()

    # by repeat
    if (et.repeat in (EventRepeat.onetime.value, EventRepeat.annual.value)) and \
       not (et.date or et.month and (et.week!=None or et.lunar_phase) and et.weekday):
        err_msg += ['For Repeat "one-time" or "annual", ' +
                    'required: "Date" or "Month", "Week", and "Weekday"']
    if et.repeat == EventRepeat.monthly.value and \
       not (et.week!=None and et.weekday):
        err_msg += ['For Repeat "month", required: "Week", "Weekday"']
    if et.repeat == EventRepeat.lunar.value and \
       not et.weekday:
        err_msg += ['for Repeat "lunar", required: "Weekday"']
    # by week
    if et.week!=None and not et.weekday:
        err_msg += ['for "Week", required: "Weekday"']
    # by start time
    if not (et.rule_start_time or et.start_time):
        err_msg += ['Need "Start time rule" or "Start time"']
    if et.rule_start_time == RuleStartTime.absolute.value and \
       not et.time_start:
        err_msg += ['for "Start time rule" = "absolute", required: "Start time"']
    if (et.time_start_offset or et.time_earliest) and \
       et.rule_start_time == RuleStartTime.absolute.value:
        err_msg += ['for "Start time offset or "Earliest start time", ' +
                    'required: "Rule start time" must not be "absolute"']
    if not ((et.time_start or et.rule_start_time) and et.time_length):
        err_msg += ['Required: "Start time rule", "Time length"']
#   print(1, et.title)
    return err_msg


def gen_events(start, end, event_types):
    global moon_phase

    year = start.year
    # generate all ephemeris data for year
    cal  = ev_sched.cal_ephemeris.cal_ephemeris(year)
    moon_phase = ev_sched.cal_ephemeris.moon_phase
#   '''
    for event_type in event_types:
        err_msg = chk_event_type_valid(event_type)
        if err_msg:
            print(event_type.title + " is invalid")
            print(err_msg)
    # get all event templates currently in use
    for event_type in event_types:
        if event_type.repeat == EventRepeat.lunar.value:
            add_events_lunar(start, end, event_type)
        elif event_type.repeat == EventRepeat.monthly.value:
            add_events_monthly(start, end, event_type)
        elif event_type.repeat == EventRepeat.annual.value:
            add_events_annual(start, end, event_type)

#   '''


#def foo(event_title=''):
def foo(event_types):
    '''
    '''
    year = 2016
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

    # make time zone aware for database save
    date_time = TZ_LOCAL.localize(date_time)
    ev = Event(event_type  = event_type,
               title       = event_type.title,
               category    = event_type.category,
               date_time   = date_time,
               time_length = event_type.time_length,
               location    = event_type.location,
               verified    = event_type.verified,
               group       = event_type.group,
               url         = event_type.url,
               notes       = event_type.notes)
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
        return list of datetime.datetime of scheduled events

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
        return      list            tuples of datetime.datetime
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
    Generate list of dates on a given weekday nearest the specified lunar
    phase in the period defined by (datetime) 'start' and 'end', inclusive.
    E.g.: February full moon Saturday

    input
        start       datetime.date   starting date of period to generate events
        end         datetime.date   ending   date of period to generate events
        event_type  EventType       default event template for type of event

    output
        return      list            tuples of datetime.date
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
                break
        date_time = date_time + DAY*7


def calc_start_time(date_time, event_type):
    '''
    Calculate start time of event based on twilight time for 'date_time'.

    input
        date_time   datetime.date_time   date/time of event
        event_type  EventType            default event template for type of event

    output
        return      datetime        calculated start time

    local: in cal_const.py
    '''

    # start time rule is absolute time
    if event_type.rule_start_time == RuleStartTime.absolute.value:
        date_time = datetime.datetime.combine(date_time, event_type.time_start)
        return date_time

    # start time rule is relative to twilight
    d = datetime.datetime.combine(date_time, datetime.time(12, tzinfo=TZ_LOCAL))
    d = TZ_LOCAL.localize(d)
    local.date = d
    
    try:
        local.horizon = rule_horizon[event_type.rule_start_time]
    except:
        pdb.set_trace()
    dusk = TZ_LOCAL.localize(ephem.localtime(local.next_setting(SUN)))
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
#   import ev_sched.gen_events
    foo()
