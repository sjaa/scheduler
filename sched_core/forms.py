from django import forms

from sched_core    .config import current_year, site_names
from sched_ev      .models import EventType, L_MONTH
from .test                 import TestModes
 

class SearchFormBase(forms.Form):
    class Meta:
        start_month = forms.ChoiceField (label='Starting month', choices=L_MONTH, initial=1)
        start_year  = forms.IntegerField(label='Starting year' , initial=current_year)
        end_month   = forms.ChoiceField (label='Ending month'  , choices=L_MONTH, initial=12)
        end_year    = forms.IntegerField(label='Ending year'   , initial=current_year)

class SearchForm(SearchFormBase):
    # choices for location
    LOCATION_CHOICES = [(0 , 'no location')]
    LOCATION_CHOICES.extend([(key, value)  for key, value in site_names.items()])
    location = forms.ChoiceField(choices=LOCATION_CHOICES)
    location.required = False
    # choices for event type
    EVENT_TYPE_CHOICES = [(0, 'no event type')]
    for event_type in EventType.objects.all():
        EVENT_TYPE_CHOICES.append((event_type.pk, event_type.nickname))
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES)
    event_type.required = False


L_TEST_MODES = []
for item in TestModes:
    s = item.name 
    L_TEST_MODES.append((item.value, s))

L_APPS = (
        ('mem', 'membership'),
        ('ann', 'announcements')
)

L_ADVANCE = (
        ('1day', '1 day'),
        ('next', 'next day with tasks')
)


class TestForm(forms.Form):
    date_start   = forms.DateField(label='start date'  )
    date_end     = forms.DateField(label='end date'    )
    # TODO: hidden
    date_current = forms.DateField(label='current date')
    app = forms.ChoiceField(choices=L_APPS)
    test_modes   = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=L_TEST_MODES)
    advance_mode = forms.ChoiceField(choices=L_ADVANCE)

'''

class TestForm(forms.Form):
    today = datetime.datetime.today()
    date_start   = forms.DateField(label='start date'   , initial=today)
    date_end     = forms.DateField(label='end date'     , initial=today)
    # TODO: hidden
    date_current = forms.DateField(label='current date' , initial=today)
    test_modes   = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=L_TEST_MODES)
    app = forms.ChoiceField(choices=L_APPS)

from sched_core.lib import set_current_date
    set_current_date(date_current)

    while current_date <= date_end:
        # membership
        if APPS.membership in apps_to_test:
            ran_job = cron_job_membership()
            if step_day or step_next_job and ran_job:
                break
        # announce
        inc_current_date()

'''
