from datetime         import datetime
from django.db.models import Q
from sched_ev.models  import Event


def get_next_evets(timedelta):
    #events = Event.objects.filter(date_time__gte=datetime.now()-timedelta(days=7))
    # get events scheduled for the next 'timedelta', e.g., 7 days
    events = Event.objects.filter(Q(date_time_gte=datetime.now()) &
                                  Q(date_time_gte=datetime.now()+timedelta))
