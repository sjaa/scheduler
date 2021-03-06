"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/'         , include(admin.site.urls)),
    url(r'^$'              , views.top_page),
    url(r'^sched_ev/'      , include('sched_ev.urls',
                                     namespace='sched_ev',
                                     app_name ='sched_ev')),
    url(r'^sched_announce/', include('sched_announce.urls',
                                     namespace='sched_announce',
                                     app_name ='sched_announce')),
    url(r'^membership/'    , include('membership.urls',
                                     namespace='membership',
                                     app_name ='membership')),
    url(r'^test/'          , include('tester.urls',
                                     namespace='test',
                                     app_name ='test'))
]
