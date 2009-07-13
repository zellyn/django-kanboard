from django.db import models

class Card(models.Model):
    title = models.CharField(max_length=80)
    

    #Optional fields
    description = models.TextField(blank=True)
    size = models.CharField(max_length=80, blank=True)
    color = models.CharField(max_length=7) #For #003399 style css colors
    ready = models.BooleanField()
    blocked = models.BooleanField()

