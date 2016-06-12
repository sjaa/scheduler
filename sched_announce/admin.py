import pdb
from django.contrib             import admin
#from django.contrib.auth.models import User, Group
#from django.db                  import models
from sched_core.models          import UserPermission

from .const                     import channel_name
from .models                    import AnnounceType, Announce


# For Announce Type
def announce_type_copy(modeladmin, request, queryset):
    for announce_type in queryset:
        new_announce = announce_type
        new_announce.pk = None
        new_announce.save()
announce_type_copy.short_description = "Copy selected announce types"

class PostAnnounceType(admin.ModelAdmin):
    list_display  = ('event_type', 'channel', 'group', 'days_offset', 'notes')
    list_filter   = ('event_type', 'channel', 'group')
    ordering      = ('event_type',)
    fields        = ('event_type', 'channel', 'group', 'days_offset',
                     'is_preface', 'use_header', 'lead_title', 'text',
                     'notes')
    actions = [announce_type_copy]


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
#   ordering      = ('event_type',)
#   actions = [event_type_copy, event_gen]


admin.site.register(AnnounceType, PostAnnounceType)
admin.site.register(Announce    , PostAnnounce)
