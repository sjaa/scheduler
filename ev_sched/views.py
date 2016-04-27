from operator import attrgetter

from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic  import ListView

from .models import Event
from ev_sched.cal_const  import locations
from ev_sched.gen_events import calc_start_time

# View: Events - draft for 'year'
def event_draft_list(request, year):
    events = Event.objects.filter(draft=True, date_time__year=year)
    return render(request,
                  'event/event_list.html',
                  {'events'    : events,
                   'year'      : year  ,
                   'draft'     : 'DRAFT',
                   'locations' : locations})

# View: Events - scheduled for 'year'
def event_list(request, year):
    events = Event.objects.filter(draft=False, planned=True, date_time__year=year)
    return render(request,
                  'event/event_list.html',
                  {'events'    : events,
                   'year'      : year  ,
                   'draft'     : '',
                   'locations' : locations})

class EventListView(ListView):
#   queryset = Event.published.all()
    context_object_name = 'events'
    template_name = 'ev_sched/event/list_view.html'

# View: event detail
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request,
                  'event/event_detail.html',
                  {'event'     : event,
                   'locations' : locations})

@register.filter
def location_to_txt(value, arg):
    return value[arg]

def event_date_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EventDateEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
# used in DBE
#           post_url = request.build_absolute_uri(post.get_absolute_rul())
            new_date = cd['new_date']
            submit   = cd['submit']
            if submit == 'New date':
                event.date_time = calc_start_time(new_date, event.event_type)
            elif submit == 'Week before':
                new_date = event.date_time - DAYS*7
            elif submit == 'Week after':
                new_date = event.date_time + DAYS*7
            event.save()
        else:
            form = EventDateEditForm()
        return render(request, 'event/event_date_edit.html',
                      {'event' : event,
                       'form'  : form  })


