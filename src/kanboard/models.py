import datetime

from django.db import models

from kanboard import signals

class Card(models.Model):
    """
    A card is a specific piece of work which must be done on a project, which
    can be hung on a "board" (under a specific "phase").
    """
    title = models.CharField(max_length=80)
    board = models.ForeignKey("Board", related_name="cards")
    phase = models.ForeignKey("Phase", related_name="cards")
    # Order is within a phase.
    order = models.SmallIntegerField()
    created_by = models.ForeignKey('auth.User')
    backlogged_at = models.DateTimeField(default=datetime.datetime.now)

    #Optional fields
    started_at = models.DateTimeField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=80, blank=True)
    # Color represents a "#003399" style css color.
    color = models.CharField(max_length=7, blank=True)
    ready = models.BooleanField()
    blocked = models.BooleanField()
    blocked_because = models.TextField(blank=True)

    class Meta:
        ordering = ['order', ]

    def __unicode__(self):
        return "%s - %s (%s) -- %s" % (self.id, self.title, self.order, self.phase.title)

    def change_phase(self, new_phase, change_at=None):
        """
        Changes a cards phase to the one passed in.
        If the card changes from backlogged to started
        or started to done it updates the appropriate
        timestamps.
        """
        if not change_at: change_at = datetime.datetime.now()

        if self.phase.type == Phase.BACKLOG and new_phase.type in (Phase.PROGRESS, Phase.DONE, Phase.ARCHIVE):
            self.started_at = change_at

        if new_phase.type in (Phase.DONE, Phase.ARCHIVE):
            if not self.done_at: self.done_at = change_at

        if new_phase.type == Phase.PROGRESS and self.done_at:
            self.done_at == None

        if new_phase.type == Phase.BACKLOG and self.started_at:
            self.started_at == None

        from_phase = self.phase
        self.phase = new_phase
        self.save()
        
        signals.phase_change.send(sender=self, from_phase=from_phase, to_phase=new_phase, changed_at=change_at)

signals.phase_change.connect(signals.update_phase_log)

class Board(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField()

    #Optional fields
    description = models.TextField(blank=True)

models.signals.post_save.connect(signals.create_default_phases, sender=Board)

    
class Phase(models.Model):
    UPCOMING = 'upcoming'
    PROGRESS = 'progress'
    FINISHED = 'finished'
    STATUSES = (
        (UPCOMING, 'Upcoming'),
        (PROGRESS, 'In progress'),
        (FINISHED, 'Finished'),
    )

    title = models.CharField(max_length=80)
    board = models.ForeignKey("Board", related_name="phases")
    # Order of the phase within the board:
    order = models.SmallIntegerField()
    # The status is used to determine whether the phase is WIP or not (for
    # stats calculation):
    status = models.CharField(max_length=25, choices=STATUSES,
                              default=PROGRESS)

    #Optional fields
    description = models.TextField(blank=True)
    limit = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u"%s - %s (%s)" % (self.board.title, self.title, self.order)

    def update_log(self, count, changed_at):
        log, created = PhaseLog.objects.get_or_create(phase=self,
                                                      date=changed_at)
        log.count = count 
        log.save()

models.signals.post_save.connect(signals.update_phase_order, sender=Phase)
models.signals.post_save.connect(signals.create_phase_log, sender=Phase)

class PhaseLog(models.Model):
    """
    Tracks the count for a phase for the period of
    one day.
    """
    phase = models.ForeignKey(Phase, related_name='logs')
    count = models.SmallIntegerField(default=0)
    date = models.DateField()

    class Meta:
        unique_together = ('phase', 'date')

    def __unicode__(self):
        return u"%s log on %s - %s" % (self.phase.title, self.date, self.count)

#TODO: Implement goal object


class KanboardStats(object):
    """
    Queries a board and other related models
    to calculate various performance stats.
    """
    def __init__(self, board):
        self.board = board

    def delta_from_done(self, attr_name, start=None, finish=None):
        now = datetime.datetime.now()
        if not finish: finish = now
        
        cards = Card.objects.filter(board = self.board, done_at__lte=finish)
        if start:
            cards = cards.filter(done_at__gte=start)

        if not cards:
            return datetime.timedelta()

        deltas = [ card.done_at - getattr(card, attr_name) for card in cards ]
        the_sum = sum(deltas, datetime.timedelta())
        return the_sum / cards.count()

    def cycle_time(self, start=None, finish=None):
        """
        cycle_time returns a timedelta representing the
        average cycle time of all completed objects on a board.

        Note: Cycle time clock starts when work begins on the request and ends when the item is ready for delivery.
        """
        return self.delta_from_done('started_at', start, finish)

    def lead_time(self, start=None, finish=None):
        """
        lead_time returns a timedelta object representing the
        average lead time of all completed objects on a board.

        It optionally accepts a start and end datetime object,
        which will limit the average to cards completed during that
        time phase.

        Note: Lead time clock starts when the request is made and ends at delivery.
        """
        return self.delta_from_done('backlogged_at', start, finish)

    def cumulative_flow(self, date=None):
        """
        cumulative_flow returns a dictionary-like object,
        each key is a Phase name and the value is the number of 
        objects that were in that phase on that day.

        Note: The done count equals Done + Archive
        """
        if date is None: date = datetime.date.today()
        
        result = {}
        for phase in self.board.phases.all():
            try:
                log = PhaseLog.objects.filter(phase=phase, date__lte=date).order_by('-date')[0]
                result[phase.title] = log.count
            except IndexError:
                #We assume the count is 0 to start because 
                #the phase may not have existed on or before the date requested
                result[phase.title] = 0

        backlog, archive = self.board.get_backlog(), self.board.get_archive()
        archive_count = result[archive.title]
        result[backlog.title] += archive_count
        del result[archive.title]

        return result

