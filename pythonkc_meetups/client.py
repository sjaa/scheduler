# -*- coding: utf-8 -*-
"""
Provides the PythonKC Meetup.com API client implementation.

"""


from pythonkc_meetups.exceptions import PythonKCMeetupsBadJson
from pythonkc_meetups.exceptions import PythonKCMeetupsBadResponse
from pythonkc_meetups.exceptions import PythonKCMeetupsMeetupDown
from pythonkc_meetups.exceptions import PythonKCMeetupsNotJson
from pythonkc_meetups.exceptions import PythonKCMeetupsRateLimitExceeded
from pythonkc_meetups.parsers    import parse_event
from pythonkc_meetups.parsers    import parse_member_from_rsvp
from pythonkc_meetups.parsers    import parse_photo
import datetime
import json
import mimeparse
import requests
import urllib.request, urllib.parse, urllib.error
from   sched_core.const       import local_time
from   sched_core.config      import coordinator
from   sched_core.sched_log   import sched_log
from   sched_announce.const   import EPOCH_UTC, MEETUP_GROUP_URLNAME
from   sched_announce.config  import meetup_venue_id, how_to_find_us
from   sched_announce.secrets import meetup_organizer

import pdb
import pprint
pp = pprint.PrettyPrinter(indent=4)


MEETUP_API_HOST   = 'https://api.meetup.com'
EVENTS_URL        = MEETUP_API_HOST + '/2/events.json'
RSVPS_URL         = MEETUP_API_HOST + '/2/rsvps.json'
PHOTOS_URL        = MEETUP_API_HOST + '/2/photos.json'
URL_CREATE_EVENT  = MEETUP_API_HOST + '/2/event'
URL_EDIT_EVENT    = MEETUP_API_HOST + '/2/event/'
URL_COMMENT       = MEETUP_API_HOST + '/2/event_comment/'
URL_DELETE_EVENTS = MEETUP_API_HOST + '/2/event/'
GROUP_URLNAME  = MEETUP_GROUP_URLNAME


def calc_seconds_since_epoch(t):
    time_since_epoch = t - EPOCH_UTC
    return int(datetime.timedelta.total_seconds(time_since_epoch))


def organizer_member_id(event):
    # get event owner
    # if owner not Meetup organizer, get group
    if event.owner in meetup_organizer:
        return meetup_organizer[event.owner]
        a = 0
    else:
        group = event.group
        if group not in coordinator:
            return
        user  = coordinator[group]
        if user in meetup_organizer:
            return meetup_organizer[user]
    # no Meetup organizer found.  Meetup defaults to owner of API key
    return


class PythonKCMeetups(object):

    """
    Retrieves information about PythonKC meetups.

    """

    def __init__(self, api_key, num_past_events=None, http_timeout=1,
                 http_retries=2):
        """
        Create a new instance.

        Parameters
        ----------
        api_key
            The Meetup.com API consumer key to make requests with.
        num_past_events
            The max number of events retrieved by get_past_events. Defaults to
            None (no limit).
        http_timeout
            Time, in seconds, to give HTTP requests to complete. Defaults to 1.
        http_retries
            The number of times to retry requests when it is appropriate to do
            so. Defaults to 2.

        """
        self._api_key = api_key
        self._http_timeout = http_timeout
        self._http_retries = http_retries
        self._num_past_events = num_past_events


    def create_event(self, announce):
        """
        Post new PythonKC meetup event.

        Returns
        -------
        ???

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """

#       pdb.set_trace()
        event = announce.event
        organizer = organizer_member_id(event)
        time_start = int(calc_seconds_since_epoch(event.date_time))
        duration   = int(event.time_length.total_seconds())

        params = {'key'            : self._api_key}
