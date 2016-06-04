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
class Coordinator(TimeStampedModel):
    user = models.OneToOneField(User, primary_key=True)
    coordinator = ManyToManyField(Group)

