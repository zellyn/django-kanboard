import datetime

from django.db import models

from kanboard.signals import set_backlogged_at, create_default_phases, update_phase_order, phase_change, update_phase_log, create_phase_log

class Card(models.Model):
    title = models.CharField(max_length=80)
    board = models.ForeignKey("Board", related_name="cards")
    phase = models.ForeignKey("Phase", related_name="cards")
    order = models.SmallIntegerField() #Order is within a phase, steps are pegged to a board
    backlogged_at = models.DateTimeField()

    #Optional fields
    started_at = models.DateTimeField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=7, blank=True) #For #003399 style css colors
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
        
        phase_change.send(sender=self, from_phase=from_phase, to_phase=new_phase, changed_at=change_at)

models.signals.pre_save.connect(set_backlogged_at, sender=Card)
phase_change.connect(update_phase_log)

class Board(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField()

    #Optional fields
    description = models.TextField(blank=True)

    def get_backlog(self):
        """
        Returns a boards Backlog phase
        """
        try:
            return Phase.objects.get(board=self, type=Phase.BACKLOG)
        except Phase.DoesNotExist:
            return none

    def get_done(self):
        """
        Returns a board's Done phase
        """
        try:
            return Phase.objects.get(board=self, type=Phase.DONE)
        except Phase.DoesNotExist:
            return None

    def get_archive(self):
        """
        Returns a board's Archive phase
        """
        try:
            return Phase.objects.get(board=self, type=Phase.ARCHIVE)
        except Phase.DoesNotExist:
            return None

models.signals.post_save.connect(create_default_phases, sender=Board)

    
class Phase(models.Model):
    BACKLOG = 'backlog'
    PROGRESS = 'progress'
    DONE = 'done'
    ARCHIVE = 'archive'
    CHOICES = (
        (BACKLOG, 'Backlog'),
        (PROGRESS, 'In progress'),
        (DONE, 'Done'),
        (ARCHIVE, 'Archive'),
    )

    title = models.CharField(max_length=80)
    board = models.ForeignKey("Board", related_name="phases")
    order = models.SmallIntegerField() #Order is within a board
    type = models.CharField(max_length=25, choices=CHOICES, default=PROGRESS) #We'll need to know if a phase is WIP or not for stats calculation

    #Optional fields
    description = models.TextField(blank=True)
    limit = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['order', ]

    def __unicode__(self):
        return u"%s - %s (%s)" % (self.board.title, self.title, self.order)

    def update_log(self, count, changed_at):
        log, created = PhaseLog.objects.get_or_create(phase=self, date=changed_at)
        log.count = count 
        log.save()

models.signals.post_save.connect(update_phase_order, sender=Phase)
models.signals.post_save.connect(create_phase_log, sender=Phase)

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

    def lead_time(self, start=None, finish=None):
        now = datetime.datetime.now()
        if not finish: finish = now 
        
        cards = Card.objects.filter(board = self.board, done_at__lte=finish)
        if start:
            cards = cards.filter(done_at__gte=start)

        if not cards:
            return datetime.timedelta() 

        deltas = [ card.done_at - card.backlogged_at for card in cards ]
        lead_sum = sum(deltas, datetime.timedelta())
        return lead_sum / cards.count()

    def cumulative_flow(self, date=None):
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
