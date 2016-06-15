import pdb
from   django.contrib     import admin
from   sched_core.models  import UserPermission

from   .const             import channel_name
from   .models            import AnnounceType, Announce
import sched_announce.gen as gen

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
    list_display  = ('event_type', 'channel', 'group', 'days_offset', 'notes')
    list_filter   = ('event_type', 'channel', 'group')
    ordering      = ('event_type',)
    fields        = ('event_type', 'channel', 'group', 'days_offset',
                     'is_preface', 'use_header', 'lead_title', 'text',
                     'notes')
    actions = [announce_type_copy]


#######################################
# For Announce
#
def announce_copy(modeladmin, request, queryset):
    for announce in queryset:
        new_announce    = announce
        new_announce.pk = None
        new_announce.save()
announce_copy.short_description = "Copy selected announcements"

def send_post(modeladmin, request, queryset):
    gen.post(modeladmin, request, queryset)
send_post.short_description = "Post selected announcements"

# TODO: Temporary - Later: initiate from cancel specific form rather than admin view
def send_cancel(modeladmin, request, queryset):
    gen.cancel(modeladmin, request, queryset)
send_cancel.short_description = "Cancel selected announcements"

def send_delete(modeladmin, request, queryset):
    gen.delete(modeladmin, request, queryset)
send_delete.short_description = "Delete selected Meetup post"

# For Announce
class PostAnnounce(admin.ModelAdmin):
    list_display  = ('event', 'channel', 'draft',
                     'date', 'date_posted', 'date_announced', 'date_canceled',
                     'text_cancel', 'notes')
    list_filter   = ('event_type', 'draft', 'channel')
#   list_filter   = ('draft', 'channel')
#   list_filter   = ( ('event.event_type', admin.RelatedOnlyFieldListFilter), 'draft', 'channel')
    search_fields = ['event', 'channel', 'date']
    fields        = ('event', 'draft', 'channel',
                     'date', 'date_posted', 'date_announced', 'date_canceled',
                     'is_preface', 'use_header', 'lead_title',
                     'text', 'text_cancel',
                     'notes', 'event_api_id')
    ordering      = ('date',)
#   actions = [event_type_copy, event_gen]
#   actions = [announce_copy, send_post]
    actions = [announce_copy, send_post, send_cancel, send_delete]



admin.site.register(AnnounceType, PostAnnounceType)
admin.site.register(Announce    , PostAnnounce)
