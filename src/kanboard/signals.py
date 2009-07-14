import datetime


def set_backlogged_at(sender, instance, **kwargs):
    if instance.id: return None
    instance.backlogged_at = datetime.datetime.now()

def create_default_phases(sender, instance, created, **kwargs):
    if not created: return None

    from kanboard.models import Phase
    backlog = Phase(title="Backlog", board=instance, type=Phase.BACKLOG, order=0)
    backlog.save()

    progress = Phase(title="In progress", board=instance, type=Phase.PROGRESS, order=1)
    progress.save()

    done = Phase(title="Done", board=instance, type=Phase.DONE, order=2)
    done.save()

    archive = Phase(title="Done", board=instance, type=Phase.ARCHIVE, order=3)
    archive.save()


