from django.db                  import models
from django.utils               import timezone
from django.contrib.auth.models import User, Group
from django.core.urlresolvers   import reverse

from core.models                import TimeStampedModel
from ev_sched.cal_const         import *


###############################################################
# 
# Model Managers
# 
###############################################################

class EventDraftManager(models.Manager):
    def get_queryset(self):
        return super(EventDraftManager, self).get_queryset().filter(draft=True)

###############################################################
# 
# Models
# 
###############################################################

# choices for models
L_CATEGORY    = []
L_REPEAT      = []
L_LUNAR_PHASE = []
L_WEEK        = []
L_WEEKDAY     = []
L_STARTTIME   = []
L_LOCATION    = []
L_GROUP       = []

lists = (
         (EventCategory  , event_category  , L_CATEGORY   ),
         (EventRepeat    , event_repeat    , L_REPEAT     ),
         (RuleLunar      , rule_lunar      , L_LUNAR_PHASE),
         (RuleWeek       , rule_week       , L_WEEK       ),
         (RuleWeekday    , rule_weekday    , L_WEEKDAY    ),
         (RuleStartTime  , rule_start_time , L_STARTTIME  )
)

L_MONTH = (
        ( 1 , 'Jan'),
        ( 2 , 'Feb'),
        ( 3 , 'Mar'),
        ( 4 , 'Apr'),
        ( 5 , 'May'),
        ( 6 , 'Jun'),
        ( 7 , 'Jul'),
        ( 8 , 'Aug'),
        ( 9 , 'Sep'),
        (10 , 'Oct'),
        (11 , 'Nov'),
        (12 , 'Dec')
)

L_BOOLEAN = (
        (True , 'true'),
        (False, 'false'),
)

L_VERIFIED = (
        (True , 'verified'),
        (False, 'NOT verified'),
)

groups = Group.objects.all()
for g in groups:
    L_GROUP.append((g.name, g))

for l in lists:
    rule, rule_strings, l_choice = l
    for item in rule:
        l_choice.append((item.value, rule_strings[item]))

for loc in locations:
    L_LOCATION.append((loc, locations[loc]))


'''
class EphemType(TimeStampedModel):
    title             = models.CharField    (         max_length=40                  )
    date_time         = models.DateTimeField("Day's ephemeris", null=True, blank=True)
    notes             = models.TextField    ('Notes', max_length=1000,     blank=True)

    def __str__(self):
        return self.title
'''


class EventType(TimeStampedModel):
    class Meta:
        ordering = ['nickname']

    nickname          = models.CharField    ('Type', max_length=40, unique = True,
                                             help_text='internal name for event')
    title             = models.CharField    (max_length=40, blank=True,
                                             help_text='external name for event.  Leave blank if same as "Type"')
    category          = models.CharField    (max_length=2, default='pu', choices=L_CATEGORY)
    repeat            = models.CharField    (max_length=2, default='lu', choices=L_REPEAT)
    lunar_phase       = models.IntegerField (                            choices=L_LUNAR_PHASE, null=True, blank=True,
                                             help_text='required if <b>repeat</b> is <b>lunar</b>')
    date              = models.DateField    (                                                   null=True, blank=True,
                                             help_text='YYYY-MM-DD -- required if <b>repeat</b> is <b>one-time</b>')
    month             = models.IntegerField (                            choices=L_MONTH      , null=True, blank=True,
                                             help_text='required if <b>repeat</b> is <b>one-time</b> or <b>annual</b>')
    week              = models.IntegerField (                            choices=L_WEEK       , null=True, blank=True,
                                             help_text='required if <b>repeat</b> is <b>monthly</b>')
    weekday           = models.IntegerField (                            choices=L_WEEKDAY    , null=True, blank=True,
                                             help_text='required if <b>repeat</b> is <b>monthly</b> or <b>lunar</b>')
    rule_start_time   = models.CharField    ('Start time rule',
                                             max_length=2, default='na', choices=L_STARTTIME  ,
                                             help_text='required if <b>repeat</b> is <b>lunar</b>')
    time_start        = models.TimeField    ('Start time',
                                                                                                null=True, blank=True,
                                             help_text='h:mm, <b>24-HOUR</b> -- time required if <b>Start time rule</b> is <b>absolute</b>')
    time_start_offset = models.DurationField('Start time offset',
                                                                                                null=True, blank=True,
                                             help_text='in hh:mm[:ss]'                            )
    neg_start_offset  = models.BooleanField('Negative start offset', default=False, choices=L_BOOLEAN,
                                             help_text='set to "true" if <b>Start time offset</b> is negative')
    time_earliest     = models.TimeField    ('Earliest start time',
                                                                                                null=True, blank=True,
                                             help_text='h:mm -- <b>24-HOUR</b> time'                 )
    time_length       = models.DurationField('Time length',
                                             help_text='h:mm:ss')
    location          = models.IntegerField(                  default=1   , choices=L_LOCATION)
    verified          = models.BooleanField('Status'        , default=True, choices=L_VERIFIED, 
                                            help_text='If some aspect of event is unknown, set to "NOT verified."')
