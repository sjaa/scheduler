from django import forms

from sched_core.config import current_year, site_names
from sched_core.forms  import SearchForm
from sched_ev  .models import EventType, L_MONTH
from .config           import channel_name, DEFAULT_CHANNEL
 

class AnnSearchForm(SearchForm):
    # choices for channel
    CHANNEL_CHOICES = []
    for channel_pk, channel_str in channel_name.items():
        CHANNEL_CHOICES.append((channel_pk, channel_str))
    channel = forms.ChoiceField(choices=CHANNEL_CHOICES, initial=DEFAULT_CHANNEL)
