#import httplib2
import os
import pdb

#from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'SJAA Scheduler'


def get_credentials(app):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    if app == 'gcal':
#       SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        SCOPES = 'https://www.googleapis.com/auth/calendar'
    elif app == 'gmail':
        SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    elif app == 'groups':
#       SCOPES = 'https://www.googleapis.com/auth/apps.groups.settings'
        SCOPES = 'https://www.googleapis.com/auth/apps.groups.settings https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.user'
#       SCOPES = 'https://www.googleapis.com/auth/admin.directory.group https://www.googleapis.com/auth/admin.directory.user'
#       SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
#       Use next line instead for 'get_gmail_list.py', but first delete .json written below in '~/.credentials/sjaa-scheduler-google-gmail.json
#       SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    else:
        print('get_credentials: bad Google app name: {}'.format(app))
        exit()

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sjaa-scheduler-google-{}.json'.format(app))
#   pdb.set_trace()
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Google API: Storing credentials to ' + credential_path)
    return credentials
