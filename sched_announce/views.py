import pdb
import datetime

from django.shortcuts import render
from django.http      import HttpResponseRedirect
from django.db.models import Q

from .forms import SearchForm
from sched_core.config          import TZ_LOCAL, local_time_str, end_of_month, \
                                       current_year, site_names
from sched_core.const           import FMT_DATE_Y, FMT_HMP
from sched_ev.models            import Event, L_MONTH
from sched_announce.const       import channel_name
from sched_announce.description import gen_description



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
            channel     = int(form.cleaned_data['channel'    ])
            period = '{}{:02}-{}{:02}'.format(start_year, start_month,
                                              end_year  , end_month)
            # update 'current_year' for this session
            if start_year != current_year:
                current_year = year
            return HttpResponseRedirect(
                    '/sched_announce/{}/ch={}/loc={}/event_type={}/'.
                    format(period,
                           channel,
                           location,
                           event_type))
    else:
        # a GET - create blank form
        form = SearchForm()
    return render(request, 'announce/announce_search.html', {'form': form})


def new_view(announces):
    class announce_view():
        date      = None
        name      = None
        location  = None
        time      = None
        planned   = False

    anns = []
#   pdb.set_trace()
    for announce in announces:
        event    = announce.event
        end_time = event.date_time + event.time_length
        ann = announce_view()
        ann.name     = event.nickname
        ann.date     = local_time_str(event.date_time, FMT_DATE_Y)
        ann.time     = '{} - {}'.format(local_time_str(event.date_time, FMT_HMP),
                                        local_time_str(end_time       , FMT_HMP))
        ann.location = site_names[event.location]
        ann.text     = gen_description(announce.text)
        ann.notes    = announce.notes
        anns.append(ann)
    return anns


def gen_announce_detail(announce, event):
    class announce_view():
        date      = None
        name      = None
        location  = None
        time      = None
        planned   = False

    end_time = event.date_time + event.time_length

    ann = announce_view()
    ann.name       = event.nickname
    ann.date       = local_time_str(event.date_time, FMT_DATE_Y)
    ann.time       = '{} - {}'.format(local_time_str(event.date_time, FMT_HMP),
                                      local_time_str(end_time       , FMT_HMP))
    ann.location   = site_names[event.location]
    ann.text       = gen_description(announce)
    ann.question   = announce.question_get()
    ann.rsvp_limit = announce.rsvp_limit_get()
    ann.notes      = announce.notes_get()
    return ann


def announce_details(request, period, channel, location, event_type):
    # get starting date
    start_year  = int(period[ 0: 4])
    start_month = int(period[ 4: 6])
    start = TZ_LOCAL.localize(datetime.datetime(start_year, start_month, 1))
    # get ending date, just before midnight
    end_year    = int(period[ 7:11])
    end_month   = int(period[11:13])
    # get last day in month - monthrange returns (first day, last day)
#   last_day_in_month = calendar.monthrange(end_year, end_month)[1]
    end   = TZ_LOCAL.localize(end_of_month(end_year, end_month))
    channel = int(channel)
    q = Q(date_time__gte=start) & Q(date_time__lte=end) & Q(planned=True)
    if location != '0':
        location = int(location)
        q &= Q(location=location)
    if event_type != '0':
        event_type = int(event_type)
        q &= Q(event_type=int(event_type))
    events = Event.objects.filter(q).order_by('date_time')
    anns = []
    # retrieve event announcements with 'channel'
    for event in events:
        ann = event.announce_event.filter(channel=channel)
        if len(ann) >= 1:
            # generate details from announcement/event for display
            anns.append(gen_announce_detail(ann[0], event))
            if len(ann) > 1:
                # TODO: fix error reporting
                print('error')
    period = '{} {} - {} {}'.format(L_MONTH[start_month-1][1], start_year,
                                    L_MONTH[end_month  -1][1], end_year)
    return render(request, 'announce/announce_detail.html',
                  {'channel'   : channel_name[channel],
                   'period'    : period,
                   'announces' : anns})

