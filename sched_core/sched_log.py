import logging
import logging.handlers

FILENAME_LOG = 'sched.log'
current_user = 'sam'

class ContextFilter(logging.Filter):
    """
    this is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.user = current_user
        return True

def setup_log():
    handler = logging.handlers.RotatingFileHandler(FILENAME_LOG, maxBytes=2**20, backupCount=5)
    filename_log     = 'sched.log'
    filename_tst_log = 'test.log'
    sched_log = logging.getLogger('Schedule logger')
    sched_log.addFilter(ContextFilter())
    logging.basicConfig(level=logging.INFO,
                        filename = FILENAME_LOG,
#                       filemode = 'w',  # with 'w', start new file each time
#                       format   = '%(levelname)-7s  %(asctime)s  %(user)-10s %(message)s',
                        format   = '%(levelname)-7s  %(asctime)s  %(message)s',
                        datefmt  = '%Y/%m/%d  %H:%M:%S')
    sched_log.addHandler(handler)
# RotatingFileHandler gets error, not working
#   handler = logging.handlers.RotatingFileHandler(FILENAME_LOG, maxBytes=2**19, backupCount=2)
#   FMT_LOG  = '%(asctime)s  %(levelname)-7s  %(user)-10s:  %(message)s',
#   FMT_DATE = '%Y/%m/%d  %H:%M:%S'
#   fmt     = logging.Formatter(FMT_LOG, datefmt=FMT_DATE)
#   handler.setFormatter(fmt)

#   sched_log.setLevel(logging.INFO)
#   sched_log.setLevel(logging.ERROR)
    return sched_log

sched_log = setup_log()

# in files
# from sched_log import *
