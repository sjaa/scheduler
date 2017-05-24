import pdb
from   django.http                 import HttpResponseRedirect
from   django.shortcuts            import render, get_object_or_404
from   django.template.defaulttags import register
from   django.utils.safestring     import mark_safe
#from   django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from   django.views.generic        import ListView

from   sched_core.const            import *
#from   sched_core.config           import site_names, current_year, local_time, \
#                                          default_date_start, default_date_end
from   sched_core.config           import site_names, current_year, local_time, local_time_now
from   sched_core.forms            import SearchForm
from   sched_core.get_events       import get_events
from   .models                     import Event, AuxEvent
from   .cal_ephemeris              import calc_date_ephem
from   sched_ev                    import gen
from   .forms                      import EventGenForm

'''
list all approved, planned
    event_list
        http://127.0.0.1:8001/sched_ev/events/2017/

list all outdoor events w/ ephemeris
    event_ephem_list
        http://127.0.0.1:8001/sched_ev/events_ephem/2017/
'''

default_date_start = local_time_now()
default_date_end   = local_time_now()

# display search form
def search(request):
    global current_year
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        form = SearchForm(request.POST)
        if form.is_valid():
            start_month = int(form.cleaned_data['start_month'])
            start_year  =     form.cleaned_data['start_year' ]
            end_month   = int(form.cleaned_data['end_month'  ])
            end_year    =     form.cleaned_data['end_year'   ]
            location    = int(form.cleaned_data['location'   ])
            event_type  = int(form.cleaned_data['event_type' ])
            period = '{}{:02}-{}{:02}'.format(start_year, start_month,
                                              end_year  , end_month)
            # update 'current_year' for this session
            if start_year != current_year:
                current_year = year
            return HttpResponseRedirect(
                    '/sched_ev/period={}/loc={}/event_type={}/'.
                    format(period,
                           location,
                           event_type))
    else:
        # a GET - create blank form
        form = SearchForm()
    return render(request, 'event/event_search.html',
                  {'form'  : form,
                   'title' : 'Event Search',
                   'action': 'search'})

'''
# display search form
def set_gen_period(request):
    global default_date_start
    global default_date_end

#   pdb.set_trace()
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        form = EventGenForm(request.POST)
        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_end   = form.cleaned_data['date_end'  ]
            if date_start<=date_end:
                default_date_start = date_start
                default_date_end   = date_end
#               request.session['default_date_start'] = date_start
#               request.session['default_date_end'  ] = date_end
    else:
        # a GET - create blank form
        form = EventGenForm(initial={'date_start' : default_date_start,
                                     'date_end'   : default_date_end})
    return render(request, 'event/set_gen_period.html',
                  {'form'  : form,
                   'title' : 'Event Generation Period',
                   'action': 'set_gen_period'})


def gen_events(request, event_types):
    if request.method == 'POST':
#       start = request.session['default_date_start']
#       end   = request.session['default_date_end'  ]
        start = default_date_start
        end   = default_date_end
        print('start/end: {} / {}'.format(start, end))
        new_events, conflicts = gen.gen_events(start, end, event_types)
        events = conflicts if conflicts else new_events
        period = '{} - {}'.format(start.strftime(FMT_YDATE),
                                  end  .strftime(FMT_YDATE))
#       pdb.set_trace()
        return render(request, 'event/event_new.html',
                      {'events'   : events,
                       'period'   : period,
                       'conflicts': conflicts!=None,
                       'events'   : conflicts})
    else:
        # a GET - create blank form
        form = EventGenForm(initial={'start'   : default_date_start,
                                     'end'     : default_date_end})
#       form = EventGenForm(initial={'start'   : request.session['default_date_start'],
#                                    'end'     : request.session['default_date_end'  ]})
    return render(request, 'event/event_search.html', {'form': form})
'''


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
#   pdb.set_trace()
    for event in events:
        if event.event_type.rule_start_time == RuleStartTime.absolute.value:
            # show events scheduled only relative to sunset/twilight
            continue
#       site = sites[event.location]
        ev = event_view()
        ev.name      = event.nickname
        ev.draft     = 'y' if event.draft else ''
        ev.location  = site_names[event.location]
        ev.date_time = event.date_time
        sunset, moon = calc_date_ephem(event.date_time, event.location)
        ev.sunset    = '{t[0]} - {t[1]} / {t[2]} / {t[3]}'.format(t=sunset)
        ev.moon      = '{t[0]} {t[1]} - {t[2]:>2}%'.format(t=moon)
        ev.planned   = event.planned
        evs.append(ev)
    return evs


