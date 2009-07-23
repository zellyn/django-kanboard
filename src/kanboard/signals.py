import datetime


def set_backlogged_at(sender, instance, **kwargs):
    if instance.id: return None
    if not instance.backlogged_at:
        instance.backlogged_at = datetime.datetime.now()

def create_default_phases(sender, instance, created, **kwargs):
    if not created: return None

    from kanboard.models import Phase
    backlog = Phase(title="Backlog", board=instance, type=Phase.BACKLOG, order=0)
    backlog.save()

    done = Phase(title="Done", board=instance, type=Phase.DONE, order=2)
    done.save()

    archive = Phase(title="Archive", board=instance, type=Phase.ARCHIVE, order=3)
    archive.save()

def update_phase_order(sender, instance, created, **kwargs):
    from kanboard.models import Phase
    if instance.type != Phase.PROGRESS: return None
    board = instance.board
    progress_phases = board.phases.filter(type=Phase.PROGRESS)
    if progress_phases:
        index = progress_phases.count()-1
        highest_phase = progress_phases[index]

        done = board.get_done()
        done.order = highest_phase.order + 1
        done.save()

        archive = board.get_archive()
        archive.order = highest_phase.order + 2
        archive.save()


