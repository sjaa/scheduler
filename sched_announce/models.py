from django.contrib.auth.models import User, Group
from django.core.exceptions     import ValidationError
from django.db                  import models
from django.utils.translation   import ugettext_lazy as _

from sched_core.models          import TimeStampedModel
from sched_core.const           import *
from sched_core.config          import site_names
from sched_ev.models            import EventType, Event, L_LOCATION, L_CATEGORY
from .const                     import AnnounceChannel, channel_name


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
for key, value in channel_name.items():
    channel[key] = value.replace('_', ' ')


# Has common fields for 'announce type' and 'announce'
class AnnounceBase(TimeStampedModel):
    # remaining fields get inherited to Announce
#   title           = models.CharField(max_length=40)
    channel         = models.IntegerField(choices=L_CHANNEL)
    
    is_preface      = models.BooleanField(default=False, choices=L_BOOLEAN, help_text=
                        'For email: If set, text goes before all announcements for the day.')
    use_header      = models.BooleanField(default=False, choices=L_BOOLEAN, help_text=
                        'For email: If set, use header for event name, location, date, time')
    lead_title      = models.CharField(max_length=40, blank=True, help_text=
                        'e.g., instructor, docent')
#   publish_later   = models.BooleanField(default=False, choices=L_BOOLEAN)
#   allow_change    = models.BooleanField(default=False, help_text=
#                       'If set, allow change after announcement is posted.')
#   text            = models.TextField(max_length=4000)
    rsvp_limit      = models.IntegerField(   null=True, blank=True, help_text=
                        'Meetup: max number of RSVPs')
    question        = models.TextField(max_length= 250, blank=True, help_text=
                        'Meetup: max 250 characters')
    text            = models.TextField(max_length=4000, blank=True)
    notes           = models.TextField(max_length=1000, blank=True)
    email           = models.TextField(max_length=1000, blank=True, help_text=
                        'email addresses - separate by spaces')
    send            = models.BooleanField(default=True, choices=L_BOOLEAN, help_text=
                        'Meetup: false means publish but don\'t send announcement')

    class Meta:
        abstract = True


class AnnounceType(AnnounceBase):
#   event_type      = models.ForeignKey  (EventType,
#                                         null=True, blank=True,
#                                         help_text=
#                       'For GCal by location.  Leave blank otherwise.')
#   location        = models.IntegerField(
#                                         null=True, blank=True,
#                                         choices=L_LOCATION, help_text=
#   partner_org     = models.IntegerField(
#                                         null=True, blank=True,
#                                         choices=L_PARTNER , help_text=
#                       'For GCal by partner.  Leave blank otherwise.')
#   category        = models.CharField   (max_length=2,
#                                         null=True, blank=True,
#                                         choices=L_CATEGORY, help_text=

    event_type      = models.ForeignKey(EventType,      null=True, blank=True)
    location        = models.IntegerField(              null=True, blank=True, choices=L_LOCATION,
                        help_text=
                        'For GCal by location.  Leave blank otherwise.')
    category        = models.CharField   (max_length=2, null=True, blank=True, choices=L_CATEGORY,
                        help_text=
                        'For GCal by category.  Leave blank otherwise.')
    days_offset     = models.IntegerField(default=26, help_text=
                        'Days before event that announcement is to be sent.')
    group           = models.ForeignKey(Group,          null=True, blank=True, related_name='group')
                        # validator > 0, < 180

    def __str__(self):
        if self.event_type:
#           return self.event_type.nickname
            return '{} ({})'.format(self.event_type.nickname, channel[self.channel])
            return 'foobar'
        if self.location:
            return '{} ({})'.format(channel[self.channel], site_names    [self.location])
        if self.category:
#           return 'foobar'
#           return str(self.channel) + '-' + self.category
            return '{} ({})'.format(channel[self.channel], event_category[self.category])
#           return '{} ({})'.format(channel[self.channel], 'foo')
#           return 'foo' + self.category + ':' + channel[self.channel]

    def clean(self):
        '''
        note: week and lunar_phase can be zero, so a test for a null field must be explicit:
            self.week!=none
        '''

        d = {}
        # by repeat
#       if (self.repeat in (EventRepeat.onetime.value, EventRepeat.annual.value)) \
        lst = (self.event_type, self.location, self.category)
        if sum(1 for i in lst if i != None) != 1:
            s = 'Exactly one of "Event type", "Channel", or "Group" must be specified'
            d['event_type'] = _(s)
        if self.event_type and not self.group:
            s = 'If "Event type" is specified, "Group" is requried'
            d['group'] = _(s)
        if len(d) > 0:
            raise ValidationError(d)


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
    date            = models.DateField('Date to announce')  # not normalized!
    date_posted     = models.DateTimeField(null=True, blank=True)
    date_announced  = models.DateTimeField(null=True, blank=True)
    date_canceled   = models.DateTimeField(null=True, blank=True)
    text_cancel     = models.TextField(max_length=500, blank=True)
    draft           = models.BooleanField(default=True, choices=L_BOOLEAN)

    class Meta:
        verbose_name = 'announcement'

    def description(self):
        return self.text if self.text else self.announce_type.text

    def question_get(self):
        return self.question if self.question else self.announce_type.question

    def rsvp_limit_get(self):
        return self.rsvp_limit if self.rsvp_limit else self.announce_type.rsvp_limit

    def notes_get(self):
        return self.notes if self.notes else self.announce_type.notes

    def __str__(self):
        return self.event.nickname + ':' + channel[self.channel]

#   def clean():
#       if is_preface:
#           if use_header:
#               s = 'If "Is preface" is set, then "Use header" must be off.'
#               d['use_prologue'] = _(s)
#           elif :

