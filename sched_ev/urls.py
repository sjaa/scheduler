from django.conf.urls import url
from . import views

urlpatterns = [
    # event draft views
    url(r'^events$', views.EventListView.as_view(), name='event_list1'),
    url(r'^events/draft/(?P<year>\d{4})$',
                                        views.event_draft_list  ,
                                        name='event_draft_list'  ),
    url(r'^events_ephem/draft/(?P<year>\d{4})$',
                                        views.event_ephem_draft_list  ,
                                        name='event_ephem_draft_list'  ),
    url(r'^events_ephem/draft/(?P<year>\d{4})/(?P<eventtype>[a-zA-Z0-9_]+)$',
                                        views.event_ephem_draft_list  ,
                                        name='event_ephem_draft_list'  ),
    url(r'^events_ephem/(?P<year>\d{4})$',
                                        views.event_ephem_list  ,
                                        name='event_ephem_list'  ),
    url(r'^events/(?P<year>\d{4})$',    views.event_list        ,
                                        name='event_list'        ),
    url(r'^(?P<pk>\d+)',                views.event_detail,
                                        name='event_detail')
]
