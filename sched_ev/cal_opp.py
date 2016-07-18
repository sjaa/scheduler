#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_opp.py
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

import sys
import datetime
import ephem
import pdb
from   sched_core.const  import TZ_UTC, FMT_YEAR_DATE_HM, PLANETS
from   sched_core.config import TZ_LOCAL


EPHEM_SECOND = ephem.second
EPHEM_DAY    = ephem.hour*24
EPHEM_MONTH  = EPHEM_DAY*30


def ephem_elong(ephem_date, planet):
    planet.compute(ephem_date)
    return planet.elong


def calc(year, planet):
    '''
    Calculate opposition to solar system object.  Opposition occurs when
    elongation goes from -pi to +pi.

    'ephem.elong' is elongation (angle between object and sun) in radians.
    As string 'ephem.elong' is deg:min:sec.

    Note: Elongation monotonically (?) decreases towards -pi until past
           opposition, at which point elongation jumps to about +pi

    elongation vs time:
                |\      |\
          \     | \     | \
           \    |  \    |  \
          --\---|---\---|---\-
             \  |    \  |    \
              \ |     \ |
               \|      \|

    Notes: - Times within two minutes of Sky Safari in most cases, but not
             identical.
           - Tried the following, but the calcuated minimum point was off by a
               few minutes:
   http://stackoverflow.com/questions/10146924/finding-the-maximum-of-a-function

   solution = scipy.optimize.minimize_scalar(lambda x: -f(x),
                                             bounds=[0,1],
                                             method='bounded')
            - ephem uses 'float' data type to represent time, not datetime

    input
        year    int                 year to be generated
        planet  ephem.<planet>()    planet object

    output
        return  datetime            time of opposition of 'planet'
    '''
    # set start_date as one month before New Year's
    # Jan 1, midnight, local time
    new_years  = datetime.datetime(year, 1, 1, 0, 0)
    new_years  = TZ_UTC.localize(new_years)
    start_date = ephem.Date(new_years) - EPHEM_MONTH
    # set end_date as one month after New Year's of following year
    end_date   = ephem.Date(new_years) + EPHEM_MONTH*13
    date = start_date
    min_elong      = +4
    min_elong_date = date
    # sample elong every month and find min
    while date < end_date:
        planet.compute(date)
        elong = planet.elong
        if elong < min_elong:
            min_elong      = elong
            min_elong_date = date
        date = ephem.Date(date) + EPHEM_MONTH
    if min_elong_date==start_date or min_elong_date==end_date:
        # min elongation is outside year -> return nothing
        return None
    # elongation the month after opposition should be positive
    end_date       = ephem.Date(min_elong_date) + EPHEM_MONTH
    end_date_elong = ephem_elong(end_date, planet)     # should be < 0
    # binary search - find min elongation until interval becomes <= 1 second
    start_date = min_elong_date
    while end_date-start_date > EPHEM_SECOND:
        mid_date       = (start_date + end_date) / 2
        mid_date_elong = ephem_elong(mid_date, planet)
        if mid_date_elong > 0:
            end_date   = mid_date
        else:
            start_date = mid_date
        d = ephem.Date(start_date)
    # change 'start_date' to datetime format
    d = ephem.Date(start_date)
    date = ephem.localtime(d)
    date = TZ_LOCAL.localize(date)
    if date.year == year:
        return date
    return None


def calc_opp_planets(year):
    '''
        Calculate opposition to solar system objects.

        input
            year    int     year to be considered

        output
            return  list    list of datetime/planet string tuples
    '''

    l_events = []
    for planet in PLANETS:
        date_opp = calc(year, planet)
        if date_opp:
            # spaces for formatting
            event = (date_opp, "                               {} at opposition".format(planet.name))
            l_events.append(event)
    return l_events


if __name__ == '__main__':
    year = '2016'
    if len(sys.argv) > 1:
        year = sys.argv[1]
    else:
        tmp = input("Specify year [{}]: ".format(year))
        if tmp:
            year = tmp
    if not year.isdigit():
        print("{} is not a number".format(year))
        print("  opp.py [year]")
        exit()
    year = int(year)
    for date, s in calc_planets(year):
        print("{} - {}".format(date.strftime(FMT_YEAR_DATE_HM), s))
