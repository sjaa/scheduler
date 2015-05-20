# scheduler
Schedule manager - rule-based events generator.  Posts events to Google calendar and Meetup via their APIs.

[Under development]

This was originally written to automate most of the effort required to generate a calendar of events for an
astronomy club.  Since most events are scheduled off of lunar cycles, the generator is aware of lunar cycles.

Required:
Python 3 (works for 3.4.3)
PyEphem
[To be added later - Pickles]
[To be added later - Django 1.8 (may work for earlier versions)]

Any number of "channels" can be used to post events, including Google calendar and Meetup, at pre-set times.

This is currently a command line invoked app.

The scheduler currently can only import/export events as a .tsv file.

Currently all event templates (e.g., event descriptions for Google calendar/Meetup) are coded in Python.  Most
of this, however, are in files separate from the core modules and should be easy to change, even those not
familiar with Python.


To be added
-----------
+ Django-based web front-end will:
  - control all aspects of scheduler
+ other APIs
  - Twitter
  - Facebook
  - Night Sky Network (when their API becomes available)
+ import/export data as XML?
