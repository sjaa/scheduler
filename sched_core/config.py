#########################################################################
#
#   Astronomy Club Event Generator
#   file: sched_core/config.py
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
#       2016-05-25  Teruo Utsumi, initial code
#
#########################################################################

import pdb
from   enum                       import Enum, unique
from   collections                import OrderedDict
from   datetime                   import datetime
import pytz
import ephem
from   sched_core.const           import FMT_YEAR_DATE_HM
from   django.contrib.auth.models import Group
from   sched_core.models          import UserPermission

# To generate all supported timezones:
#   python
#   >>> import pytz
#   >>> print(pytz.all_timezones)
TZ_LOCAL = pytz.timezone('US/Pacific')

def local_time(date_time):
    return date_time.astimezone(TZ_LOCAL)

def local_time_str(date_time, fmt=None):
    if not fmt:
        fmt = FMT_YEAR_DATE_HM
    return date_time.astimezone(TZ_LOCAL).strftime(fmt)

def local_time_now():
    return datetime.now(TZ_LOCAL)


@unique
class EventLocation(Enum):
    # index 1 is default
    HougeParkBld1 =  1
    HougePark     =  2
    CampbellPark  =  3
    CupertinoCCtr =  4
    DeAnzaCollege =  5
    RanchoCanada  =  6
    MendozaRanch  =  7
    CoyoteValley  =  8
    PinnaclesEast =  9
    PinnaclesWest = 10
    YosemiteNPGP  = 11
    Other         = 99


########################################
# set location variables
#
locations_gps = {
    #     location / latitude / longitude (- is west) / elevation (meters)
    EventLocation.HougeParkBld1.value : ("Houge Park, Blg. 1"                , '37.257482', '-121.941998',   50),  # indoor
    EventLocation.HougePark    .value : ("Houge Park"                        , '37.257471', '-121.942331',   50),  # outdoor
    EventLocation.CampbellPark .value : ("Campbell Park"                     , '37.285939', '-121.939300',   30),
    EventLocation.CupertinoCCtr.value : ("Cupertino Civic Center"            , '37.319839', '-122.029243',   30),
    EventLocation.DeAnzaCollege.value : ("De Anza Community College"         , '37.319225', '-122.044609',   40),
    EventLocation.RanchoCanada .value : ("Rancho Cañada del Oro"             , '37.147076', '-121.775296',  200),
    EventLocation.MendozaRanch .value : ("Mendoza Ranch"                     , '37.070585', '-121.522456',  300),
    EventLocation.CoyoteValley .value : ("Coyote Valley"                     , '37.172142', '-121.729031',  100),
    EventLocation.PinnaclesEast.value : ("Pinnacles Nat'l Park, East Side"   , '36.489659', '-121.150614',  500),
    EventLocation.PinnaclesWest.value : ("Pinnacles Nat'l Park, West Side"   , '36.491788', '-121.209606',  500),
    EventLocation.YosemiteNPGP .value : ("Yosemite Nat'l Park, Glacier Point", '37.727884', '-119.572965', 2800),
    EventLocation.Other        .value : ("Other"                             , '0'        , '0'          ,    0)
}

sites      = {}
site_names = OrderedDict()
for key, value in locations_gps.items():
    site = ephem.Observer()
    site.lat        = value[1]
    site.lon        = value[2]
    site.elevation  = value[3]
    sites     [key] = site
    site_names[key] = value[0]


coordinator_email = {
    Group.objects.get(name='Beginners Class'             ).pk : 'astronomy101@sjaa.net'        ,
    Group.objects.get(name='Board of Directors'          ).pk : 'president@sjaa.net'           ,
    Group.objects.get(name='In-town Star Party'          ).pk : 'president@sjaa.net'           ,
    Group.objects.get(name='Fix It'                      ).pk : 'fixit@sjaa.net'               ,
    Group.objects.get(name='Astro Imaging SIG'           ).pk : 'imagingsig@sjaa.net'          ,
    Group.objects.get(name='Dark Sky'                    ).pk : 'president@sjaa.net'           ,
    Group.objects.get(name='Quick STARt'                 ).pk : 'quickstart@sjaa.net'          ,
    Group.objects.get(name='Solar Observing'             ).pk : 'solar@sjaa.net'               ,
    Group.objects.get(name='Starry Night'                ).pk : 'starrynights@sjaa.net'        ,
    Group.objects.get(name='General Meeting'             ).pk : 'speaker@sjaa.net'             ,
    Group.objects.get(name='General Meeting Refreshments').pk : 'marianne_damon@yahoo.com'     ,
    Group.objects.get(name='Binocular Stargazing'        ).pk : 'binocular.stargazing@sjaa.net',
    Group.objects.get(name='Coders'                      ).pk : 'director3@sjaa.net'           ,
    Group.objects.get(name='Astro Imaging Workshop'      ).pk : 'handsonimaging@sjaa.net'       }
    
def get_coord_email(group):
    email = coordinator_email.get(group.pk, None)
    return email
