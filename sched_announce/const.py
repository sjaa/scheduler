from   enum            import Enum, unique


@unique
class AnnounceChannel(Enum):
    Meetup       = 1
    SJAA_email   = 2
    member_email = 3
    Twitter      = 4
    Facebook     = 5
    Wordpress    = 6

# Add check of 'channel_public' to announce type / announce model clean()
channel_public = {
    AnnounceChannel.Meetup      .value: True , # Meetup
    AnnounceChannel.SJAA_email  .value: True , # SJAA announcelist email
    AnnounceChannel.member_email.value: False, # member email
    AnnounceChannel.Twitter     .value: True , # Twitter
    AnnounceChannel.Facebook    .value: True , # Facebook
    AnnounceChannel.Wordpress   .value: False  # member email
}
