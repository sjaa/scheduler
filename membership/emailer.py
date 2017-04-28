import pdb
from   .config import TEST_EMAIL_MODE, TEST_EMAIL_ADDR

def send_email(msg):
    if TEST_EMAIL_MODE:
        if TEST_EMAIL_MODE == 'test email':
            msg['to'] = TEST_EMAIL_ADDR
        elif TEST_EMAIL_MODE == 'print':
            pass
        else:
            print('bad test mode')
            pdb.set_trace()
    else:
