from operator import attrgetter

from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdb
from django.views.generic  import ListView

from .models import Event
from sched_ev.cal_const  import *
from sched_ev.cal_ephemeris import calc_date_ephem


def new_view(events):
    class event_view():
        name      = None
        draft     = None
        location  = None
        date_time = None
        sunset    = None
        moon      = None
        planned   = False

    evs = []
    for event in events:
        if event.event_type.rule_start_time == RuleStartTime.absolute.value:
            # show events scheduled only relative to sunset/twilight
            continue
        site = sites[event.location]
        ev = event_view()
#       ev.name      = event.title if event.title else event.nickname
        ev.name      = event.nickname
        ev.draft     = 'y' if event.draft else ''
        ev.location  = site_names[event.location]
        ev.date_time = event.date_time
        sunset, moon = calc_date_ephem(event.date_time, event.location)
        ev.sunset    = '{t[0]} - {t[1]} / {t[2]} / {t[3]}'.format(t=sunset)
        ev.moon      = '{t[0]} {t[1]} - {t[2]}'.format(t=moon)
        ev.planned   = event.planned
        evs.append(ev)
    return evs


# View: Events - draft for 'year'
def event_draft_list(request, year):
    events = Event.objects.filter(date_time__year=year)
    return render(request,
                  'event/event_list.html',
                  {'events'    : events,
                   'year'      : year  ,
                   'draft'     : 'DRAFT:',
                   'categories': event_category,
                   'locations' : site_names})

# View: Events - scheduled for 'year'
def event_list(request, year):
    events = Event.objects.filter(draft=False, planned=True,
                                  date_time__year=year)\
                          .order_by('date_time')
    return render(request,
                  'event/event_list.html',
                  {'events'    : events,
                   'year'      : year  ,
                   'draft'     : '',
                   'categories': event_category,
                   'locations' : site_names})

# View: Ephem - scheduled for 'year'
def event_ephem_draft_list(request, year):
    # TODO: year is for UTC
    events = Event.objects.filter(date_time__year=int(year))\
                          .order_by('title', 'date_time')
    evs = new_view(events)
    return render(request,
                  'event/ephem_list.html',
                  {'events'    : evs,
                   'draft'     : 'DRAFTS:',
                   'year'      : year   })

# View: Ephem - scheduled for 'year'
def event_ephem_type_draft_list(request, year, eventtype):
    # TODO: year is for UTC
    events = Event.objects.filter(date_time__year=int(year),
                                  event_type=eventtype)\
                          .order_by('date_time')
    evs = new_view(events)
    return render(request,
                  'event/ephem_list.html',
                  {'events'    : evs,
                   'draft'     : 'DRAFTS:',
                   'year'      : year   })

# View: Ephem - scheduled for 'year'
def event_ephem_list(request, year):
    # TODO: year is for UTC
    events = Event.objects.filter(draft=False, planned=True,
                                  date_time__year=int(year))\
                          .order_by('title', 'date_time')
    evs = new_view(events)
    return render(request,
                  'event/ephem_list.html',
                  {'events'    : evs,
                   'draft'     : '',
                   'year'      : year   })

# View: Ephem - scheduled for 'year'
def event_ephem_type_list(request, year, eventtype):
    # TODO: year is for UTC
    events = Event.objects.filter(draft=False, planned=True,
                                  date_time__year=int(year),
                                  event_type=eventtype)\
                          .order_by('date_time')
    evs = new_view(events)
    return render(request,
                  'event/ephem_list.html',
                  {'events'    : evs,
                   'draft'     : '',
                   'year'      : year   })

class EventListView(ListView):
#   queryset = Event.published.all()
    context_object_name = 'events'
    template_name = 'sched_ev/event/list_view.html'

# View: event detail
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request,
                  'event/event_detail.html',
                  {'event'     : event,
                   'locations' : site_names})

@register.filter
def dict_lookup(value, arg):
    # 'arg' must be string
    return value[arg]

@register.filter
def subtract(a, b):
    return a - b

@register.filter
def end_next_day(event):
    date_time_end = event.date_time + event.time_length

    date_start    = event.date_time.astimezone(TZ_LOCAL).date()
    date_end      = date_time_end  .astimezone(TZ_LOCAL).date()
    return date_start != date_end

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


# View: Ephem - scheduled for 'year'
def test_ephem_list(request, year):
    # TODO: year is for UTC
    events = Event.objects.filter(draft=False, planned=True,
                                  date_time__year=int(year))\
                          .order_by('date_time')
    evs = new_view(events)
    return render(request,
                  'event/test_ephem_list.html',
                  {'events'    : evs,
                   'draft'     : '',
                   'year'      : year   })


# View: Events - scheduled for 'year'
def test_list(request, year):
    events = Event.objects.filter(draft=False, planned=True,
                                  date_time__year=year)\
                          .order_by('date_time')
    return render(request,
                  'event/test_list.html',
                  {'events'    : events,
                   'year'      : year  ,
                   'draft'     : '',
                   'categories': event_category})
