#########################################################################
#
#   Astronomy Club Event Generator
#   file: cal_const.py
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
import pytz
import ephem
from   enum        import Enum, unique


# To deal w/ DST transitions, set 'DAY_DST' to more than 24 hours
# After adding 'day'
# - use tz.normalize()
# - date.replace(hour=0) to set hour to midnight
DAY_DST  = datetime.timedelta(days=1, hours=4)
DAY      = datetime.timedelta(days=1)
HOUR     = datetime.timedelta(hours=1)
MINUTE   = datetime.timedelta(minutes=1)
SECOND   = datetime.timedelta(seconds=1)
TZ_UTC   = pytz.timezone('UTC')
# TODO: move to configuration, need method to show all possible timezones
# To generate all supported timezones:
#   python
#   >>> import pytz
#   >>> print(pytz.all_timezones)
TZ_LOCAL = pytz.timezone('US/Pacific')

FMT_YEAR_DATE_HM = "%Y %a %m/%d %I:%M %p"
FMT_DATE_Y = "%a %m/%d %Y"
FMT_DATE = "%m/%d"
FMT_YDATE = "%Y %m/%d"
FMT_HM   = "%I:%M %p"
FMT_HMS  = "%I:%M:%S %p"

########################################
# initialization for 'ephem' module
SUN     = ephem.Sun()
MOON    = ephem.Moon()
PLANETS = ( ephem.Mars()  , ephem.Jupiter(), ephem.Saturn(),
            ephem.Uranus(), ephem.Neptune(), ephem.Pluto()  )

local = ephem.Observer()
# TODO: move to configuration
local.lat       =   '37.257465'  # houge_park_lat
local.lon       = '-121.942281'  # houge_park_lon
local.elevation = 50             # houge_park_elev


########################################
# Rules that govern scheduling of events
@unique
class RuleWeek(Enum):
    week_1       = 0
    week_2       = 1
    week_3       = 2
    week_4       = 3
    week_5       = 4


@unique
class RuleLunar(Enum):
    moon_new     = 0
    moon_1q      = 1
    moon_full    = 2
    moon_3q      = 3


@unique
class RuleStartTime(Enum):
    absolute     = 'ab'  # start time specifies exact time
    sunset       = 'su'  # others specfies twilight on given day
    civil        = 'ci'
    nautical     = 'na'
    astronomical = 'as'


@unique
class RuleWeekday(Enum):
    # to match datetime.weekday()
    monday       = 0
    tuesday      = 1
    wednesday    = 2
    thursday     = 3
    friday       = 4
    saturday     = 5
    sunday       = 6


@unique
class AuxCategory(Enum):
    holiday      = 'ho'
    astro_event  = 'as'
    sunset       = 'su'


@unique
class EventCategory(Enum):
#   ephemeris    = 'ep'
    public       = 'pu'
    member       = 'me'
    volunteer    = 'vo'
    coordinator  = 'co'
    private      = 'pr'
    board        = 'bo'
    external     = 'ex'
#   observers    = 'ob'
#   imagers      = 'im'


@unique
class EventRepeat(Enum):
    onetime      = 'on'
#   weekly       = 'we'  # not currently supported
    monthly      = 'mo'
    lunar        = 'lu'
    annual       = 'an'


########################################
# Locations not hard coded.
# TODO: Need to move to file for configuration data
locations = { 1 : "Houge Park, Blg. 1",  # indoor
              2 : "Houge Park",          # outdoor
              3 : "Rancho Cañada del Oro",
              4 : "Mendoza Ranch",
              5 : "Coyote Valley",
              6 : "Pinnacles Nat'l Park, East Side",
              7 : "Pinnacles Nat'l Park, West Side",
              8 : "Yosemite Nat'l Park, Glacier Point"
}

########################################
# Pools not hard coded.
# TODO: Need to move to file for configuration data
pools     = {
              1 : "admin"  ,
              2 : "Board of Directors",
              3 : "Beginners Class",
              4 : "Binocular Stargazing",
              5 : "Coordinator",
              6 : "Dark Sky Site",
              7 : "Fix It",
              8 : "General Meeting",
              9 : "ITSP",
             10 : "Imaging SIG",
             11 : "Library",
             12 : "Loaner",
             13 : "Quick STARt",
             14 : "Solar",
             15 : "Starry Night",
             16 : "Pinnacles Nat'l Park",
             17 : "Yosemite Nat'l Park"
}


