#########################################################################
#
#   Astronomy Club Event Generator
#   file: const.py
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
from   collections       import OrderedDict

import pytz
import ephem
from   enum              import Enum, unique
#from   sched_core.const  import EventCategory
from   sched_core.config import site_names

########################################
# initialization for 'ephem' module
#
SUN     = ephem.Sun()
MOON    = ephem.Moon()
PLANETS = ( ephem.Mars()  , ephem.Jupiter(), ephem.Saturn(),
            ephem.Uranus(), ephem.Neptune(), ephem.Pluto()  )
