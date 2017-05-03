from django import forms

from sched_core    .config import current_year, site_names
from sched_ev      .models import EventType, L_MONTH
 

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
