from django.conf.urls import url
from . import views

urlpatterns = [
    # event draft views
    url(r'^search$', views.search,
                     name='search'),
#   url(r'^aux_events/(?P<year>\d{4})/(?P<order>[-\w]*)$',
    url(r'^(?P<year>\d{4})/channel=(?P<channel>\d*)/location=(?P<location>\d*)/event_type=(?P<event_type>\d*)',
                     views.announce_details,
                     name='announce_details')
]
