import pdb

from django.shortcuts import render
from django.http      import HttpResponseRedirect
from django.db.models import Q

from .forms import SearchForm

from sched_core.config          import local_time_str, current_year
from sched_core.const           import FMT_DATE_Y
from sched_ev.models            import Event
from sched_announce.description import gen_description

def search(request):
    global current_year
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        form = SearchForm(request.POST)
        if form.is_valid():
            year       =     form.cleaned_data['year'      ]
            location   = int(form.cleaned_data['location'  ])
            event_type = int(form.cleaned_data['event_type'])
            channel    = int(form.cleaned_data['channel'   ])
            # update 'current_year' for this session
            if year != current_year:
                current_year = year
            return HttpResponseRedirect(
                    '/sched_announce/{}/channel={}/location={}/event_type={}/'.
                    format(year,
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
    ann.name     = event.nickname
    ann.date     = local_time_str(event.date_time, FMT_DATE_Y)
    ann.time     = '{} - {}'.format(local_time_str(event.date_time, FMT_HMP),
                                    local_time_str(end_time       , FMT_HMP))
    ann.location = site_names[event.location]
    ann.text     = gen_description(announce.text)
    ann.notes    = announce.notes
    return ann


def announce_details(request, year, channel, location, event_type):
    # get events by year, location, event type
    q = Q(date_time__year=int(year)) & Q(planned=True)
    if location != '0':
        q &= Q(location=int(location))
    elif event_type != '0':
        q &= Q(event_type=int(event_type))
    events = Event.objects.filter(q).order_by('date_time')
    anns = []
#   pdb.set_trace()
    return
    # retrieve event announcements with 'channel'
    for event in events:
        ann = event.announce_event.filter(channel=int(channel))
        if len(ann) >= 1:
            # generate details from announcement/event for display
            anns.append(gen_announce_detail(ann, event))
            if len(ann) > 1:
                # TODO: fix error reporting
                print('error')
    return render(request, 'announce/announce_detail.html',
                  {'year'      : year     ,
                   'announces' : anns      })

