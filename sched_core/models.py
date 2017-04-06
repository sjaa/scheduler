from django.contrib.auth.models import User, Group
from django.db                  import models

from .const                     import *


class TimeStampedModel(models.Model):
    '''
    Ab abstract base class model that provides self-
    updating 'created' and 'modified' fields.
    '''
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now    =True)

    class Meta:
        abstract = True


###################
# For permissions #
###################
# Define separate 'group' since 'User' may come from different database
class UserPermission(TimeStampedModel):
    user        = models.OneToOneField(User, primary_key=True)
    volunteer   = models.BooleanField(default=False, choices=L_BOOLEAN)
    groups      = models.ManyToManyField(Group, related_name='perm_group'      , blank=True)
    coordinator = models.ManyToManyField(Group, related_name='perm_coordinator', blank=True)
    notes       = models.TextField(max_length=400, blank=True)

