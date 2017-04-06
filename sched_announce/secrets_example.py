# Copy contents to "secrets.py"
#
# DO NOT check in file!

from sched_announce.const import AnnounceChannel


# API secret keys
api_key = {
#   AnnounceChannel.GCal        .value: '',
    AnnounceChannel.Meetup      .value: '1234',
#   AnnounceChannel.Meetup_OSA  .value: '',
#   AnnounceChannel.SJAA_email  .value: '',
#   AnnounceChannel.member_email.value: '',
#   AnnounceChannel.Twitter     .value: '',
#   AnnounceChannel.Facebook    .value: '',
#   AnnounceChannel.Wordpress   .value: '',
}

# TODO: use dictionary with default
meetup_organizer = {
        1 : 111111111,  # Joe
        2 : 222222222   # Frank
}
