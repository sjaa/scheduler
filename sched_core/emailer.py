'''
    Taken from:
        http://pymotw.com/2/smtplib/

    Works with Earthlink SMTP
    Can't get it to work w/ Google SMTP

    For Google:
        First try the Python script.
            Google will detect a new device but block it.
        In "Settings":
            enable "access for less secure apps"
            In "Recent activity" -> "Devices"
                okay your device.
'''

import smtplib
from   email.utils     import formataddr
from   email.mime.text import MIMEText
import pdb
from   .secrets        import EMAIL_HOST, EMAIL_PORT, \
                              EMAIL_HOST_USER_NAME, EMAIL_HOST_USER_ADDR, \
                              EMAIL_PASSWORD, EMAIL_USE_TLS


def send_email(addr_to, addr_cc, subject, message,
               addr_bcc=EMAIL_HOST_USER_ADDR, addr_from=None):
    if not addr_from:
        addr_from = formataddr((EMAIL_HOST_USER_NAME, EMAIL_HOST_USER_ADDR))
    msg = MIMEText(message)
    msg['To'     ] = addr_to
    if addr_cc:
        msg['CC' ] = addr_cc
    msg['BCC'    ] = addr_bcc
    msg['From'   ] = addr_from
    msg['Subject'] = subject
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#   pdb.set_trace()
    try:
#       server.set_debuglevel(True)
        # identify ourselves, prompting server for supported features
        server.ehlo()
        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

        server.login(EMAIL_HOST_USER_ADDR, EMAIL_PASSWORD)
        server.send_message(msg)
    except Exception as ex:
        return HttpResponse('Email failed: {}', ex)

    finally:
        server.quit()