#                 'group_urlname'  : GROUP_URLNAME  }
        post   = {'name'           : event.name(),
                  'group_urlname'  : GROUP_URLNAME,
                  'description'    : announce.description() + 'foo',
                  'time'           : time_start*1000,  # milliseconds,
                  'duration'       : duration  *1000,  # milliseconds
#                 'publish_status' : 'published'}
                  'publish_status' : 'draft'}
        if event.location in meetup_venue_id:
            post['venue_id'      ] = meetup_venue_id[event.location]
        if event.location in how_to_find_us:
            post['how_to_find_us'] = how_to_find_us[event.location]
        if organizer:
            post['hosts'] = organizer
        else:
            sched_log.error('event owner/coordinator not Meetup organizer "{}"  --  {}'.
                             format(event.title, local_time(event.date_time)))
        query = urllib.parse.urlencode(params)
        url = '{0}?{1}'.format(URL_CREATE_EVENT, query)
        try:
            data = self._http_post_json(url, post)
        except Exception as e:
            sched_log.error('event meetup failed "{}"  --  {}  --  {}'.
                             format(event.title, local_time(event.date_time), e))
            return False
        event_api_id = data['id']
        sched_log.info('meetup event posted "{}"  --  {}  -- id: {}'.
                       format(event.title, local_time(event.date_time),
                              event_api_id))
        sched_log.debug("after insert event")
        return event_api_id


    def edit_event(self, announce):
        """
        Post new PythonKC meetup event.

        Returns
        -------
        ???

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """

#       pdb.set_trace()
        event = announce.event
        time_start = int(calc_seconds_since_epoch(event.date_time))
        duration   = int(event.time_length.total_seconds())

        params = {'key'            : self._api_key}
