import pdb
from django.shortcuts      import render
from django.http           import HttpResponseRedirect

from sched_core.const      import FMT_DATE_Y, FMT_HMP
from sched_core.config     import local_time_str, current_year, site_names
from sched_core.get_events import get_events
from .forms                import AnnSearchForm
from .config               import channel_name, channel_url_base, how_to_find_us
from .description          import gen_description



# display search form
def search(request, a=None, b=None):
    global current_year
    if request.method == 'POST':
        # create a form instance and populate with data from request:
        form = AnnSearchForm(request.POST)
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
                    '/sched_announce/period={}/ch={}/loc={}/event_type={}/'.
                    format(period,
                           channel,
                           location,
                           event_type))
    else:
        # a GET - create blank form
        form = AnnSearchForm()
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
        time      = None
        location  = None
        field1    = None
        field2    = None
        planned   = False

    end_time = event.date_time + event.time_length

    ann = announce_view()
    ann.name       = event.nickname
    ann.date       = local_time_str(event.date_time, FMT_DATE_Y)
    ann.time       = '{} - {}'.format(local_time_str(event.date_time, FMT_HMP),
                                      local_time_str(end_time       , FMT_HMP))
    ann.location   = site_names[event.location]
    channel = announce.channel
    if 'Meetup' in channel_name[channel]:
        # how to find us
        ann.field1 = how_to_find_us[event.location]
        # link to Meetup event
        ann.field2 = '<a href={uri}/{eid} target="_blank">{uri}/{eid}</a>'. \
                        format(uri=channel_url_base[channel],
                               eid=announce.event_api_id)
    ann.text       = gen_description(announce)
    ann.question   = announce.question_get()
    ann.rsvp_limit = announce.rsvp_limit_get()
    ann.notes      = announce.notes_get()
    return ann

def announce_details(request, period, channel, location, event_type):
    events, period = get_events(period, location, event_type)
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
    channel = int(channel)
    return render(request, 'announce/announce_detail.html',
                  {'channel'    : channel_name[channel],
                   'period'     : period,
                   'announces'  : anns})

