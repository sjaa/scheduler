from   .models               import AnnounceType, Announce
from   .const                import AnnounceChannel
from   sched_core    .const  import DAY
from   sched_core    .config import TZ_LOCAL
import sched_announce.meetup as meetup


# Add check of 'channel_public' to announce type / announce model clean()
channel_public = {
    AnnounceChannel.Meetup      .value: True , # Meetup
    AnnounceChannel.SJAA_email  .value: True , # SJAA announcelist email
    AnnounceChannel.member_email.value: False, # member email
#   AnnounceChannel.Twitter     .value: True , # Twitter
#   AnnounceChannel.Facebook    .value: True , # Facebook
#   AnnounceChannel.Wordpress   .value: False  # member email
}


# When announcements are accepted (draft=True -> draft=False), process
# announcements.  Meetup is currently the only channel requiring
# pre-processing when announcements are accepted.


func_post = {
        AnnounceChannel.Meetup      .value : meetup.post,
#       AnnounceChannel.SJAA_email  .value : email_sjaa.post,
#       AnnounceChannel.member_email.value : email_member.post,
#       AnnounceChannel.Twitter     .value : twitter.post,
#       AnnounceChannel.Facebook    .value : facebook.post,
#       AnnounceChannel.Wordpress   .value : wordpress.post
}


func_announce = {
#       AnnounceChannel.Meetup      .value : meetup.announce,
        AnnounceChannel.Meetup      .value : meetup,
        AnnounceChannel.SJAA_email  .value : None,
        AnnounceChannel.member_email.value : None,
#       AnnounceChannel.Twitter     .value : None,
#       AnnounceChannel.Facebook    .value : None,
#       AnnounceChannel.Wordpress   .value : None
}


def announce_gen(modeladmin, request, queryset):
    # TODO: how to use modeladmin, request ??
#   pdb.set_trace()
    for event in queryset:
        if event.draft or not event.planned:
            # don't generate announcements for draft or unplanned events
            print("announce_gen: skipped - draft or unplanned")
            continue
        event_type = event.event_type
        date = event.date_time.astimezone(TZ_LOCAL).date()
        announce_types = AnnounceType.objects.filter(event_type=event_type)
        for announce_type in announce_types:
            a = Announce(event_type    = event_type,
                         event         = event,
                         announce_type = announce_type,
                         channel       = announce_type.channel,
                         is_preface    = announce_type.is_preface,
                         use_header    = announce_type.use_header,
                         lead_title    = announce_type.lead_title,
#                        publish_later = announce_type.publish_later,
#                        allow_change  = announce_type.allow_later,
                         notes         = announce_type.notes,
#                        group         = announce_type.group,
                         date          = date - DAY*announce_type.days_offset,
                         draft         = True)
            a.save()




def post(modeladmin, request, queryset):
#   for channel, func in func_announce.items():
#       if func:
#           func.post(request, queryset.filter(event_type=channel))
    for announce in queryset:
        func = func_announce[announce.channel]
        if func:
            func.post(queryset)


def announce(modeladmin, request, queryset):
#   for channel, func in func_announce.items():
#       if func:
#           func.announce(request, queryset.filter(event_type=channel))
    for announce in queryset:
        func = func_announce[announce.channel]
        if func:
            func.announce(queryset)


