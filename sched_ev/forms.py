'''
from django import forms

class EventDateChangeForm(forms.Form):
    
'''

'''
from
    https://docs.djangoproject.com/en/1.8/topics/forms/modelforms/
'''

from django.forms import ModelForm
from myapp.models import Article

L_CHANGE_WEEK = (
        (''   : 'no change'),
        ('+1' : 'week before'),
        ('-1' : 'week after' )
)

# Create the form class.
class DraftEventsForm(ModelForm):
    class Meta:
        model = Article
        fields = ['event_type', 'title', 'date_time', 'planned', 'date_chg']

    change_week = CharField(max_length=2, default='', choices=L_CHANGE_WEEK)
    new_date    = DateField(null=True, blank=True)

'''
move next to model.py?
'''

draft_events_formset = DraftEventsSet(queryset=Events.drafts)

from django.forms import modelformset_factory
from django.shortcuts import render_to_response
from myapp.models import Author
from sched_ev.cal_const import DAY

def clean(??):
    if new_date and change_week:
        raise exception

from sched_ev.gen_events import calc_start_time

#def draft_events_change(request):
def DraftEventsView(request):
    DraftEventFormSet = modelformset_factory(Event, form=DraftEventsForm)
    if request.method == 'POST':
#       formset = DraftEventFormSet(request.POST, request.FILES)
        formset = DraftEventFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.change_week or form.new_date:
                    if form.change_week=='-1':
                        form.date_time -= DAY*7
                    elif form.change_week=='+1':
                        form.date_time += DAY*7
                    elif form.new_date:
                        form.date_time = form.new_date
                    time_start = calc_start_time(form.date_time, form.event_type)
                    form.date_time = datetime.datetime.combine(date_time, time_start)
                    form.date_chg = True
            formset.save()
            # do something.
    else:
        formset = AuthorFormSet()
    return render_to_response("manage_authors.html", {
        "formset": formset,
    })
