import datetime
from django.contrib      import admin
from .models             import EventType, Event
from ev_sched.gen_events import calc_start_time, foo
from ev_sched.cal_const  import DAY, TZ_LOCAL
import pdb


def event_gen(modeladmin, request, queryset):
    foo(queryset)
event_gen.short_description = "Generate events from selected templates"

class PostEventType(admin.ModelAdmin):
    list_display = ('nickname', 'category', 'verified', 'location', 'repeat',
                    'lunar_phase', 'month', 'rule_start_time', 'time_start',
                    'time_start_offset', 'notes')
    list_filter = ('repeat', 'category', 'location', 'lunar_phase', 'verified')
    search_fields = ('nickname', 'repeat')
#   raw_id_fields = ('name',)
    ordering = ['nickname']
    actions = [event_gen]


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

def event_draft_accept(modeladmin, request, queryset):
    for event in queryset:
        if event.draft and event.planned:
            event.draft = False
            event.save()
event_draft_accept.short_description = "Accept selected draft events"

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

class PostEvent(admin.ModelAdmin):
    list_display = ('title', 'draft', 'planned', 'date_chg', 'verified', 'date_time', 'category', 'location',
                    'time_length', 'notes')
    list_filter = ('planned', 'draft', 'event_type', 'category', 'location')
    search_fields = ('title',)
#   raw_id_fields = ('name',)
    ordering = ['date_time']
    actions = [event_draft_remove_planned, event_draft_accept, event_draft_delete,
               event_draft_set_planned, event_mv_week_before, event_mv_week_after]
admin.site.register(EventType, PostEventType)
admin.site.register(Event, PostEvent)
