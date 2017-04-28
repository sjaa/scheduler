'''
import pdb
from django.contrib             import admin
#from django.contrib.auth.models import User, Group

from .models                    import UserPermission



# For Announce
class PostUserPermission(admin.ModelAdmin):
    list_display  = ('user', 'volunteer', 'notes')
    list_filter   = ('user', 'volunteer')
    search_fields = ['user']
    ordering      = ('user',)
#   actions = [event_type_copy, event_gen]


#admin.site.register(UserPermission, PostUserPermission)
'''
