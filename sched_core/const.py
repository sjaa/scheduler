#########################################################################
#
#   Astronomy Club Event Scheduler
#   file: sched_core/const.py
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
#       2016-06-04  Teruo Utsumi, initial code
#
#########################################################################

import datetime
import pytz

from   sched_core.config  import TZ_LOCAL


DAY_DST  = datetime.timedelta(days=1, hours=4)
DAY      = datetime.timedelta(days=1)
HOUR     = datetime.timedelta(hours=1)
MINUTE   = datetime.timedelta(minutes=1)
SECOND   = datetime.timedelta(seconds=1)
TZ_UTC   = pytz.timezone('UTC')

FMT_YEAR_DATE_HM = "%Y %a %m/%d %I:%M %p"
FMT_DATE_Y = "%a %m/%d %Y"
FMT_DATE = "%m/%d"
FMT_YDATE = "%Y %m/%d"
FMT_HMP  = "%I:%M %p"
FMT_HM   = "%I:%M"
FMT_HMS  = "%I:%M:%S %p"


########################################
# for models
#
L_BOOLEAN = (
        (True , 'true'),
        (False, 'false'),
)


def local_time(date_time):
    return date_time.astimezone(TZ_LOCAL).strftime(FMT_YEAR_DATE_HM)
