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

from   enum        import Enum, unique
import pytz


# To generate all supported timezones:
#   python
#   >>> import pytz
#   >>> print(pytz.all_timezones)
TZ_LOCAL = pytz.timezone('US/Pacific')


# Enumerated values MUST be no more than two characters
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


coordinator = {}

def init():
    if coordinator:
        # ran previously
        return
    # find all coordinators
    users = UserPermission.objects.all()
    for user in users:
        for group in user.coordinator:
            coordinator[group] = user
