# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
from cloudinary.models import CloudinaryField
import pytz


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('statico', 'Motoraduni statici'),
        ('motogiro', 'Motogiri'),
        ('enogastronomico', 'Moto Tour Enogastronomici'),
        ('trackday', 'Trackday'),
    ]

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

    location = models.CharField(max_length=200, verbose_name='Città/Paese di ritrovo')
    location_link = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Link del ritrovo'
    )
    maps_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text='Link al percorso su Maps (opzionale)'
    )

    image = CloudinaryField('image', blank=True, null=True)

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='statico',
        verbose_name='Tipo di evento'
    )

    registration_start = models.DateTimeField(
        verbose_name='Inizio iscrizioni',
        help_text='Quando si aprono le iscrizioni'
    )
    registration_end = models.DateTimeField(
        verbose_name='Fine iscrizioni',
        help_text='Quando scadono le iscrizioni'
    )

    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Annullato dall'organizzatore",
        help_text="Se l'organizzatore ha cancellato l'evento"
    )

    def __str__(self):
        return f"{self.title} (ID: {self.id})"

    @property
    def status(self):
        rome_tz = pytz.timezone('Europe/Rome')
        now = timezone.localtime(timezone.now(), timezone=rome_tz)

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

    num_participates = models.PositiveIntegerField(default=1, help_text="Numero totale di partecipanti (utente + ospiti)")

    motorcycle = models.ForeignKey(
        'accounts.Motorcycle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partecipazioni',
        verbose_name='Moto del partecipante'
    )

    class Meta:
        unique_together = ('user', 'event')
        verbose_name = 'Partecipazione'
        verbose_name_plural = 'Partecipazioni'

    def __str__(self):
        return f"{self.user} -> {self.event} ({self.status})"
