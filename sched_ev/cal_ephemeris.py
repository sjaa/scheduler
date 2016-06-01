#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_ephemeris.py
#
#   Copyright (C) 2016  Teruo Utsumi, San Jose Astronomical Association
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
#       2016-02-25  Teruo Utsumi, initial code
#
#########################################################################

import datetime
import pdb
import ephem
from   enum               import Enum, unique

from   .models            import AuxEvent
from   sched_ev.cal_const import *
from   sched_ev.cal_opp   import calc_opp_planets


#astro_events = []
#moon_phase   = []


def cal_ephemeris(year):
#   global moon_phase

#   moon_phase   = []
    #
#   def __init__(self, year):
    '''
        Generate seasons, moon, opposition data for entire year
    '''
#   global moon_phase
#   global astro_events
    astro_events = []

    # moon phase for every day of year help determine default event dates
    moon_phase = ['']*368
    # exact datetime of lunar phases for calendar
#   self.moon_events = []

    # Jan 1, midnight, local time
    new_years  = datetime.datetime(year, 1, 1, 0, 0)
    new_years  = TZ_LOCAL.localize(new_years)
    site = sites[1]
    site.date = new_years.astimezone(TZ_UTC)

    # Generate seasons
    season = {
        'spring': (ephem.next_vernal_equinox , 'Spring Equinox' ),
        'summer': (ephem.next_summer_solstice, 'Summer Solstice'),
        'fall'  : (ephem.next_autumn_equinox , 'Fall Equinox'   ),
        'winter': (ephem.next_winter_solstice, 'Winter Solstice')
    }
    for e in ('spring', 'summer', 'fall', 'winter'):
        m, n = season[e]
        d0   = m(new_years)
        d1   = TZ_LOCAL.localize(ephem.localtime(d0))
        # spaces for formatting
        n    = '              ' + n
        astro_events.append((d1, n))

    # Generate moon phase events
    next_phase = {
        #                      method to get phase          , name of phase , next phase
        RuleLunar.moon_new  : (ephem.next_new_moon          , 'New moon'    , RuleLunar.moon_1q  ),
        RuleLunar.moon_1q   : (ephem.next_first_quarter_moon, '1st Qtr moon', RuleLunar.moon_full),
        RuleLunar.moon_full : (ephem.next_full_moon         , 'Full moon'   , RuleLunar.moon_3q  ),
        RuleLunar.moon_3q   : (ephem.next_last_quarter_moon , '3rd Qtr moon', RuleLunar.moon_new )
    }
    y         = year - 1
    next_year = year + 1
    ph = RuleLunar.moon_new
    # Generate each successive moon phase event
    # start in December of prior year ("30" days before New Year's Day)
    #   to first phase in next year
    d0 = new_years - DAY*30
    l_moon_phases = []
    while y != next_year:
        prev_ph = ph
        m, n, ph = next_phase[ph]
        d0       = m(d0)
#       d1       = ephem.localtime(d0)
        d1       = TZ_LOCAL.localize(ephem.localtime(d0))
        y        = d1.year
        if y == year:
            astro_events.append((d1, n))
        l_moon_phases.append((d1, prev_ph))
    # append list of planetary oppositions
    astro_events += calc_opp_planets(year)
    astro_events.sort()
    # Add astro event to AuxEvents
    for date, title in astro_events:
        dt = date.astimezone(TZ_LOCAL).date()
        title = title.strip()
#       print(":", date, title)
        queryset = AuxEvent.objects.filter(date=dt, category=AuxCategory.astro_event.value)
        # add astro event if it's not already in AuxEvent
        if not queryset or title not in [t.title for t in queryset]:
#           print("-- adding {} {}".format(title, str(dt)))
#           pdb.set_trace()
            s = AuxEvent()
            s.title    = title
            s.category = AuxCategory.astro_event.value
            s.date     = dt
            # store time in notes
            s.notes    = date.strftime(FMT_HMP).lstrip('0')
            s.save()

    # populate "moon_phase" with moon phase for every day of year
    ph_time, ph = l_moon_phases.pop(0)
    for e in l_moon_phases:
        next_ph_time, next_ph = e
        delta_ph_time = next_ph_time - ph_time
        # find midpoint between two consecutive lunar events,
        #   e.g., 1Q, full moon
        mid_ph_time   = ph_time + delta_ph_time/2
        # append midpoint time
        # use old phase if midpoint is after 7pm, otherwise use new phase
        if mid_ph_time.year == year:
            # day of year, e.g., 201
            mid_ph_day  = int(mid_ph_time.strftime("%j"))
            moon_phase[mid_ph_day] = ph if mid_ph_time.hour>=19 else next_ph
        ph_time = next_ph_time
        ph      = next_ph
        # fill in "moon_phase" 10 days after midpoint with "ph"
        # 10 days ensures no gap between this midpoint and the next
        for j in range(1, 12):
            day = mid_ph_time + DAY*j
            # don't fill in moon_phase if day is not in current year
            if day.year == year:
                k  = int(day.strftime("%j"))
                moon_phase[k] = ph
    return moon_phase


def calc_date_ephem(date_time, location):
    '''
    input:
        date     - datetime.datetime
        location - location key
    output:
        return string of sun/moon ephemeris for 'date', e.g. for 2016 02/28:
            06:00 PM sunset - 06:28 PM / 06:58 PM / 07:28 PM
            10:06 PM moonrise - 66%
        One of moonrise or moonset is generated, whichever is after 3pm that day.
    output:
        Generate strings of
          - sunset and twilight
          - 'moonrise' or 'moonset' / time / % illumination
        One of moonrise or moonset is generated, whichever is after 3pm that day.
        E.g.:
            (('6:00 PM', '06:28 PM', '06:58 PM', '07:28 PM'),
             ('moonrise', '10:06 PM', '66%'))
    '''

    # Get sunset, twiilight times
    # set time for noon
    date = TZ_LOCAL.localize(datetime.datetime.combine(date_time, datetime.time(12, 0)))
    site = sites[location]
    site.date    = date.astimezone(TZ_UTC)
    sunset = []
    fmt = FMT_HMP
    # calculate time and format string
    for horizon in (RuleStartTime.sunset      ,
                    RuleStartTime.civil       ,
                    RuleStartTime.nautical    ,
                    RuleStartTime.astronomical ):
        site.horizon = rule_horizon[horizon.value]
        t = TZ_LOCAL.localize(ephem.localtime(site.next_setting(SUN)))
        t = t.strftime(fmt)
        fmt = FMT_HM
        sunset.append(t)

    # Get moon data
    # re-set horizon
    site.horizon = '0'
    # find moonrise/set following 3pm
    date = TZ_LOCAL.localize(date.combine(date, datetime.time(15, 0)))
    site.date    = date.astimezone(TZ_UTC)
    time_moonset = TZ_LOCAL.localize(ephem.localtime(site.next_setting(MOON)))
    # figure out which of moonrise/moonset occurs from 3pm-3am
    if date <= time_moonset < date + HOUR*12:
        mode = 'moonset'
        time = time_moonset.strftime(FMT_HMP)
    else:
        mode = 'moonrise'
        time_moonrise = TZ_LOCAL.localize(ephem.localtime(site.next_rising(MOON)))
        time = time_moonrise.strftime(FMT_HMP)
    # Compute moon so illumination is accurate for start of event
    MOON.compute(date_time)
    illumination = '{:1.0f}%'.format(MOON.phase)
    moon = (mode, time, illumination)
    return sunset, moon
            
if __name__ == '__main__':
    date = datetime.datetime(2016,2,28)
    print(calc_date_ephem(date))
