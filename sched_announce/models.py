from django.contrib.auth.models import User, Group
from django.core.exceptions     import ValidationError
from django.db                  import models
from django.utils.translation   import ugettext_lazy as _

from sched_core.models          import TimeStampedModel
from sched_core.const           import *
from sched_ev.models            import EventType, Event
from .const                     import AnnounceChannel


L_CHANNEL   = []

lists = (
         (AnnounceChannel    , None         , L_CHANNEL  ),
)


for l in lists:
    rule, rule_string, l_choice = l
    for item in rule:
        if rule_string:
            s = rule_string[item]
        else:
            s = item.name 
        l_choice.append((item.value, s))

channel = {}
for ch in AnnounceChannel:
    channel[ch.value] = ch.name.replace('_', ' ')

# Has common fields for 'announce type' and 'announce'
class AnnounceBase(TimeStampedModel):
    # remaining fields get inherited to Announce
#   title           = models.CharField(max_length=40)
    channel         = models.IntegerField(choices=L_CHANNEL)
    is_preface      = models.BooleanField(default=False, choices=L_BOOLEAN, help_text=
                        'If set, text goes before all announcements for the day.')
    use_header      = models.BooleanField(default=False, choices=L_BOOLEAN, help_text=
                        'If set, use header for event name, location, date, time')
    lead_title      = models.CharField(max_length=40, blank=True, help_text=
                        'e.g., instructor, docent')
#   publish_later   = models.BooleanField(default=False, choices=L_BOOLEAN)
#   allow_change    = models.BooleanField(default=False, help_text=
#                       'If set, allow change after announcement is posted.')
#   text            = models.TextField(max_length=4000)
    text            = models.TextField(max_length=4000, blank=True)
    notes           = models.TextField(max_length=1000, blank=True)

    class Meta:
        abstract = True


class AnnounceType(AnnounceBase):
#   event_type      = models.ForeignKey(EventType, related_name='announce_event_type')
    event_type      = models.ForeignKey(EventType)
    group           = models.ForeignKey(Group, related_name='group')
    days_offset     = models.IntegerField(default=40, help_text=
                        'Days before announcement is to be sent.<br>' +
                        'If "Publish later" is set: days before ' +
                        'announcement is to be published.')
                        # validator > 0, < 180

    def __str__(self):
        return self.event_type.nickname + ':' + channel[self.channel]


class Announce(AnnounceBase):
    # TODO: remove 'event_type' from AnnounceType
#   event_type      = models.ForeignKey(EventType, related_name='announce_event_type')
    event_type      = models.ForeignKey(EventType)
    event           = models.ForeignKey(Event, related_name='announce_event')
    event_api_id    = models.CharField(max_length=50, blank=True, help_text=
                        'e.g., for Meetup API')
    announce_type   = models.ForeignKey(AnnounceType, related_name='announce_type')
#   owner           = ForeignField(User, related_name='owner')
    # if text is blank, use field from parent AnnounceType instance
#   text            = models.TextField(max_length=4000, blank=True)
    date            = models.DateField()  # not normalized!
    date_posted     = models.DateTimeField(null=True, blank=True)
    date_announced  = models.DateTimeField(null=True, blank=True)
    date_canceled   = models.DateTimeField(null=True, blank=True)
    text_cancel     = models.TextField(max_length=500, blank=True)
    draft           = models.BooleanField(default=True, choices=L_BOOLEAN)

    class Meta:
        verbose_name = 'announcement'

    def description(self):
        return self.text if self.text else self.announce_type.text

    def __str__(self):
        return self.event.nickname + ':' + channel[self.channel]

#   def clean():
#       if is_preface:
#           if use_header:
#               s = 'If "Is preface" is set, then "Use header" must be off.'
#               d['use_prologue'] = _(s)
#           elif :

