



import sched_announce
import sched_task



def cron_jobs():
    today = local_time(datetime.datetime.now().date())

    # 
    announces = Announce.objects.filter(Q(date_announced=None) & Q(date__lte=today))
    #send_announce(modeladmin, request, queryset):
    sched_announce.gen.send_announce(None, None, announces)

    # send task reminders
    tasks = Task.objects.filter(Q(reminder_sent=False) & Q(date_reminder__lte=today))
    sched_task.gen.send_reminder(tasks)

    # send task completion reminders
    tasks = Task.objects.filter(Q(date_completed=None) & Q(date_due__lte=today))
    sched_task.gen.send_completion_reminder(tasks)
