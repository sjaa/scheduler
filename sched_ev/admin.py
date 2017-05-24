import pdb
import datetime
from   django.contrib        import admin
from   sched_core.sched_log  import sched_log
from   sched_core.const      import DAY
from   sched_core.config     import TZ_LOCAL
from   sched_core.filters    import AdminDateTimeYearFilter
from   sched_ev.gen          import foo, calc_start_time
import sched_announce.gen  
from   .models               import AuxEvent, EventType, Event
#from   .views                import gen_events


# For AuxEvent
class PostAuxEvent(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'notes')
    list_filter = ('category',)
    search_fields = ['title']
    ordering = ('date',)
#   actions = [event_type_copy, event_gen]


###############
# For EventType
###############
def event_gen(modeladmin, request, queryset):
#   pdb.set_trace()
#   foo(request, queryset)
    foo(queryset)
#   return HttpResponseRedirect('/sched_ev/gen_events_period')
event_gen.short_description = "Generate events from selected templates"

def event_type_copy(modeladmin, request, queryset):
    for event_type in queryset:
        new_event_type = event_type
        new_event_type.pk = None
        new_event_type.nickname += ' (Copy)'
        new_event_type.save()
event_type_copy.short_description = "Copy templates from selected templates"

class PostEventType(admin.ModelAdmin):
    list_display = ('nickname', 'category', 'verified', 'location', 'repeat',
                    'lunar_phase', 'month', 'weekday', 'rule_start_time', 'time_start',
                    'time_start_offset', 'notes')
    list_filter = ('repeat', 'category', 'location', 'lunar_phase', 'verified')
    search_fields = ['nickname']
    ordering = ('nickname',)
#   fields += ('verified',)
    fields = ('nickname', 'title', 'category', 'verified',
              'location',
              ('repeat', 'lunar_phase'),
              'date',
              ('month', 'week', 'weekday'),
              ('rule_start_time', 'time_start', 'time_length'),
              ('time_start_offset', 'neg_start_offset', 'time_earliest'),
              ('time_setup', 'time_teardown'),
              'group', 'owner_title', 'url', 'notes', 'use')
    actions = [event_type_copy, event_gen]


###########
# For Event
###########
def event_draft_set_planned(modeladmin, request, queryset):
    for event in queryset:
        if event.draft and not event.planned:
            event.planned = True
            event.save()
event_draft_set_planned.short_description = "Make selected events planned"

def event_draft_remove_planned(modeladmin, request, queryset):
    for event in queryset:
        if event.draft and event.planned:
            event.planned = False
            event.save()
event_draft_remove_planned.short_description = "Make selected events unplanned"

def find_draft_event_conflicts(events):
    '''
    Detect scheduling conflicts between events at the same location.
    Assume accepted events don't have conflicts.
    'events' already sorted by date/time.

    Return
        set of draft events that conflict with other events
    '''
    # for each event, check all events that start at the same time or after
#   pdb.set_trace()
    events_copy = events[1:]
    conflict_set = set()
    # compare times for every pair of events
    for ev1 in events[:-1]:
        if not ev1.planned:
            # ev1 is not planned, no need to evaluate
            continue
        ev1_end = ev1.date_time + ev1.time_length
        for ev2 in events_copy:
            if not ev2.planned:
                # ev2 is not planned, no need to evaluate
                continue
            if ev1_end > ev2.date_time:
                # ev1 ends after start of ev2
                # if there's a conflict and the event is draft,
                #   add event for later removal
                if ev1.draft:
                    conflict_set.add(ev1)
                if ev2.draft:
                    conflict_set.add(ev2)
                sched_log.error('draft event time conflict "{}" / "{}"  --  {}'.
                     format(ev1.title, ev2l.title, local_time(event.date_time)))
            if ev1_end <= ev2.date_time:
                # ev1 ends before ev2 starts
                #  -> all events sorted by time.  no need to check rest
                #     of events_copy
                break
        events_copy.pop(0)
    return conflict_set


def before_now(date_time):
    # check if 'date_time' is before current time
    # TODO: during test return False
    return False


