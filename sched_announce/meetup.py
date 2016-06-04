from models      import AnnounceType, Announce
from core.common import DAY


def gen_meetup(announce_type, event):
    announce = Announce(event           = event,
                        channel         = announce_type.channel,
                        lead_title      = announce_type.lead_title,
                        publicize_later = announce_type.publicize_later,
                        allow_change    = announce_type.allow_later,
                        notes           = announce_type.notes,
                        group           = announce_type.group,
                        date            = event.date_time.date() -
                                          DAY*announce_type.days_offset
                        draft           = True)

def gen_meetup(announce_type, event):
