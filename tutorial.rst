========================
Event Scheduler Tutorial
========================

Calendar Generation Process
---------------------------
The following steps outline the process to generate a calendar of events
based on a set of event templates.

#. Specify one or more event templates (called event types)
#. Select templates from which to generate events 
#. Mark all unplanned events that were generated 
#. Change dates of events as needed 
#. Accept draft events 

*Details*

1. Open app

   In a web browser go to "<URL>/admin".

2. Specify new event template

  - *For the time being, do NOT enter a new event type.  An invalid set of fields
    will cause the app to crash.  A validator will be added later.*
  - Under "Ev_Sched", click "Add" to the left of "Event types".
  - Fill out form.  Note that some fields are required and others should be blank,
    depending on what is selected.  E.g., If "Repeat" is "lunar", then "Date" should be
    blank and "Weekday" must be specified.

3. View all event templates

   The templates listed can be constrained by: 
    - Entering text in the search box and clicking "Search" or 
    - Clicking on one or more filter items on the left.

  - Under "Ev_Sched", click "Event types".  Note the following: 

    - click on column header to sort 
    - search box on the top left 
    - "Action" select beneath the search box 
    - filter items in the column on the right 
    - List of events and some of their attributes 

4. View a template

  - Click on a template name in the 2nd left hand column, e.g., "Astronomy 101". 
  - Note the fields.  Some fields are required.  (Shown in bold.)  Without them, the app won't let you proceed until these are filled in.  Depending on the value of certain fields, other fields are also require.  For example, if "Repeat" is "lunar", then "Date" is not required but "Weekday" is.  Note the help text under the boxes of each field. 
  - For now do NOT create a new event template.  Checks to ensure required fields for new templates are not yet in place.  An incorrectly specified template will cause the app to fail! 
  - Click the "back page" button on your browser. 

5. Select templates

   Click the checkbox(es) on the left for one (or more) event templates.  To select all, click on the checkbox (just under "Action") on row of column headers. 

6. Generate events from selected templates

   -   Click in box to the right of "Action:". 
   -   Select "Generate events from selected templates". 
   -   Just to the right click "Go". 

7. View generated events

   -  In the top horizontal menu bar, click "Ev_Sched". 
   -  Click "Events". 

  Just as for templates, the events listed can be constrained by: 

  - Entering text in the search box and clicking "Search" or 
  - Clicking on one or more filter items on the right. 

  Note the following: 

  - search box on the top left 
  - "Action" select beneath the search box 
  - filter items in the column on the right 
  - List of events and some of their attributes 

8. View an event

   Click an event under "Title".

9. Event field explanation 

  - Event type - Template from which the event was generated.  Needed esp.
    for events with a relative start time since events don't have start time rule. 
  - Title – Name of event 
  - Category – category of event, e.g., public, member, BoD 
  - Date time – date and starting time of event.  Note the date and time formats. 
  - Time length – length of event.  Note the format. 
  - Location – location of event. 
  - Status – "Not verified" means some aspect of event is unknown, e.g.,
    speaker for General Meeting. 
  - Group – Group in charge of event. 
  - Owner – member tasked w/ leading event. 
  - URL – URL for event.  Intended to show page on SJAA website. 
  - Notes – For any notes.  1k characters max. 
  - Cancelled – If checked, event was canceled.  Used to show on calendar. (for future) 
  - Draft – All generated events initially have "Draft" set on.  Will be set
    off after event is accepted. 
  - Planned – Shows whether or not event is planned.  Used to indicate generated
    event should not be accepted into the final calendar. 
  - Date changed – Indicates if date for event was manually changed. 

10. Attributes of events can be changed by either: 

  - One event at a time by clicking on the event under "Title" or 
  - Selecting one or more events and applying an action. 

11. Set unplanned events

  - Select one or more events 
  - Click in box to the right of "Action:". 
  - Select "Make selected events unplanned". 
  - Just to the right click "Go". 
  - The "Planned" field for each selected event will be set off. 

12. Undo unplanned events

  - Same as 11. except select "Make selected events planned".

13. Move date of event back (after) one week 

  - Same as 11. except select "Move selected draft events one week before"
    (or "Move selected draft events one week after)".

  For events with a relative start time (e.g., civil twilight), the
  actual start time will be automatically recalculated.

14. Change date/time of one event arbitrarily

    - Click on event under "Title" 
    - Change date/time. 
    - Click "Save" on lower right.

    Note: The user is responsible for setting both the date *AND* time

13. Accept draft events

  - Same as 11. except select "Accept selected draft events". 

  Accepted events are now in the calendar.  Future features will act on only
  accepted (i.e., non-draft) events. 

14. Delete remaining draft events

  To complete the event generation process, in a similar fashion to the above
  steps, select the remaining "draft" events and delete the remaining unplanned
  draft events.

  In general, once an event has been generated it should not be deleted.  Mark
  the event as "canceled" or not "planned".  The idea is that it's better to
  have knowledge of the planning. 
  
  A future version of the app will have non-admin views that prevent deletion
  of events from the database.
