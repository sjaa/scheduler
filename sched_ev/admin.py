import datetime
from django.contrib      import admin
from .models             import AuxEvent, EventType, Event
from sched_ev.gen_events import calc_start_time, foo
from sched_ev.cal_const  import DAY, TZ_LOCAL
import pdb


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
    foo(queryset)
event_gen.short_description = "Generate events from selected templates"

def event_type_copy(modeladmin, request, queryset):
    for event_type in queryset:
        new_event_type = event_type
        new_event_type.pk = None
        new_event_type.nickname += ' (Copy)'
        event_type.save()
event_type_copy.short_description = "Copy templates from selected templates"

class PostEventType(admin.ModelAdmin):
    list_display = ('nickname', 'category', 'verified', 'location', 'repeat',
                    'lunar_phase', 'month', 'rule_start_time', 'time_start',
                    'time_start_offset', 'notes')
    list_filter = ('repeat', 'category', 'location', 'lunar_phase', 'verified')
    search_fields = ['nickname']
    ordering = ('nickname',)
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
        ev1_end = ev1.date_time + ev1.time_length
        for ev2 in events_copy:
            if ev1_end > ev2.date_time:
                # ev1 ends after start of ev2
                # if there's a conflict and the event is draft,
                #   add event for later removal
                if ev1.draft:
                    print('** conflict ', ev1.title)
                    conflict_set.add(ev1)
                if ev2.draft:
                    print('** conflict ', ev2.title)
                    conflict_set.add(ev2)
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
            if not event.date_time or before_now(event.date_time):
                # skip events with blank date_time or in past
                continue
            if event.location not in events_by_loc:
                events_by_loc[event.location] = []
            events_by_loc[event.location].append(event)
    except:
        pdb.set_trace()
    # for each location, find pairs of events whose times overlap
    conflict_set = set()
    for l_events in events_by_loc.values():
        if len(l_events) > 1:
            # nothing to do if list doesn't have more than one event
            l_events.sort(key = lambda x: x.date_time)
            # find if events overlap - events are sorted by start time
            conflict_set |= find_draft_event_conflicts(l_events)
    for event in queryset:
        if not event.date_time or before_now(event.date_time):
            # blank date_time or in past: keep event as draft, don't touch event
            continue
        elif event in conflict_set:
            # time conflict: keep event as draft, don't touch event
            conflict_set.remove(event)
        elif event.planned:
            # no conflict, accept event into calendar
            event.draft = False
            event.save()
event_draft_accept.short_description = "Accept selected draft events"

def event_copy(modeladmin, request, queryset):
    for event in queryset:
        if event.planned:
            new_event = event
            new_event.pk = None
            new_event.draft = True
            new_event.nickname += ' (Copy)'
            event.save()
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
        event.save()
event_mv_week_before.short_description = "Move selected draft event dates one week before"

def event_mv_week_after(modeladmin, request, queryset):
    for event in queryset:
        # Convert date_time back to time zone unaware, local time
        # Add 7 days
        dt = event.date_time.astimezone(TZ_LOCAL) + 7*DAY
        event.date_time = calc_start_time(dt, event.event_type)
        event.date_chg  = True
        event.save()
event_mv_week_after.short_description = "Move selected draft event dates one week after"

class PostDraftEvent(admin.ModelAdmin):
    list_display  = ('nickname', 'draft', 'planned', 'date_chg', 'verified',
                     'category', 'date_time', 'time_length', 'location',
                     'notes')
    list_editable = ('draft', 'planned',)
    list_filter   = ('draft', 'planned', 'event_type', 'category', 'location')
    search_fields = ['nickname']
    ordering      = ('date_time',)
    actions       = [event_copy,
                     event_mv_week_before   , event_mv_week_after,
                     event_draft_set_planned, event_draft_remove_planned,
                     event_draft_accept     , event_draft_delete]
    list_per_page = 250


admin.site.register(AuxEvent, PostAuxEvent)
admin.site.register(EventType, PostEventType)
admin.site.register(Event, PostDraftEvent)