def event_draft_accept(modeladmin, request, queryset):
    '''
    Detect scheduling conflicts among events at the same location.
    For each location, detect time overlap of events.
      -> If a draft event overlaps another event, don't unset 'draft'.

    Assume accepted events don't have conflicts.
    'queryset' should be events with 'draft' set
    '''
    # Get all events between first and last draft events.
    # To account for multi-day events, set range for 7 days before
    # first draft event to 7 days after last draft event
    date_start = queryset[0].date_time - datetime.timedelta(days=7)
    date_end   = queryset[0].date_time + datetime.timedelta(days=7)
    events = Event.objects.filter(date_time__range=(date_start, date_end))

    # For each location, construct list of events
    events_by_loc = {}
    try:
        for event in queryset:
            if not event.planned:
                # don't accept events not planned
                continue
            if not event.date_time or before_now(event.date_time):
                # skip events with blank date_time or in past
                continue
            # TODO: add later
#           if not event.owner:
#               # skip events with no owner
#               continue
            if event.location not in events_by_loc:
                events_by_loc[event.location] = []
            events_by_loc[event.location].append(event)
    except:
        pdb.set_trace()
    # for each location, find sets of events whose times overlap
    conflict_set = set()
    for l_events in events_by_loc.values():
        # nothing to do if list doesn't have more than one event
        if len(l_events) > 1:
            l_events.sort(key = lambda x: x.date_time)
            # find if events overlap - events are sorted by start time
            conflict_set |= find_draft_event_conflicts(l_events)
#   pdb.set_trace()
    count = 0
    for event in queryset:
        if not event.date_time or before_now(event.date_time):
            # blank date_time or in past: keep event as draft, don't touch event
            continue
        elif event in conflict_set:
            # time conflict: keep event as draft, don't touch event
            conflict_set.remove(event)
        elif event.planned and event.draft:
            # no conflict, accept event into calendar
            event.draft = False
            event.save()
            count += 1
    sched_log.info('draft events accepted ' + str(count))
event_draft_accept.short_description = "Accept selected draft events"

def event_copy(modeladmin, request, queryset):
    for event in queryset:
        new_event = event
        new_event.pk = None
        new_event.draft = True
        new_event.nickname += ' (Copy)'
        new_event.save()
event_copy.short_description = "Copy selected draft events"

def event_draft_delete(modeladmin, request, queryset):
    for event in queryset:
        if event.draft and not event.planned:
            event.delete()
event_draft_delete.short_description = "Delete selected draft events"

def event_mv_week_before(modeladmin, request, queryset):
    for event in queryset:
        # Convert date_time back to time zone unaware, local time
        # Subtract 7 days
        dt = event.date_time.astimezone(TZ_LOCAL) - 7*DAY
        event.date_time = calc_start_time(dt, event.event_type)
        event.date_chg  = True
        # TODO: add code to change date of announcementes
        event.save()
event_mv_week_before.short_description = "Move selected draft event dates one week before"

def event_mv_week_after(modeladmin, request, queryset):
    for event in queryset:
        # Convert date_time back to time zone unaware, local time
        # Add 7 days
        dt = event.date_time.astimezone(TZ_LOCAL) + 7*DAY
        event.date_time = calc_start_time(dt, event.event_type)
        event.date_chg  = True
        # TODO: add code to change date of announcementes
        event.save()
event_mv_week_after.short_description = "Move selected draft event dates one week after"

# action from admin event page
def announce_gen(modeladmin, request, queryset):
    sched_announce.gen.announce_gen(modeladmin, request, queryset)
announce_gen.short_description = "Generate announcements from selected events"

class PostDraftEvent(admin.ModelAdmin):
    list_display  = ('nickname', 'draft', 'planned', 'date_chg', 'verified',
                     'category', 'date_time', 'time_length', 'location',
                     'notes')
    list_editable = ('draft',)
    list_filter   = ('draft', 'planned', 'event_type', 'category', 'location',
                     AdminDateTimeYearFilter)
    search_fields = ['nickname']
    ordering      = ('date_time',)
    actions       = [event_copy,
                     event_mv_week_before   , event_mv_week_after,
                     event_draft_set_planned, event_draft_remove_planned,
                     event_draft_accept     , event_draft_delete,
                     announce_gen]
    fields = ('event_type', 'nickname', 'title', 'category', 'verified',
              'location',
              ('date_time', 'time_length'),
              ('time_setup', 'time_teardown'),
              'group',
              ('owner', 'owner_title'),
              'url', 'notes',
              'cancelled',
              ('draft', 'planned'),
              'date_chg')
    list_per_page = 250


admin.site.register(AuxEvent, PostAuxEvent)
admin.site.register(EventType, PostEventType)
admin.site.register(Event, PostDraftEvent)
