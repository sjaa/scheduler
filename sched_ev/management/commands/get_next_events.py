from django.core.management.base import BaseCommand, CommandError
from datetime                    import datetime, timedelta
from django.db.models            import Q
from sched_ev.models             import Event
from sched_core.const            import FMT_YEAR_DATE_HM, FMT_HMP
from sched_core.config           import TZ_LOCAL


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

class Command(BaseCommand):
    help = 'Display events over specified number of days'

    def add_arguments(self, parser):
        parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            days = int(options['days'])
        except:
            days = 7
        td = timedelta(days=days)
        events = Event.objects.filter(Q(date_time__gte=datetime.now()) &
                                      Q(date_time__lte=datetime.now() + td))
        
        for ev in events:

            start     = ev.date_time.astimezone(TZ_LOCAL)
            start_str = start.strftime(FMT_YEAR_DATE_HM)
            end_str   = (start + ev.time_length).strftime(FMT_HMP)
            s = '{:25} : {} - {}'.format(ev.name(), start_str, end_str)
            self.stdout.write(s)