#                 'group_urlname'  : GROUP_URLNAME  }
#                 'id'             : announce.event_api_id}
        post   = {'name'           : event.name(),
#                 'group_urlname'  : GROUP_URLNAME,
                  'description'    : announce.description(),
                  'time'           : time_start*1000,  # milliseconds
                  'duration'       : duration  *1000}  # milliseconds
        if event.location in meetup_venue_id:
            post['venue_id'      ] = meetup_venue_id[event.location]
        if event.location in how_to_find_us:
            post['how_to_find_us'] = how_to_find_us[event.location]
        query = urllib.parse.urlencode(params)
        url = '{0}{1}?{2}'.format(URL_EDIT_EVENT, announce.event_api_id, query)
        try:
            data = self._http_post_json(url, post)
            announce.save()
        except Exception as e:
            sched_log.error('event meetup failed {}  --  {}  --  {}'.
                             format(event.title, local_time(event.date_time), e))
            return False
        return True

    # The Meetup API doesn't have a cancel method
    # Instead, prepend "CANCELED -- " to "name" and post comment
    def cancel_event(self, announce):
        """
        Post new PythonKC meetup event.

        Returns
        -------
        ???

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        # Change event name and description
        pdb.set_trace()
        event = announce.event
        name        = '**** C A N C E L E D   --   {} ****'.format(announce.event.name())
        description = '<i>[{}]</i><br><br>{}'\
                      .format(announce.text_cancel, announce.description())
        params = {'key' : self._api_key}
        post   = {'name'        : name,
                  'description' : description}
        # Add modify Meetup post
        query = urllib.parse.urlencode(params)
        url = '{0}{1}?{2}'.format(URL_EDIT_EVENT, announce.event_api_id, query)
        try:
            data = self._http_post_json(url, post)
        except Exception as e:
            sched_log.error('event meetup cancel failed {}  --  {}  --  {}'.
                             format(event.title, local_time(event.date_time), e))
            return False

        # Add comment to announce 
#       query = urllib.parse.urlencode(params)
#       url = '{0}?{1}'.format(URL_EDIT_EVENT, query)
#       data = self._http_post_json(url, post)
        # TODO: uncomment below after publish_status can be set to 'publish'
        '''
        params = {'key' : self._api_key}
        post   = {'name'        : name,
                  'description' : description}
        query = urllib.parse.urlencode(params)
        url = '{0}{1}?{2}'.format(URL_COMMENT, announce.event_api_id, query)
        try:
            data = self._http_post_json(url, post)
        except Exception as e:
            sched_log.error('event meetup comment failed {}  --  {}  --  {}'.
                             format(event.title, local_time(event.date_time), e))
            return False
        '''
        return True

#       event.d_channel[CH_MEETUP]['cancel'] = comment

    def delete_event(self, event_id):
        params = {'key' : self._api_key,
                  'id'  : event_id}
        query = urllib.parse.urlencode(params)
        url = '{0}?{1}'.format(URL_DELETE_EVENT, query)
        data = self._http_post_json(url)

    def get_upcoming_events(self):
        """
        Get upcoming PythonKC meetup events.

        Returns
        -------
        List of ``pythonkc_meetups.types.MeetupEvent``, ordered by event time,
        ascending.

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """

        query = urllib.parse.urlencode({'key': self._api_key,
                                        'group_urlname': GROUP_URLNAME})
        url = '{0}?{1}'.format(EVENTS_URL, query)
        data = self._http_get_json(url)
        events = data['results']
        return [parse_event(event) for event in events]

    def get_past_events(self):
        """
        Get past PythonKC meetup events.

        Returns
        -------
        List of ``pythonkc_meetups.types.MeetupEvent``, ordered by event time,
        descending.

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """

        def get_attendees(event):
            return [attendee for event_id, attendee in events_attendees
                    if event_id == event['id']]

        def get_photos(event):
            return [photo for event_id, photo in events_photos
                    if event_id == event['id']]

        params = {'key': self._api_key,
                  'group_urlname': GROUP_URLNAME,
                  'status': 'past',
                  'desc': 'true'}
        if self._num_past_events:
            params['page'] = str(self._num_past_events)
        query = urllib.parse.urlencode(params)
        url = '{0}?{1}'.format(EVENTS_URL, query)
        data = self._http_get_json(url)
        print("Got JSON")
#       pp.pprint(data)
#       pdb.set_trace()

        events = data['results']
        event_ids = [event['id'] for event in events]

#       events_attendees = self.get_events_attendees(event_ids)
#       events_photos = self.get_events_photos(event_ids)
        events_attendees = []
        events_photos    = []

        return [parse_event(event, get_attendees(event), get_photos(event))
                for event in events]

    def get_events_attendees(self, event_ids):
        """
        Get the attendees of the identified events.

        Parameters
        ----------
        event_ids
            List of IDs of events to get attendees for.

        Returns
        -------
        List of tuples of (event id, ``pythonkc_meetups.types.MeetupMember``).

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        query = urllib.parse.urlencode({'key': self._api_key,
                                  'event_id': ','.join(event_ids)})
        url = '{0}?{1}'.format(RSVPS_URL, query)
        data = self._http_get_json(url)
        rsvps = data['results']
        return [(rsvp['event']['id'], parse_member_from_rsvp(rsvp))
                for rsvp in rsvps
                if rsvp['response'] != "no"]

    def get_event_attendees(self, event_id):
        """
        Get the attendees of the identified event.

        Parameters
        ----------
        event_id
            ID of the event to get attendees for.

        Returns
        -------
        List of ``pythonkc_meetups.types.MeetupMember``.

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        query = urllib.parse.urlencode({'key': self._api_key,
                                        'event_id': event_id})
        url = '{0}?{1}'.format(RSVPS_URL, query)
        data = self._http_get_json(url)
        rsvps = data['results']
        return [parse_member_from_rsvp(rsvp) for rsvp in rsvps
                if rsvp['response'] != "no"]

    def get_events_photos(self, event_ids):
        """
        Get photos for the identified events.

        Parameters
        ----------
        event_ids
            List of IDs of events to get photos for.

        Returns
        -------
        List of tuples of (event id, ``pythonkc_meetups.types.MeetupPhoto``).

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        query = urllib.parse.urlencode({'key': self._api_key,
                                        'event_id': ','.join(event_ids)})
        url = '{0}?{1}'.format(PHOTOS_URL, query)
        data = self._http_get_json(url)
        photos = data['results']
        return [(photo['photo_album']['event_id'], parse_photo(photo))
                for photo in photos]

    def get_event_photos(self, event_id):
        """
        Get photos for the identified event.

        Parameters
        ----------
        event_id
            ID of the event to get photos for.

        Returns
        -------
        List of ``pythonkc_meetups.types.MeetupPhoto``.

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        query = urllib.parse.urlencode({'key': self._api_key,
                                        'event_id': event_id})
        url = '{0}?{1}'.format(PHOTOS_URL, query)
        data = self._http_get_json(url)
        photos = data['results']
        return [parse_photo(photo) for photo in photos]

    def _http_post_json(self, url, post):
        """
        Make an HTTP GET request to the specified URL, check that it returned a
        JSON response, and returned the data parsed from that response.

        Parameters
        ----------
        url
            The URL to GET.

        Returns
        -------
        Dictionary of data parsed from a JSON HTTP response.

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        response = self._http_post(url, post)

        content_type = response.headers['content-type']
        parsed_mimetype = mimeparse.parse_mime_type(content_type)
        if parsed_mimetype[1] not in ('json', 'javascript'):
            raise PythonKCMeetupsNotJson(content_type)

        try:
            return json.loads(response.content.decode('utf-8'))
        except ValueError as e:
            raise PythonKCMeetupsBadJson(e)

    def _http_post(self, url, post):
        """
        Make an HTTP GET request to the specified URL and return the response.

        Retries
        -------
        The constructor of this class takes an argument specifying the number
        of times to retry a GET. The statuses which are retried on are: 408,
        500, 502, 503, and 504.

        Returns
        -------
        An HTTP response, containing response headers and content.

        Exceptions
        ----------
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsRateLimitExceeded

        """
        for try_number in range(self._http_retries + 1):
            response = requests.post(url, data=post, timeout=self._http_timeout)
            status_code = response.status_code
            if status_code == 200 or status_code == 201:
                sched_log.debug('event meetup get response code: {}'.
                                format(status_code))
                return response

            if (try_number >= self._http_retries or
                    status_code not in (408, 500, 502, 503, 504)):

                sched_log.error('event meetup post response code: {}'.
                                format(status_code))
                if status_code >= 500:
                    raise PythonKCMeetupsMeetupDown(response, response.content)
                if status_code == 400:
                    try:
