import datetime

from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=80)
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

class Board(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField()

    #Optional fields
    description = models.TextField(blank=True)

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

