from django import forms

from sched_core    .config import current_year, site_names
from sched_ev      .models import EventType, L_MONTH
from .config               import channel_name, DEFAULT_CHANNEL
 

class SearchForm(forms.Form):
    start_month = forms.ChoiceField (label='Starting month', choices=L_MONTH, initial=1)
    start_year  = forms.IntegerField(label='Starting year' , initial=current_year)
    end_month   = forms.ChoiceField (label='Ending month'  , choices=L_MONTH, initial=12)
    end_year    = forms.IntegerField(label='Ending year'   , initial=current_year)
       
    # choices for location
    LOCATION_CHOICES = [(0 , 'no location')]
    LOCATION_CHOICES.extend([(key, value)  for key, value in site_names.items()])
#   location = forms.IntegerField(choices=LOCATION_CHOICES)
    location = forms.ChoiceField(choices=LOCATION_CHOICES)
    location.required = False
    # choices for event type
    EVENT_TYPE_CHOICES = [(0, 'no event type')]
    for event_type in EventType.objects.all():
        EVENT_TYPE_CHOICES.append((event_type.pk, event_type.nickname))
#   event_type = forms.IntegerField(choices=EVENT_TYPE_CHOICES)
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES)
    event_type.required = False
    # choices for channel
    CHANNEL_CHOICES = []
    for channel_pk, channel_str in channel_name.items():
        CHANNEL_CHOICES.append((channel_pk, channel_str))
#   channel = forms.IntegerField(choices=CHANNEL_CHOICES)
    channel = forms.ChoiceField(choices=CHANNEL_CHOICES, initial=DEFAULT_CHANNEL)