#   hide_loc          = models.BooleanField(default=False)  # ???
    group             = models.ForeignKey(Group, related_name='ev_type_group')
    url               = models.CharField('URL',
                                         max_length=100, default='www.sjaa.net')
    notes             = models.TextField('Notes',
                                         max_length=1000, blank=True)
    use               = models.BooleanField(default=True, choices=L_BOOLEAN,
                                            help_text='set to "false" if type is not longer needed')

    def __str__(self):
        return self.nickname


class Event(TimeStampedModel):
    class Meta:
        ordering = ['date_time']

    event_type  = models.ForeignKey(EventType, related_name='event_type', on_delete=models.CASCADE)
    nickname    = models.CharField('name', max_length=40)
    title       = models.CharField(max_length=40, blank=True,
                                   help_text='external name for event.  Leave blank if same as "nickname"')
    category    = models.CharField(max_length=2, default='pu', choices=L_CATEGORY)
    date_time   = models.DateTimeField(                                 null=True, blank=True,
                                   help_text='YYYY-MM-DD h:mm -- <b>24-HOUR</b>')
    time_length = models.DurationField(                                 null=True, blank=True,
                                   help_text='h:mm:ss')
    location    = models.IntegerField(default=1, choices=L_LOCATION   , null=True, blank=True)
    verified    = models.BooleanField('Status', choices=L_VERIFIED, default=True,
                                      help_text='If some aspect of event is unknown, set to "NOT verified."')
#   hide_loc    = models.BooleanField(initial=False)  # ???
    group       = models.ForeignKey(Group, related_name='ev_group', null=True)
    # owner == None means owner defaults to first group lead
    owner       = models.ForeignKey(User , related_name='owner'   , null=True, blank=True,
                                    help_text='If blank, owner defaults to group lead.')
    url         = models.CharField('URL',
                                   max_length=100, default='www.sjaa.net')
    notes       = models.TextField('Notes',
                                   max_length=1000, blank=True)
    cancelled   = models.BooleanField(default=False)
    #--- for planning ---#
    # 'draft' is true for all events generated immediately after generation
    draft       = models.BooleanField(default=True,
                                      help_text='Initally all events are draft.')
    # 'planned' is set to False for unplanned generated events.  event will be deleted after
    # draft events are committed.  Show planned=False as strike-through
    # not looked at if draft=False
    planned     = models.BooleanField(default=True,
                                      help_text='set to "false" if event is not planned')
    # set to True if time was changed.  Show date_chg=True as green
    # not looked at if draft=False
    date_chg    = models.BooleanField('Date changed', default=False,
                                      help_text='indicates date was changed from generated date')
    #--------------------#

    objects     = models.Manager()
    drafts      = EventDraftManager()

    def end_next_day(self):
        '''
        For HTML template -- return True when start date and end date differ
        '''
        date_start = self.date_time.date()
        date_end   = (self.date_time + self.time_length).date()
        return date_start != date_end

    def get_absolute_url(self):
        return reverse('ev_sched:event_detail',
                       args=[self.pk])
#                      args=[self.name,
#                            self.date.year,
#                            self.date.strftime('%m'),
#                            self.date.strftime('%d') ])

    def __str__(self):
        return self.nickname


'''
    # custom EventType/Event forms validation
    if repeat==EventRepeat.onetime and date              and start time or
       repeat==EventRepeat.monthly and week and weekday  and start time or
       repeat==EventRepeat.lunar   and lunar_phase       and (start time rule or start time) or
       repeat==EventRepeat.annual  and month and weekday and (week or lunar_phase)
    if rule_start_time and time_start and time_length

    if time_start and not time_length or not time_start and time_length
'''
