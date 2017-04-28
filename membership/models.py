from django.db                  import models
from django.utils               import timezone
from django.contrib.auth.models import AbstractUser, Group

from sched_core.const           import L_BOOLEAN
from sched_core.models          import TimeStampedModel
from .config                    import CHOICES_MEM_STATUS


# User:
# first name
# last name
# email


# Parallel table to Tendenci membership table
#class Membership(TimeStampedModel):
class User(AbstractUser):
    # pk implicit
#   user       = models.OneToOneField(User, null=True, blank=True, help_text=
#                                     'Click "+" to add new user')
#   date_since    = models.DateField('Member since'              , auto_now_add=True)
#   date_start    = models.DateField('Start of membership period', null=True, blank=True, auto_now_add=True)
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



