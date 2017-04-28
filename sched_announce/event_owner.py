
import pdb


def get_event_owner(event):
    if event.owner:
        # event has designated owner
        return event.owner
    else:
        # owner defaults to group coordinator
        group = event.group
        # get first user who is a coordinator of group
        coordinator = group.user_coordinator.first()
        if not coordinator:
            # bad !!
            # TODO: show invalid event owner/group coordinator
            #       show on init?
            return
    return coordinator
