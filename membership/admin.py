import pdb
import datetime
from   django.contrib        import admin
from   sched_core.sched_log  import sched_log
from   sched_core.filters    import AdminDateTimeYearFilter
from   .models               import User


###############
# For EventType
###############


class PostUsers(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'status', 'date_start', 'date_end',
                    'date_since', 'email', 'notes')
#   list_filter = ('status', 'date_end', 'groups', 'coordinator')
    list_filter = ('status', 'date_end', 'volunteer')
    search_fields = ['last_name']
#   ordering = ('status', 'last_name', 'first_name')
#   ordering = ('status', last_name, first_name)
    ordering = ('status',)
    fields = ('status', 'username', 'first_name', 'last_name', 'email',
              ('date_start', 'date_end', 'date_since'),
              'addr1', 'addr2', ('city', 'state', 'zip_code'),
              'phone1', 'phone2',
              'notices', 'associate', 'notes', 'volunteer', 'groups', 'coordinator')
#   actions = [event_type_copy, event_gen]

# TODO: add to list_filter later?
#   volunteer   = models.BooleanField(default=False, choices=L_BOOLEAN)


admin.site.register(User, PostUsers)
