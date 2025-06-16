from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title