from   enum            import Enum, unique


@unique
class AnnounceChannel(Enum):
    Meetup       = 0
    SJAA_email   = 1
    member_email = 2
    twitter      = 3
    facebook     = 4
    wordpress    = 5

# Add check of 'channel_public' to announce type / announce model clean()
channel_public = {
    AnnounceChannel.Meetup      .value: True , # Meetup
    AnnounceChannel.SJAA_email  .value: True , # SJAA announcelist email
    AnnounceChannel.member_email.value: False, # member email
    AnnounceChannel.Twitter     .value: True , # Twitter
    AnnounceChannel.Facebook    .value: True , # Facebook
    AnnounceChannel.Wordpress   .value: False  # member email
}
