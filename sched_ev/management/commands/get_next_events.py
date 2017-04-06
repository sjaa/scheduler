import pdb

from django.core.management.base import BaseCommand, CommandError
from django.utils                import timezone
from datetime                    import datetime, timedelta
from django.db.models            import Q
from sched_ev.models             import Event
from sched_announce.models       import Announce, AnnounceType
from sched_core.const            import FMT_YEAR_DATE_HM, FMT_HMP, FMT_YDATE
from sched_core.config           import local_time


'''
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write('Successfully closed poll "%s"' % poll_id)
'''


'''
def foo():
    # hack to set days-to-event to 28 days
    pdb.set_trace()
    announces = Announce.objects.all()
    now_date = timezone.now()
    for an in announces:
        ev_date  = local_time(an.event.date_time     ).date()
#       now_date = local_time(datetime.now()).date()
        an.date = ev_date - timedelta(days=28)
        an.save()
    announces = AnnounceType.objects.all()
    for an in announces:
        an.days_offset = 28
        an.save()
    pdb.set_trace()
'''


class Command(BaseCommand):
    help = 'Display events over specified number of days'

    def add_arguments(self, parser):
        parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **options):
#       pdb.set_trace()
        try:
            days = int(options['days'][0])
        except:
            days = 7
        td = timedelta(days=days)
        now = timezone.now()

#       pdb.set_trace()
#       foo()

        # Events in next 'days' days
        events = Event.objects.filter(Q(date_time__gte=now) &
                                      Q(date_time__lte=now + td)).order_by('date_time')
        self.stdout.write('')
        self.stdout.write('Events in next {} days'.format(days))
        for ev in events:
            start_str = local_time(ev.date_time                 ).strftime(FMT_YEAR_DATE_HM)
            end_str   = local_time(ev.date_time + ev.time_length).strftime(FMT_HMP)
            s = '{:30} {} - {}'.format(ev.name(), start_str, end_str)
            self.stdout.write(s)
 
        # Announcements in next 'days' days not announced
        today = now.date()
        announces = Announce.objects.filter(Q(date__lte=now) &
                                            Q(date_announced=None)).order_by('date')
#       pdb.set_trace()
        self.stdout.write('')
        self.stdout.write('Events not yet announced in next {} days'.format(days))
        for ann in announces:
            # print event name, announce date, event date
            s = '{:30} {} - {}'.format(ann.event.name(),
                                       ann.date.strftime(FMT_YDATE),
                                       local_time(ann.event.date_time).strftime(FMT_YDATE))
            self.stdout.write(s)


