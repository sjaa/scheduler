# scheduler
Schedule manager - A Django app that has rules-based events generator.  Has hooks to
post events to email and Meetup via their APIs.

[Under development]
Currently has views/forms to specify event types (templates).  For example an
event type specifies:
+ title of event
+ location
+ event repeat pattern, e.g., 1st Friday of every month
+ start time, e.g., 7:00pm, 1 hour after sunset

The templates are then used to generate a set of events.  Currently nothing is done with
events.  Features to be added later.  See tutorial.rst.

All views currently require superuser access.

This was originally written to automate most of the effort required to generate
a calendar of events for an astronomy club.  Since most events are scheduled off
of lunar cycles, the generator is aware of lunar cycles.

Required
--------
+ Python 3 (works for 3.4.3)
+ PyEphem (needed if using astronomy based generator)
+   pip install pyephem
+ pytz
+ debug_toolbar
+   pip install django-debug-toolbar
+ [To be added later - Pickles]

Any number of "channels" can be used to post events, including Google calendar and Meetup, at pre-set times.

The scheduler currently can only import/export events as a .tsv file.

Currently all event templates (e.g., event descriptions for Google calendar/Meetup) are coded in Python.  Most
of this, however, are in files separate from the core modules and should be easy to change, even those not
familiar with Python.


To be added
-----------
+ Convert admin views to user accessible views
+ Add calendar (instead of list) views
+ APIs
  - Meetup
  - email
  - Twitter
  - Facebook
  - Night Sky Network (when their API becomes available)
+ import/export data as XML?
