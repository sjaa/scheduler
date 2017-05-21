#########################################################################
#
#   Astronomy Club Event Generator
#   file: sched_core/google_authorize.py
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
#       2016-06-01  Teruo Utsumi, initial code
#
#########################################################################

import os
import pdb
from   enum         import Enum, unique
import argparse
import httplib2
from   apiclient    import discovery
import oauth2client
from   oauth2client import file
from   oauth2client import client
from   oauth2client import tools

@unique
class GOOGLE_APP(Enum):
    # index 1 is default
    gmail = 1
    gcal  = 2
    admin = 3


# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
param = {GOOGLE_APP.gmail: ('sjaa-scheduler-google-gmail.json',
                            'https://www.googleapis.com/auth/gmail.send',
                            'gmail', 'v1'),
         GOOGLE_APP.gcal : ('sjaa-scheduler-google-gcal.json',
                            'https://www.googleapis.com/auth/calendar',
                            'calendar', 'v3'),
         GOOGLE_APP.admin: ('sjaa-scheduler-google-admin.json',
                            'https://www.googleapis.com/auth/apps.groups.settings ' + \
                            'https://www.googleapis.com/auth/admin.directory.group ' + \
                            'https://www.googleapis.com/auth/admin.directory.user'
                            'admin', 'v3')
}

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'


def authorize(app): # Gets valid user credentials from disk.
    app_param = param[app]
    json_filename = app_param[0]
    scope         = app_param[1]
    app_name      = app_param[2]
    app_version   = app_param[3]
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    credential_path = os.path.join(credential_dir, json_filename)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(app_name, app_version, http=http)
    print('in authorize: got credentials and service')
    return service


# Reset authorization so next time send is attempted, we force a retry of authorization
def deauthorize():
    global service

    service = None
