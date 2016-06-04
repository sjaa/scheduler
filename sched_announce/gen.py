from models      import AnnounceType, Announce
from core.common import DAY


# action from admin event page
def announce_gen(event):
    event_type = event.event_type
    announce_types = AnnounceType.objects.filter(event_type=event_type)
    for a in announce_types:
        a = Announce(event           = event,
                     channel         = announce_type.channel,
                     is_preface      = announce_type.is_preface
                     use_header      = announce_type.use_header
                     lead_title      = announce_type.lead_title,
                     publicize_later = announce_type.publicize_later,
#                    allow_change    = announce_type.allow_later,
                     notes           = announce_type.notes,
                     group           = announce_type.group,
                     date            = event.date_time.date() -
                                       DAY*announce_type.days_offset
                     draft           = True)
        a.save()


# When announcements are accepted (draft=True -> draft=False), process
# announcements.  Meetup is currently the only channel requiring
# processing when announcements are accepted.

announce_func = {
        AnnounceChannel.Meetup      .value : announce_meetup.post,
        AnnounceChannel.SJAA_email  .value : None,
        AnnounceChannel.member_email.value : None,
        AnnounceChannel.Twitter     .value : None,
        AnnounceChannel.Facebook    .value : None,
        AnnounceChannel.Wordpress   .value : None
}

# for admin.py
def announce_post(modeladmin, request, queryset):
    for channel, func in announce_func.items():
        if func:
            func(request, queryset.filter(event_type=channel))


# for announce_meetup.py
def post(request, queryset):
    # initialize channel
    posted = True
    for p in queryset:
        pass
        # if not p.date_sent
        #   form post
        #   send post
        #   receive response
        #   if valid response
        #       extract event ID
        #       set sent date
        #       p.save()
        #   else:
        #       posted = False
    if posted:
        print('log: all Meetup posts sent')
    else:
        print('log: some Meetup posts not sent')
