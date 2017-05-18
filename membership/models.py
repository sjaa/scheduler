#########################################################################
#
#   Astronomy Club Membership
#   file: membership/models.py
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

from django.db                  import models
from django.utils               import timezone
from django.contrib.auth.models import AbstractUser, Group

from sched_core.const           import L_BOOLEAN
from sched_core.test            import TestModes
from sched_core.models          import TimeStampedModel
from .config                    import CHOICES_MEM_STATUS

# Parallel table to Tendenci membership table
#class Membership(TimeStampedModel):
class User(AbstractUser):
    # pk implicit
    date_since  = models.DateField('Member since'              , null=True, blank=True)
    date_start  = models.DateField('Start of membership period', null=True, blank=True)
    date_end    = models.DateField('End of membership period'  , null=True, blank=True)
    addr1       = models.CharField('Address 1', max_length=40)
    addr2       = models.CharField('Address 2', max_length=40, null=True, blank=True)
    city        = models.CharField(max_length=40)
    state       = models.CharField(max_length=2 )
    zip_code    = models.CharField(max_length= 5)
    phone1      = models.CharField('Phone 1', max_length=15, null=True, blank=True)
    phone2      = models.CharField('Phone 2', max_length=15, null=True, blank=True)
    status      = models.IntegerField(default=0, choices=CHOICES_MEM_STATUS)
    notices     = models.IntegerField(default=0, help_text=
                                     'Default: 0 -- # of renewal notices sent', null =True)
    associate   = models.BooleanField(default=False, help_text=
                                     'True: not member but on announce email list')
    notes       = models.TextField(max_length=500, blank=True)
    volunteer   = models.BooleanField(default=False, choices=L_BOOLEAN)
    coordinator = models.ManyToManyField(Group, related_name='user_coordinator', blank=True)
    modified    = models.DateTimeField(auto_now=True, null=True, blank=True)

'''
    def save(self, *args, **kwargs):
#       if TestModes.Fake_Save.value in test_modes:
        if False:
            # don't update entry for 'member'
            if self.pk:
                print('Membership: fake save -- new member')
            else:
                print('Membership: fake save -- renewing member')
            return
        else:
            super(User, self).save(*args, **kwargs)
'''
