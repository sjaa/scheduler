from django.conf.urls import url
from . import views

urlpatterns = [
    # event draft views
    url(r'^search$', views.search,
                     name='search'),
#   url(r'^aux_events/(?P<year>\d{4})/(?P<order>[-\w]*)$',
    url(r'^(?P<period>\d{6}-\d{6})/ch=(?P<channel>\d*)/loc=(?P<location>\d*)/event_type=(?P<event_type>\d*)',
                     views.announce_details,
                     name='announce_details')
]
