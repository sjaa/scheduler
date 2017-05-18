#########################################################################
#
#   Astronomy Club Membership
#   file: membership/admin.py
#
#   Copyright (C) 2017  Teruo Utsumi, San Jose Astronomical Association
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Contributors:
#       2017-06-01  Teruo Utsumi, initial code
#
#########################################################################

import pdb
import datetime
from   django.contrib        import admin
from   sched_core.sched_log  import sched_log
from   sched_core.filters    import AdminDateTimeYearFilter
from   .models               import User
from   .views                import renew


################
# For Membership
################


# action from admin event page
def renew_memberships(modeladmin, request, queryset):
#   renew(modeladmin, request, queryset)
    views.renew(queryset)
renew_memberships.short_description = "Renew memberships"


class PostUsers(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'modified',
                    'status', 'notices',
                    'date_start', 'date_end', 'date_since', 'email', 'notes')
    list_filter = ('status', 'date_end', 'volunteer')
    search_fields = ['last_name', 'email']
    ordering = ('status',)

    fields = ('status',
              ('username', 'is_staff'),
              ('first_name', 'last_name', 'email'),
              ('date_start', 'date_end', 'date_since'),
              'addr1', 'addr2', ('city', 'state', 'zip_code'),
              'phone1', 'phone2',
              'notices', 'associate', 'notes', 'volunteer', 'groups', 'coordinator')
    actions = [renew]

admin.site.register(User, PostUsers)
