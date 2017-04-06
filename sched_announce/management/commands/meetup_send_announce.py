import pdb

from   django.core.management.base import BaseCommand, CommandError
from   django.utils                import timezone
#from  datetime                    import datetime, timedelta
from   django.db.models            import Q
#from   sched_ev.models             import Event
from   sched_announce.models       import Announce
from   sched_announce.gen          import send_announce
#from   sched_core.const            import FMT_YEAR_DATE_HM, FMT_HMP, FMT_YDATE
#from   sched_core.config           import local_time

import datetime

class Command(BaseCommand):
    help = 'Send scheduled Meetup announcements'

#   def add_arguments(self, parser):
#       parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **options):
#       pdb.set_trace()
#       try:
#           days = int(options['days'][0])
#       except:
#           days = 7
#       td = timedelta(days=days)
#       now = timezone.now()

#       pdb.set_trace()
#       foo()

        # Events in next 'days' days
#       events = Event.objects.filter(Q(date_time__gte=now) &
#                                     Q(date_time__lte=now + td)).order_by('date_time')
#       self.stdout.write('')
#       self.stdout.write('Events in next {} days'.format(days))
#       for ev in events:
#           start_str = local_time(ev.date_time                 ).strftime(FMT_YEAR_DATE_HM)
#           end_str   = local_time(ev.date_time + ev.time_length).strftime(FMT_HMP)
#           s = '{:30} {} - {}'.format(ev.name(), start_str, end_str)
#           self.stdout.write(s)
 
        # Announcements in next 'days' days not announced
        today = timezone.now().date() + datetime.timedelta(days=14)
        announces = Announce.objects.filter(Q(date__lte=today) &
                                            Q(date_announced=None)).order_by('date')
        send_announce(None, None, announces)
#       self.stdout.write('')
#       self.stdout.write('Events not yet announced in next {} days'.format(days))
#       for ann in announces:
#           # print event name, announce date, event date
#           s = '{:30} {} - {}'.format(ann.event.name(),
#                                      ann.date.strftime(FMT_YDATE),
#                                      local_time(ann.event.date_time).strftime(FMT_YDATE))
#           self.stdout.write(s)


