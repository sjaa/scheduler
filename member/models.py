from django.db                  import models
from django.utils               import timezone
from django.contrib.auth.models import User, Group

from core.models                import TimeStampedModel


class MemberSubst(TimeStampedModel):
    # pk implicit
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    active = models.BooleanField()
    notes = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name

class MemberAux(TimeStampedModel):
    # pk implicit
    member = models.OneToOneField(MemberSubst, primary_key=True)
    groups = models.ManyToManyField(Group)
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    active = models.BooleanField()
    notes = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name

