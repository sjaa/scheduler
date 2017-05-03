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
