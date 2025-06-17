from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# Create your models here.

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('statico', 'Motoraduni statici'),
        ('itinerante', 'Motoraduni itineranti'),
        ('motogiro', 'Motogiri'),
        ('enogastronomico', 'Moto Tour Enogastronomici'),
        ('trackday', 'Trackday')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='eventImages/', blank=True)
    maps_link = models.URLField(max_length=500, blank=True, null=True, help_text="Link al percorso su Maps (opzionale)")
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='statico',
        verbose_name="Tipo di evento"
    )

    def __str__(self):
        return self.title

class Participation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    inscription_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')