def aux_view(events):
    class event_view():
        name      = None
        date      = None

    evs = []
#   pdb.set_trace()
    for event in events:
        ev = event_view()
        ev.name      = event.title
        ev.date      = event.date
        evs.append(ev)
    return evs


# View: Events - draft for 'year'
def event_draft_list(request, year, order):
    if order == '':
        events = Event.objects.filter(date_time__year=year)\
                              .order_by('date_time')
    else:
        events = Event.objects.filter(date_time__year=year)\
                              .order_by('title', 'date_time')
#   pdb.set_trace()
    return render(request,
                  'event/event_list.html',
                  {'events'    : events,
                   'year'      : year  ,
                   'draft'     : 'DRAFT:',
                   'categories': event_category,
                   'locations' : site_names})

# View: Ephem - scheduled for 'year'
def event_ephem_draft_list(request, year, order):
    # TODO: year is for UTC
    if order == '':
        events = Event.objects.filter(date_time__year=year)\
                              .order_by('date_time')
    else:
        events = Event.objects.filter(date_time__year=year)\
                              .order_by('title', 'date_time')
#   pdb.set_trace()
    evs = new_view(events)
    return render(request,
                  'event/ephem_list.html',
                  {'events'    : evs,
                   'draft'     : 'DRAFT:',
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
                   'draft'     : 'DRAFT:',
                   'year'      : year   })

# View: Ephem - scheduled for 'year'
def event_ephem_list(request, year, order):
    # TODO: year is for UTC
    if order == '':
        events = Event.objects.filter(draft=False, planned=True,
                                      date_time__year=int(year))\
                              .order_by('date_time')
    else:
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
#   pdb.set_trace()
    return render(request,
                  'event/event_detail.html',
                  {'event'     : event,
                   'locations' : site_names})

# View: Aux events for 'year'
def aux_event_list(request, year, order):
    # TODO: year is for UTC
    events = AuxEvent.objects.filter(date__year=int(year)).order_by('date')
    evs = aux_view(events)
    return render(request,
                  'event/aux_event_list.html',
                  {'events'    : evs,
                   'year'      : year   })

@register.filter
def dict_lookup(value, arg):
    # 'arg' must be string
    return value[arg]

@register.filter
def subtract(a, b):
    return a - b

@register.filter()
def nbsp(value):
    return mark_safe("&nbsp;".join(value.split(' ')))

@register.filter
def end_next_day(event):
    date_time_end = event.date_time + event.time_length

    date_start = local_time(event.date_time).date()
    date_end   = local_time(date_time_end  ).date()
    days = (date_end - date_start).days
    if days == 0:
        return ''
    else:
        return '(+{})'.format(days)

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
                new_date = event.date_time - DAY*7
            elif submit == 'Week after':
                new_date = event.date_time + DAY*7
            event.save()
        else:
            form = EventDateEditForm()
        return render(request, 'event/event_date_edit.html',
                      {'event' : event,
                       'form'  : form  })


############################
# Cancel event
#
def event_cancel_list(request):
    user = request.user
    groups = get_coordinator_groups(user)
    events = Event.objects.filter(Q(group__in=coordinator) | Q(owner=user.pk),
                                  date_time__gte=datetime.datetime.now())\
                          .order_by('date_time')
    return render(request,
                  'event/event_cancel_list.html',
                  {'events'    : events,
                   'locations' : site_names})


def event_cancel(request, event_id):
    user = request.user
    groups = get_coordinator_groups(user)
    event  = Event.objects.get(pk=event_id)
    have_permission = user.pk == event.owner or event.group in groups
    return render(request,
                  'event/event_cancel.html',
                  {'event'      : event,
                   'locations'  : site_names,
                   'permission' : have_permission})


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

def event_list(request, period, location, event_type):
    events, period = get_events(period, location, event_type)
    return render(request,
                  'event/event_list.html',
                  {'events'    : events,
                   'period'    : period,
                   'draft'     : '',
                   'categories': event_category,
                   'locations' : site_names})
