from django.contrib.auth.models import User, Group
from django.core.urlresolvers   import reverse
from django.core.exceptions     import ValidationError
from django.db                  import models
from django.core.validators     import MinValueValidator, MaxValueValidator
from django.utils.translation   import ugettext_lazy as _

from sched_core.models          import TimeStampedModel
from sched_core.const           import L_BOOLEAN, HOUR
from sched_core.config          import EventCategory
from sched_ev  .const           import *


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

# choices for models, need to be in sets
L_AUX_EVENT   = []
L_CATEGORY    = []
L_REPEAT      = []
L_LUNAR_PHASE = []
L_WEEK        = []
L_WEEKDAY     = []
L_STARTTIME   = []
L_LOCATION    = []

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

L_VERIFIED = (
        (True , 'verified'),
        (False, 'NOT verified'),
)


# create choices from class Enum objects
lists = (
         (AuxCategory    , None         , L_AUX_EVENT  ),
         (EventCategory  , None         , L_CATEGORY   ),
         (EventRepeat    , event_repeat , L_REPEAT     ),
         (RuleLunar      , rule_lunar   , L_LUNAR_PHASE),
         (RuleWeek       , rule_week    , L_WEEK       ),
         (RuleWeekday    , rule_weekday , L_WEEKDAY    ),
         (RuleStartTime  , None         , L_STARTTIME  )
)

for l in lists:
    rule, rule_string, l_choice = l
    for item in rule:
        if rule_string:
            s = rule_string[item]
        else:
            s = item.name 
        l_choice.append((item.value, s))

# treat 'locations' differently since it's a dict, not class Enum
for key, value in site_names.items():
    L_LOCATION.append((key, value))


#####################################
# For astronomical events, holidays #
#####################################
class AuxEvent(models.Model):
    title             = models.CharField(max_length=40)
    category          = models.CharField(max_length=2, choices=L_AUX_EVENT)
    date              = models.DateField()
    notes             = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.title


