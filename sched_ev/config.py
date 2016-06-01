#########################################################################
#
#   Astronomy Club Event Generator
#   file: config.py
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


locations_gps = {
    # index 1 is default
    #     location / latitude / longitude (- is west) / elevation (meters)
     1 : ("Houge Park, Blg. 1"                , '37.257482', '-121.941998',   50),  # indoor
     2 : ("Houge Park"                        , '37.257471', '-121.942331',   50),  # outdoor
     3 : ("Rancho Cañada del Oro"             , '37.147076', '-121.775296',  200),
     4 : ("Mendoza Ranch"                     , '37.070585', '-121.522456',  300),
     5 : ("Coyote Valley"                     , '37.172142', '-121.729031',  100),
     6 : ("Pinnacles Nat'l Park, East Side"   , '36.489659', '-121.150614',  500),
     7 : ("Pinnacles Nat'l Park, West Side"   , '36.491788', '-121.209606',  500),
     8 : ("Yosemite Nat'l Park, Glacier Point", '37.727884', '-119.572965', 2800),
    99 : ("Other"                             , '0'        , '0'          ,    0),
}

