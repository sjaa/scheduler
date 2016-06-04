from django.contrib.auth.models import User, Group
from django.core.exceptions     import ValidationError
from django.utils.translation   import ugettext_lazy as _

from core.models                import TimeStampedModel

import models
import groups



# Has common fields for 'announce type' and 'announce'
class AnnounceBase(TimeStampedModel):
    # remaining fields get inherited to Announce
#   title           = CharField(max_length=40)
    channel         = IntegerField(choices=L_CHANNEL)
    is_preface      = BooleanField(default=False, help_text=
                        'If set, text goes before all announcements for the day.'
    use_header      = BooleanField(default=True, help_text=
                        'If set, use header for event name, location, date, time')
    lead_title      = CharField(max_length=40, blank=True, help_text=
                        'e.g., instructor, docent')
    publicize_later = BooleanField(default=False)
#   allow_change    = BooleanField(default=False, help_text=
#                       'If set, allow change after announcement is posted.')
    text            = TextField(max_length=4000)
    notes           = TextField(max_length=1000, blank=True)

    class Meta:
        abstract = True

    def __str__():
        return self.title


class AnnounceType(AnnounceBase):
    event_type      = ForeignField(EventType, related_to='event_type')
    group           = ForeignKey(Group, related_to='group')
    days_offset     = IntegerField(default=40, help_text=
                        'Days before announcement is to be sent.<br>' +
                        'If "Publicize later" is set: days before ' +
                        'announcement is to be publicized.')
                        # validator > 0, < 180


class Announce(AnnounceBase):
    # TODO: remove 'event_type' from AnnounceType
    event           = ForeignField(Event, related_to='event')
    event_api_id    = TextField(max_length=50, blank=True, help_text=
                        'e.g., for Meetup API')
#   owner           = ForeignField(User, related_to='owner')
    # if text is blank, use field from parent AnnounceType instance
    text            = TextField(max_length=4000, blank=True)
#   publicize_later = BooleanField()
    date            = DateField()  # not normalized!
    date_sent       = DateTimeField(null=True, blank=True)
    date_publicized = DateTimeField(null=True, blank=True)
    draft           = BooleanField(default=True)

    def clean():
        if is_preface:
            if use_prologue:
                s = 'If "Is preface" is set, then "Use prologue" must be off.'
                d['use_prologue'] = _(s)
            elif 

