from django.conf.urls import url
from .                import views

urlpatterns = [
    # event draft views
    url(r'^search$', views.search,
                     name='announce-search'),
    url(r'^period=(?P<period>\d{6}-\d{6})/ch=(?P<channel>\d*)/loc=(?P<location>\d*)/event_type=(?P<event_type>\d*)',
                     views.announce_details,
                     name='announce_details')
]
