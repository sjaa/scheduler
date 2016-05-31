# scheduler
Schedule manager - A Django app that has rules-based events generator.
Has hooks to post events to email and Meetup via their APIs.

Has views/forms to specify event types (templates).  For example,
an event type specifies:
+ title of event
+ location
+ event repeat pattern, e.g., 1st Friday of every month
+ start time, e.g., 7:00pm, 1 hour after sunset

The templates are then used to generate a set of events.  During
event generation, holidays and astronomy events (e.g., 3Q moon,
summer solstice, Jupiter oppositioni) are generated in AuxEvents.
Currently nothing is done with events.  Features to be added later.
See tutorial.rst.

Views show lists of events.  Some views show sunset, twilight, and
moonrise/set times.

All editable views currently require superuser access.

This was originally written to automate most of the effort required
to generate a calendar of events for an astronomy club.  The generator
is aware of lunar cycles and sunset/twilight times.


Required
--------
+ Python 3 (works for 3.4.3)
+ PyEphem (needed if using astronomy based generator)
+   pip install pyephem
+ pytz
+ debug_toolbar (optional)
+   pip install django-debug-toolbar
+ psycopg2 (required if using PostgreSQL)
+ [To be added later - Pickles]

Any number of "channels" can be used to post events, including
Google calendar and Meetup, at pre-set times.

The scheduler currently can only import/export events as a .tsv
file.

Currently all event templates (e.g., event descriptions for Google
calendar/Meetup) are coded in Python.  Most of this, however, are
in files separate from the core modules and should be easy to change,
even those not familiar with Python.


Notes:
-----
- Database
    The default data base is sqlite3, which is a part of Python.
    It's fine for very light usage.  For heavier traffic, PostgreSQL
    is recommended (psycopg2 is required).
- Learn how to back up and restore database by using:
    python manage.py [dumpdata|loaddata]


To be added
-----------
+ HTML links/buttons to access views
+ Convert admin views to user accessible views
+ Add calendar (instead of list) views
+ APIs
  - Meetup
  - email
  - Twitter
  - Facebook
