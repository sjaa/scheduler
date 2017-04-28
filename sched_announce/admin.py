import pdb
from   django.contrib     import admin
from   sched_core.filters import AdminDateYearFilter

from   .config            import channel_name
from   .models            import AnnounceType, Announce
from   .gen               import send_post, send_update, send_announce, \
                                 send_cancel, send_delete

#######################################
# For Announce Type
#
def announce_type_copy(modeladmin, request, queryset):
    for announce_type in queryset:
        new_announce_type    = announce_type
        new_announce_type.pk = None
        new_announce_type.save()
announce_type_copy.short_description = "Copy selected announce types"

class PostAnnounceType(admin.ModelAdmin):
#   list_display  = ('event_type', 'channel', 'group', 'category', 'location', 'days_offset', 'send', 'notes')
    list_display  = ('name', 'channel', 'group', 'category', 'location', 'days_offset', 'send', 'notes')
    list_filter   = ('event_type', 'channel', 'group', 'category', 'location')
    ordering      = ('event_type',)
    fields        = ('event_type', 'channel', 'group', 'category', 'location', 'days_offset',
                     'send', 'is_preface', 'use_header', 'lead_title', 'text',
                     'question', 'rsvp_limit',
                     'notes')
    actions = [announce_type_copy]
    def name(self, obj):
        return str(obj)


#######################################
# For Announce
#
def announce_copy(modeladmin, request, queryset):
    for announce in queryset:
        new_announce    = announce
        new_announce.pk = None
        new_announce.save()
announce_copy.short_description = "Copy selected announcements"

def accept_draft(modeladmin, request, queryset):
    for announce in queryset:
        announce.draft = False
        announce.save()
accept_draft.short_description = "Accept selected draft announcements"

def post(modeladmin, request, queryset):
    send_post(modeladmin, request, queryset)
post.short_description = "Post selected announcements"

def update(modeladmin, request, queryset):
    send_update(modeladmin, request, queryset)
update.short_description = "Update selected announcements"

def announce(modeladmin, request, queryset):
    send_announce(modeladmin, request, queryset)
announce.short_description = "Announce selected announcements"

# TODO: Temporary - Later: initiate from cancel specific form rather than admin view
def cancel(modeladmin, request, queryset):
    send_cancel(modeladmin, request, queryset)
cancel.short_description = "Cancel selected announcements"

def delete(modeladmin, request, queryset):
    send_delete(modeladmin, request, queryset)
delete.short_description = "Delete selected Meetup post"

def ev_date_time(announce):
    return announce.event.date_time
ev_date_time.short_description = 'Event date/time'

# For Announce
class PostAnnounce(admin.ModelAdmin):
    list_display  = ('event', 'channel', 'draft',
                     ev_date_time, 'send', 'date', 'date_posted',
                     'date_announced', 'date_canceled',
                     'notes')
    list_filter   = ('event_type', 'draft', 'channel', AdminDateYearFilter)
#   list_filter   = ('draft', 'channel')
#   list_filter   = ( ('event.event_type', admin.RelatedOnlyFieldListFilter), 'draft', 'channel')
    search_fields = ['event', 'channel', 'date']
    fields        = ('event', 'draft', 'channel', 'send',
                     'date', 'date_posted', 'date_announced', 'date_canceled',
                     'is_preface', 'use_header', 'lead_title',
                     'question', 'rsvp_limit',
                     'text', 'text_cancel',
                     'notes', 'event_api_id')
    ordering      = ('date',)
#   actions = [event_type_copy, event_gen]
#   actions = [announce_copy, send_post]
    actions = [announce_copy, accept_draft, post, update, announce, cancel, delete]



admin.site.register(AnnounceType, PostAnnounceType)
admin.site.register(Announce    , PostAnnounce)