#######################
# For event templates #
#######################
class EventType(TimeStampedModel):
    class Meta:
        ordering = ['nickname']

    nickname          = models.CharField    ('Type', max_length=40, unique=True,
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
    neg_start_offset  = models.BooleanField ('Negative start offset', default=False, choices=L_BOOLEAN,
                                             help_text='set to "true" if <b>Start time offset</b> is negative')
    time_earliest     = models.TimeField    ('Earliest start time',
                                                                                                null=True, blank=True,
                                             help_text='h:mm -- <b>24-HOUR</b> time'                 )
    time_length       = models.DurationField('Time length',                                     null=True, blank=True,
                                             help_text='h:mm:ss')
    time_setup        = models.DurationField('Setup time', default=HOUR,
                                             help_text='h:mm:ss - Time for setup required before event')
    time_teardown     = models.DurationField('Teardown time', default=HOUR,
                                             help_text='h:mm:ss - Time for tear down required after event')
    location          = models.IntegerField (                  default=1   , choices=L_LOCATION)
    verified          = models.BooleanField ('Status'        , default=True, choices=L_VERIFIED, 
                                            help_text='If some aspect of event is unknown, set to "NOT verified."')
#   hide_loc          = models.BooleanField(default=False)  # ???
    group             = models.ForeignKey   (Group, related_name='ev_type_group')
    url               = models.URLField     ('URL',
                                         max_length=100, default='www.sjaa.net', blank=True)
    notes             = models.TextField    ('Notes',
                                         max_length=1000, blank=True)
    use               = models.BooleanField (default=True, choices=L_BOOLEAN,
                                            help_text='set to "false" if type is not longer needed')

    def clean(self):
        '''
        note: week and lunar_phase can be zero, so a test for a null field must be explicit:
            self.week!=none
        '''

        d = {}
        # by repeat
#       if (self.repeat in (EventRepeat.onetime.value, EventRepeat.annual.value)) \
        if (self.repeat == EventRepeat.annual.value) \
           and not (self.date or self.month and \
                    (self.week!=None or self.lunar_phase) and self.weekday):
            s = 'if "Repeat" is "one-time" or "annual", ' + \
                '"Date" or "Month", "Week", and "Weekday" are required'
            d['repeat'] = _(s)
        if self.repeat == EventRepeat.monthly.value and \
           not (self.week!=None and self.weekday):
            d['repeat'] = _('if "Repeat" is "month", "Week" and "Weekday" are required')
        if self.repeat == EventRepeat.monthly.value and self.lunar_phase!=None:
            d['lunar_phase'] = _('must be blank if "Repeat" is "monthly"')
        if self.repeat == EventRepeat.lunar.value and not self.weekday:
            d['weekday'] = _('required if "Repeat" is "lunar"')
        if self.repeat == EventRepeat.lunar.value and self.lunar_phase==None:
            d['lunar_phase'] = _('required if "Repeat" is "lunar"')
        # by week
        if self.week!=None and not self.weekday:
            d['weekday'] = _('required if "Week" is specified')
        # by start time
        if not (self.rule_start_time or self.start_time):
            d['rule_start_time'] = 'Need "Start time rule" or "Start time"'
            d['time_start'     ] = 'Need "Start time rule" or "Start time"'
        if self.rule_start_time == RuleStartTime.absolute.value and \
           self.repeat != EventRepeat.onetime.value and \
           not self.time_start:
            d['time_start'] = 'required if "Start time rule" is "absolute"'
        if self.time_start_offset and \
           self.rule_start_time == RuleStartTime.absolute.value:
            s = 'must be blank if "Rule start time" is "absolute"'
            d['time_start_offset'] = _(s)
        if self.time_earliest     and \
           self.rule_start_time == RuleStartTime.absolute.value:
            s = 'must be blank if "Rule start time" is "absolute"'
            d['time_earliest'] = _(s) 
        if self.category != EventCategory.external.value and not self.group:
            s = 'group required for non-external events'
            d['group'] = _(s) 
        if self.category != EventCategory.external.value and not self.url:
            s = 'URL required for non-external events'
            d['url'] = _(s) 
#       if not ((self.time_start or self.rule_start_time) and self.time_length):
#           d['time_length'] = _('required if if "Start time" or "Start time rule" is specified')

#           'time_start': _('"Time length" required if "Start time" or "Start time rule" is specified'),
#           'rule_start_time': _('"Time length" required if "Start time" or "Start time rule" is specified')
        if len(d) > 0:
            raise ValidationError(d)
    #   print(1, self.title)
#       return err_msg

    def __str__(self):
        return self.nickname


##############
# For events #
##############
class Event(TimeStampedModel):
#   def get_actions(self, request):
#       actions = super(MyModelAdmin, self).get_actions(request)
#       del actions['delete_selected']
#       return actions

    event_type    = models.ForeignKey   (EventType, related_name='event_type', on_delete=models.CASCADE)
    nickname      = models.CharField    ('name', max_length=40)
    title         = models.CharField    (max_length=40, blank=True,
                                         help_text='external name for event.  Leave blank if same as "nickname"')
    category      = models.CharField    (max_length=2, choices=L_CATEGORY)
    date_time     = models.DateTimeField(                                 null=True, blank=True,
                                         help_text='YYYY-MM-DD h:mm -- <b>24-HOUR</b>')
    time_length   = models.DurationField(                                 null=True, blank=True,
                                         help_text='h:mm:ss')
    time_setup    = models.DurationField('Setup time', default=HOUR,
                                         help_text='h:mm:ss - Time for setup required before event')
    time_teardown = models.DurationField('Teardown time', default=HOUR,
                                         help_text='h:mm:ss - Time for tear down required after event')
    location      = models.IntegerField (choices=L_LOCATION, null=True, blank=True)
    verified      = models.BooleanField ('Status', choices=L_VERIFIED,
                                         help_text='If some aspect of event is unknown, set to "NOT verified."')
#   hide_loc      = models.BooleanField (initial=False)  # ???
    group         = models.ForeignKey   (Group, related_name='ev_group', null=True)
    owner         = models.ForeignKey   (User , related_name='owner'   , null=True, blank=True,
                                         help_text='If blank, owner defaults to group lead.')
    url           = models.URLField     ('URL', max_length=100)
    notes         = models.TextField    ('Notes',
                                         max_length=1000, blank=True)
    cancelled   = models.BooleanField (default=False)
    #--- for planning ---#
    # 'draft' is true for all events generated immediately after generation
    draft       = models.BooleanField (default=True, help_text='Initally all events are draft.')
    # 'planned' is set to False for unplanned generated events.  event will be deleted after
    # draft events are committed.  Show planned=False as strike-through
    # not looked at if draft=False
    planned     = models.BooleanField (default=True,
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

    def name(self):
        return self.nickname if not self.title else title

    def get_absolute_url(self):
        return reverse('sched_ev:event_detail',
                       args=[self.pk])
#                      args=[self.name,
#                            self.date.year,
#                            self.date.strftime('%m'),
#                            self.date.strftime('%d') ])

    def __str__(self):
        return self.nickname
