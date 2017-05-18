#########################################################################
#
#   Astronomy Club Event Scheduler
#   file: membership/process.py
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

import os
import pdb
import datetime
import base64
#from   email.mime.base      import MIMEBase
#from   email.mime.image     import MIMEImage
#from   email.mime.multipart import MIMEMultipart
from   email.mime.text      import MIMEText
import apiclient.errors

from   .google_authorize    import authorize
from   .test                import TestModes, EMAIL_ON
from   .sched_log           import *
#from test_log               import *


#FMT_NO_TO    = 'Google email - No to, cc, bcc'
#FMT_NO_SUBJ  = 'Google email - No subject'
#FMT_NO_MSG   = 'Google email - No message'
FMT_MSG_SENT = 'Google email - message sent, Id: {}'
FMT_ERROR    = 'Google email - error: {}'
#FMT_TST_SENT = "from:{}\nto:{}\nsubject:{}\ntext:{}"

service = None

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail'


def send_msg(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
#   pdb.set_trace()
    try:
        if EMAIL_ON:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            # TODO: remove next line later
#           print ('Message Id: %s' % message['id'])
            logging.info(FMT_MSG_SENT.format(message['id']))
        else:
            print('error - Email mode is not set')
    except apiclient.errors.HttpError as error:
        logging.error(FMT_ERROR.format(error))
        print('in send_msg: error - {}'.format(error))
        raise Exception


def create_message(sender, to, subject, message_text): # Create a message for an email.
    message = MIMEText(message_text, 'plain', 'utf-8')
    message['to'     ] = to
    message['from'   ] = sender
    message['subject'] = subject
    raw = base64.b64encode(bytes(str(message), "utf-8"))
    return {'raw': raw.decode()}


def send_gmail( sender, recepient, subject, text_body, test_modes):
    global service
    
    message = create_message( sender, recepient, subject, text_body )
    user_id = 'me'
    if TestModes.Email_To_Console.value in test_modes:
        print('######### email to console ############')
        print(text_body)
        print('#####################')
        print('')
    if test_modes:
        subject = '{} - {}'.format(datetime.datetime.now().strftime('%Y %m-%d %H-%M'), subject)
    if not test_modes or TestModes.Email_To_Tester.value in test_modes:
        # make sure we're authorized by Google first
        if not service:
            service = authorize(OAUTH_SCOPE)
        if not message:
#           print('in send_gmail - bad message')
            raise Exception
        else:
            send_msg(service, user_id, message)
#           print('sent email')
    '''
    except Exception as error:
        logging.error(FMT_ERROR.format(error))
        raise error
        return False
    '''
