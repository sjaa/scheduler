import httplib2
import os
import pdb

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#from sched_core        import google_api
#from sched_core.config import TZ_NAME
import google_api
from   config          import FMT_RFC3339, TZ_NAME, site_names, gcal_id


def gcal_insert(event, channel):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    print('Getting Google credentials')

    cal_id = gcal_id[channel)
    start = local_time_str(event.date_time, FMT_RFC3339)
    end   = local_time_str(event.date_time + event.time_length, FMT_RFC3339)
    event = {'summary'     : event.name(),
             'location'    : site_names[event.location],
             'start'       : {'dateTime' : start,
                              'timeZone' : TZ_NAME},
             'end'         : {'dateTime' : end,
                              'timeZone' : TZ_NAME},
             'description' : description}
    
#   pdb.set_trace()
    credentials = google_api.get_credentials('gcal')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    print('insert event into calendar')
    # 'response' is dictionary
    response = service.events().insert(
                    calendarId = cal_id,
                    body       = event).execute()

    print('{} - id: {}'.format(response['summary'], response['id']))
    pdb.set_trace()

if __name__ == '__main__':
    main()
