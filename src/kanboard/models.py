from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=80)
    board = models.ForeignKey("Board", related_name="cards")
    step = models.ForeignKey("Step", related_name="cards")
    order = models.SmallIntegerField() #Order is within a step, steps are pegged to a board
    
    #Optional fields
    description = models.TextField(blank=True)
    size = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=7) #For #003399 style css colors
    ready = models.BooleanField()
    blocked = models.BooleanField()

class Board(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField()

    #Optional fields
    description = models.TextField(blank=True)

class Step(models.Model):
    title = models.CharField(max_length=80)
    board = models.ForeignKey("Board", related_name="steps")

    #Optional fields
    description = models.TextField(blank=True)
        


