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
import datetime
import calendar
import pytz
import ephem
from   sched_core.const           import FMT_YEAR_DATE_HM
from   django.contrib.auth.models import Group

# To generate all supported timezones:
#   python
#   >>> import pytz
#   >>> print(pytz.all_timezones)
TZ_NAME = 'US/Pacific'
TZ_LOCAL = pytz.timezone(TZ_NAME)

test_date = None

def local_time(date_time):
    return date_time.astimezone(TZ_LOCAL)

def local_time_str(date_time, fmt=None):
    if not fmt:
        fmt = FMT_YEAR_DATE_HM
    return date_time.astimezone(TZ_LOCAL).strftime(fmt)

def local_time_now():
    return datetime.datetime.now(TZ_LOCAL)

def local_date_now():
    if test_date:
        return test_date
    else:
        return datetime.date.today()

def set_local_date(date):
    global test_date
    test_date = date


def end_of_month(year, month):
    # get last day in month - monthrange returns (first day, last day)
    last_day_in_month = calendar.monthrange(year, month)[1]
    return last_day_in_month

def day_of_year(date):
#   jan_1 = TZ_LOCAL.localize(datetime.datetime(date.year, 1, 1))
    jan_1 = datetime.date(date.year, 1, 1)
    
    days = (date - jan_1).days + 1
    return days

# Keep track of most recent year used in current session
current_year = local_date_now().year
default_date_start = local_date_now()
default_date_end   = local_date_now()


@unique
class EventLocation(Enum):
    # index 1 is default
    HomeBase      =  1


########################################
# set location variables
#
locations_gps = {
    #     location / latitude / longitude (- is west) / elevation (meters)
    EventLocation.HomeBase     .value : ("Home Base"                         , '37.000000', '-121.000000',   50),  # indoor
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


@unique
class PartnerOrg(Enum):
    No_org        =  0
    CoSJ          =  1  # City of San Jose
    OSA           =  2  # Open Space Authority, Santa Clara County

partner = {
    PartnerOrg.No_org.value : 'None',
}


@unique
class TransactionSource(Enum):
    # index 1 is default
    cash          =  1
    Paypal        =  2
    SquareUp      =  3

CHOICES_TRANSACTION_SOURCE = []
for item in TransactionSource:
    CHOICES_TRANSACTION_SOURCE.append((item.value, item.name))


coordinator_email = {
    Group.objects.get(name='Star Party'          ).pk : 'starparty@my_org.net'           ,
    
def get_coord_email(group):
    email = coordinator_email.get(group.pk, None)
    return email
