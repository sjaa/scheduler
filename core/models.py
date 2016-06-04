from django.db import models

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
    user = models.OneToOneField(User, primary_key=True)
    groups      = ManyToManyField(Group, related_to='groups')
    coordinator = ManyToManyField(Group, related_to='coordinator')