########################################
# display strings corresponding to above rules
mo = datetime.datetime(2007, 1, 1).strftime('%A')  # 2007/1/1 is Monday
tu = datetime.datetime(2007, 1, 2).strftime('%A')
we = datetime.datetime(2007, 1, 3).strftime('%A')
th = datetime.datetime(2007, 1, 4).strftime('%A')
fr = datetime.datetime(2007, 1, 5).strftime('%A')
sa = datetime.datetime(2007, 1, 6).strftime('%A')
su = datetime.datetime(2007, 1, 7).strftime('%A')
rule_week        = { RuleWeek.week_1             : '1st week'    ,
                     RuleWeek.week_2             : '2nd week'    ,
                     RuleWeek.week_3             : '3rd week'    ,
                     RuleWeek.week_4             : '4th week'    ,
                     RuleWeek.week_5             : '5th week'     }
rule_weekday     = { RuleWeekday.sunday          : su            ,
                     RuleWeekday.monday          : mo            ,
                     RuleWeekday.tuesday         : tu            ,
                     RuleWeekday.wednesday       : we            ,
                     RuleWeekday.thursday        : th            ,
                     RuleWeekday.friday          : fr            ,
                     RuleWeekday.saturday        : sa             }
'''
# to match datetime.weekday()
weekday_to_int   = { RuleWeekday.sunday          : 6             ,
                     RuleWeekday.monday          : 0             ,
                     RuleWeekday.tuesday         : 1             ,
                     RuleWeekday.wednesday       : 2             ,
                     RuleWeekday.thursday        : 3             ,
                     RuleWeekday.friday          : 4             ,
                     RuleWeekday.saturday        : 5              }
weekday_to_int   = { su                          : 6             ,
                     mo                          : 0             ,
                     tu                          : 1             ,
                     we                          : 2             ,
                     th                          : 3             ,
                     fr                          : 4             ,
                     sa                          : 5              }
weekday_to_int   = { 
                     6                           : su            ,
                     0                           : mo            ,
                     1                           : tu            ,
                     2                           : we            ,
                     3                           : th            ,
                     4                           : fr            ,
                     5                           : sa             }
'''
##########################
# for astronomy scheduling
rule_start_time  = { RuleStartTime.absolute      : 'absolute'    ,
                     RuleStartTime.sunset        : 'sunset'      ,
                     RuleStartTime.civil         : 'civil'       ,  # add "twilight"?
                     RuleStartTime.nautical      : 'nautical'    ,
                     RuleStartTime.astronomical  : 'astronomical' }
rule_lunar       = { RuleLunar.moon_new          : 'new moon'    ,
                     RuleLunar.moon_1q           : '1Q moon'     ,
                     RuleLunar.moon_full         : 'full moon'   ,
                     RuleLunar.moon_3q           : '3Q moon'      }
rule_horizon     = { RuleStartTime.sunset.value       : '0'      ,
                     RuleStartTime.civil.value        : '-6'     ,
                     RuleStartTime.nautical.value     : '-12'    ,
                     RuleStartTime.astronomical.value : '-18'     }
##########################
aux_category     = { AuxCategory.holiday         : 'holiday'     ,
                     AuxCategory.astro_event     : 'astro event' ,
                     AuxCategory.sunset          : 'sunset'       }
event_category   = { EventCategory.public        : 'public'      ,
                     EventCategory.member        : 'member'      ,
                     EventCategory.volunteer     : 'volunteer'   ,
                     EventCategory.coordinator   : 'coordinator' ,
                     EventCategory.private       : 'private'     ,
                     EventCategory.board         : 'board'       ,
                     EventCategory.external      : 'external'     }
event_repeat     = { EventRepeat.onetime         : 'one-time'    ,
                     EventRepeat.monthly         : 'monthly'     ,
#                    EventRepeat.weekly          : 'weekly'      ,
                     EventRepeat.lunar           : 'lunar'       ,
                     EventRepeat.annual          : 'annual'       }

channels = { 1: "GCal",
             2: "Meetup",
             3: "SJAA email",
             4: "member email",
             5: "Twitter",
             6: "Facebook",
             7: "Wordpress"
}

channel_public = {
    1 : False,  # GCal
    2 : True , # Meetup
    3 : True , # SJAA announcelist email
    4 : False, # member email
    5 : True , # Twitter
    6 : True , # Facebook
    7 : False  # member email
}
