import pdb
import datetime

from   django.core.management.base import BaseCommand, CommandError
from   django.utils                import timezone
from   django.db.models            import Q

from   sched_core.test             import TEST
from   sched_core.const            import FMT_YDATE
from   sched_core.config           import local_time, local_time_now
from   sched_announce.models       import Announce
from   sched_announce.gen          import send_announce

class Command(BaseCommand):
    help = 'Send scheduled Meetup announcements'

#   def add_arguments(self, parser):
#       parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **options):
        days = 14 + 28
        # Announcements in next 'days' days not announced
        today = local_time_now().date() + datetime.timedelta(days=14)
        announces = Announce.objects.filter(Q(date__lte=today) &
                                            Q(date_announced=None)).order_by('date')
        if TEST:
            # For testing - print to console
            self.stdout.write('')
            self.stdout.write('Events not yet announced in next {} days'.format(days))
            for ann in announces:
                # print event name, announce date, event date
                s = '{:30} {} - {}'.format(ann.event.name(),
                                           ann.date.strftime(FMT_YDATE),
                                           local_time(ann.event.date_time).strftime(FMT_YDATE))
                self.stdout.write(s)
        else:
            send_announce(None, None, announces)
