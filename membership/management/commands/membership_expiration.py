#########################################################################
#
#   Astronomy Club Event Scheduler
#   file: membership/process.py
#
#   Copyright (C) 2017  Teruo Utsumi, San Jose Astronomical Association
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
#       2017-06-01  Teruo Utsumi, initial code
#
#########################################################################

import pdb
from   django.core.management.base import BaseCommand

from   membership.process          import cron_job
from   sched_core.test             import TestModes


class Command(BaseCommand):
    help = 'Check pending membership expiration and send reminder emails'

    def handle(self, *args, **options):
        test_modes = [TestModes.Email_To_Console.value, TestModes.Email_To_Tester.value]
#       test_modes = [TestModes.Email_To_Console.value]
        if not cron_job(username='cron_job', test_modes=test_modes):
            print('no membership renewal activity')
