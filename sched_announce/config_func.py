from .       import meetup
from .config import AnnounceChannel


func_announce = {
        AnnounceChannel.Meetup      .value : meetup,
#       AnnounceChannel.SJAA_email  .value : None,
#       AnnounceChannel.member_email.value : None,
#       AnnounceChannel.Twitter     .value : None,
#       AnnounceChannel.Facebook    .value : None,
#       AnnounceChannel.Wordpress   .value : None
}
