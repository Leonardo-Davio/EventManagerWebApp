import requests
from django.db import models
from django.conf import settings
from django.utils import timezone
import re


class Event(models.Model):
    """
    Modello per eventi motociclistici con gestione automatica
    della città in base al link di Maps.
    """
    # Tipologie di evento
    EVENT_TYPE_CHOICES = [
        ('statico', 'Motoraduni statici'),
        ('itinerante', 'Motoraduni itineranti'),
        ('motogiro', 'Motogiri'),
        ('enogastronomico', 'Moto Tour Enogastronomici'),
        ('trackday', 'Trackday'),
    ]

    # FK all'organizzatore principale
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='organized_events',
        verbose_name='Organizzatore'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    date = models.DateTimeField()

    # Campo che verrà popolato automaticamente via reverse-geocoding
    location = models.CharField(max_length=200, verbose_name='Città/Paese di ritrovo')
    location_link = models.CharField(max_length=500, blank=True, help_text='Link del ritrovo')

    # Link al percorso su Maps (opzionale)
    maps_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Link al percorso su Maps (opzionale)'
    )

    image = models.ImageField(upload_to='eventImages/', blank=True)

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='statico',
        verbose_name='Tipo di evento'
    )

    # Date per apertura e chiusura delle iscrizioni
    registration_start = models.DateTimeField(
        verbose_name='Inizio iscrizioni',
        help_text='Quando si aprono le iscrizioni'
    )
    registration_end = models.DateTimeField(
        verbose_name='Fine iscrizioni',
        help_text='Quando scadono le iscrizioni'
    )

    # Flag per cancellazione manuale
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Annullato dall'organizzatore",
        help_text="Se l'organizzatore ha cancellato l'evento"
    )

    def __str__(self):
        return self.title

    @property
    def status(self):
        """
        Restituisce lo stato corrente dell'evento:
          - 'annullato' se is_cancelled=True
          - 'passato' se date < now
          - 'iscrizioni_non_aperte' se now < registration_start
          - 'iscrizioni_aperte' se registration_start <= now <= registration_end
          - 'iscrizioni_chiuse' se now > registration_end e date > now
        """
        now = timezone.now()

        if self.is_cancelled:
            return 'annullato'
        if now > self.date:
            return 'passato'
        if now < self.registration_start:
            return 'iscrizioni_non_aperte'
        if self.registration_start <= now <= self.registration_end:
            return 'iscrizioni_aperte'
        return 'iscrizioni_chiuse'


class Participation(models.Model):
    """
    Modello per la registrazione degli utenti agli eventi.
    """
    STATUS_CHOICES = [
        ('pending', 'In attesa'),
        ('confirmed', 'Confermata'),
        ('cancelled', 'Annullata'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partecipazioni'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    inscription_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Stato iscrizione'
    )

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = 'Partecipazione'
        verbose_name_plural = 'Partecipazioni'

    def __str__(self):
        return f"{self.user} -> {self.event} ({self.status})"
