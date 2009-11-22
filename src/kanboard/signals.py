import datetime

import django.dispatch

phase_change = django.dispatch.Signal(providing_args=['from_phase', 'to_phase', 'changed_at']) 

def create_phase_log(sender, instance, created, **kwargs):
    if not created: return None

    from kanboard.models import PhaseLog
    log = PhaseLog(phase=instance, count=0, date=datetime.date.today())
    log.save()

def update_phase_log(signal, sender, from_phase, to_phase, changed_at, **kwargs):
    from_phase.update_log(from_phase.cards.count(), changed_at)    
    to_phase.update_log(to_phase.cards.count(), changed_at)

def create_default_phases(sender, instance, created, **kwargs):
    if not created: return None
    instance.phases.create(title="Backlog", status=Phase.UPCOMING, order=1)
    instance.phases.create(title="Done", status=Phase.FINISHED, order=1)
    instance.phases.create(title="Archive", type=Phase.FINISHED, order=2)

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