#                       data = json.loads(response.content)
                        data = json.loads(response.content.decode('utf-8'))
                        if data.get('code', None) == 'limit':
                            raise PythonKCMeetupsRateLimitExceeded
                    except:  # Don't lose original error when JSON is bad
                        pass
                raise PythonKCMeetupsBadResponse(response, response.content)


    def _http_get_json(self, url):
        """
        Make an HTTP GET request to the specified URL, check that it returned a
        JSON response, and returned the data parsed from that response.

        Parameters
        ----------
        url
            The URL to GET.

        Returns
        -------
        Dictionary of data parsed from a JSON HTTP response.

        Exceptions
        ----------
        * PythonKCMeetupsBadJson
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsNotJson
        * PythonKCMeetupsRateLimitExceeded

        """
        response = self._http_get(url)
        pp.pprint(response.headers)
#       pdb.set_trace()

        content_type = response.headers['content-type']
        parsed_mimetype = mimeparse.parse_mime_type(content_type)
        if parsed_mimetype[1] not in ('json', 'javascript'):
            raise PythonKCMeetupsNotJson(content_type)

        try:
            x = response.content
            return json.loads(x.decode('utf-8'))
        except ValueError as e:
            raise PythonKCMeetupsBadJson(e)

    def _http_get(self, url):
        """
        Make an HTTP GET request to the specified URL and return the response.

        Retries
        -------
        The constructor of this class takes an argument specifying the number
        of times to retry a GET. The statuses which are retried on are: 408,
        500, 502, 503, and 504.

        Returns
        -------
        An HTTP response, containing response headers and content.

        Exceptions
        ----------
        * PythonKCMeetupsBadResponse
        * PythonKCMeetupsMeetupDown
        * PythonKCMeetupsRateLimitExceeded

        """
        for try_number in range(self._http_retries + 1):
            response = requests.get(url, timeout=self._http_timeout)
            status_code = response.status_code
            if status_code == 200:
#               sched_log.info('event meetup get response code: {}'.
#                               format(status_code))
                return response

            if (try_number >= self._http_retries or
                    status_code not in (408, 500, 502, 503, 504)):
                sched_log.error('event meetup get response code: {}'.
                                format(status_code))
                print('event meetup get response code: {}'.format(status_code))
                if status_code >= 500:
                    raise PythonKCMeetupsMeetupDown(response, response.content)
                if status_code == 400:
                    try:
                        data = json.loads(response.content.decode('utf-8'))
                        if data.get('code', None) == 'limit':
                            raise PythonKCMeetupsRateLimitExceeded
                    except:  # Don't lose original error when JSON is bad
                        pass
                raise PythonKCMeetupsBadResponse(response, response.content)


#meetup = PythonKCMeetups(MEETUP_API_KEY)
