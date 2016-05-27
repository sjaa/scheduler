import os
import datetime
import urllib.request
from   icalendar import Calendar
import pdb
from   .models   import AuxEvent
from sched_ev.cal_const  import AuxCategory

#from cal_const import URL_HOLIDAYS

# US holidays from Google Calendar
# Note: Google US holiday have holidays for past, current, and subsequent years.
#       Any other period requires another source.
URL_HOLIDAYS = "https://calendar.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics"

#FILE_HOLIDAYS = join(os.base_dir, 'data', 'holidays.ics')
FILE_HOLIDAYS = 'holidays_{year}.ics'
#FILE_HOLIDAYS = 'holidays.ics'


'''
class AuxEvent:
    def __init__(self, name, date, category):
        self.name     = name
        self.date     = date
        self.category = category

    def __str__():
        return self.name
'''


# TODO: put try/except bad connection around caller of 'get_holidays'
def gen_holidays(year):
    #pdb.set_trace()

    # Get iCalendar data from Google
    # Gets holidays from prior year through following year
    filename = FILE_HOLIDAYS.format(year=year)
    a = os.path.dirname(__file__)
    print("file path:", a)
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            print('reading out ical')
            gcal = Calendar.from_ical(f.read())
    else:
        response = urllib.request.urlopen(URL_HOLIDAYS)
        rsp = response.read()
        gcal = Calendar.from_ical(rsp)
        with open(filename, 'wb') as f:
            print('writing out ical')
            f.write(Calendar.to_ical(gcal))

    # Extract name and date from iCalendar data
    l_s_event = []
    for ev in gcal.walk():
        if ev.name == 'VEVENT':
            name = str(ev.get('summary'))
            # ignore specific VEVENTs
            # TODO: change below check
            #       - move strings into list
            #       - check in comprehension
            if name != "Thomas Jefferson's Birthday" and not "observed" in name :
                date = ev.get('dtstart').dt
                # add VEVENT if it occurs between 'start' and 'end'
#               if start <= date <= end:
                if date.year == year:
                    # TODO: change below replace
                    #       - make list of match/replace string pairs
                    name = name.replace('Daylight Saving Time', 'DST')
                    queryset = AuxEvent.objects.filter(date=date, category=AuxCategory.holiday.value)
                    if not queryset or name not in [t.title for t in queryset]:
#                       s = AuxEvent(name, date, AuxCategory.holiday)
                        s = AuxEvent()
                        s.title    = name
                        s.date     = date
                        s.category = AuxCategory.holiday.value
                        s.notes    = ''
                        s.save()
#                       print('hi')
#                       l_s_event.append(s)
#                   s = AuxEvent(name, date, 'HO')
#                   l_s_event.append(s)
#   return l_s_event
    return

if __name__ == '__main__':
    start = datetime.date(2016,  1,  1)
    end   = datetime.date(2016, 12, 30)
#   pdb.set_trace()
    l_s_event = get_holidays(start, end)
    # sort VEVENTs by date
    l_s_event.sort(key = lambda e: e.date)

    # print VEVENTs by name and date
    for ev in l_s_event:
        print("{:25} : {}".format(ev.name, ev.date))

