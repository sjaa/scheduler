#########################################################################
#
#   Astronomy Club Membership
#   file: membership/urls.py
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

from django.conf.urls import url
from .                import views

urlpatterns = [
    # membership views
    # list all
    # list active
    # list associate
    # list expired
    # list expiring
#   url(r'^active$'   , views.active,
#                       name='membership_active'),
#   url(r'^associate$', views.associate,
#                       name='membership_associate'),
#   url(r'^expiring$' , views.expiring,
#                       name='membership_expiring'),
#   url(r'^new=(?P<period>\d{8}-\d{8})',
#                       views.new,
#                       name='membership_new'),
#   url(r'^renewed=(?P<period>\d{8}-\d{8})',
#                       views.renewed,
#                       name='membership_renewed'),
#   url(r'^expired=(?P<period>\d{8}-\d{8})',
#                       views.expired,
#                       name='membership_expired'),
#   url(r'^report_summary=(?P<period>\d{8}-\d{8})',
#                       views.report_summary,
#                       name='membership_summary'),
#   url(r'^report=(?P<period>\d{8}-\d{8})',
#                       views.report,
#                       name='membership_report'),
    url(r'^search$',
                        views.search,
                        name='search'),
    url(r'^new$',
                        views.new,
                        name='new'),
    url(r'^renew_update$',
                        views.renew_update,
                        name='renew_update'),
    url(r'^report_summary/(?P<period>\d{8}-\d{8})$',
                        views.report_summary,
                        name='report_summary'),
    url(r'^report_details/(?P<period>\d{8}-\d{8})$',
                        views.report_details,
                        name='report_details'),
#   url(r'^report/(?P<type>\a*)$',
#                       views.report_type,
#                       name='report_type'),
#   url(r'^report/expired/(?P<type>\a*)$',
#                       views.report_expired,
#                       name='report_expired'),
#   url(r'^report/(?P<period>\d{8}-\d{8})',
#                       views.report,
#                       name='report'),
    url(r'^verify_orion_ngc244$',
                        views.verify_orion,
                        name='verify_orion'),
    url(r'^verify_membership$',
                        views.verify_membership,
                        name='verify_membership')
]
