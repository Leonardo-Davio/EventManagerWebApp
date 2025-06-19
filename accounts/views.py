from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from event.models import Participation, Event
from .forms import RegistrationForm

# Create your views here.

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'  # Corretto: reindirizza alla home

class DashboardView(TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        participates = Participation.objects.filter(user=user).select_related("event")
        events = [p.event for p in participates]
        is_organizer = user.groups.filter(id=2).exists()
        organized_events = []
        if is_organizer:
            organized_events = Event.objects.filter(organizer=user)
        context.update({
            "events": events,
            "is_organizer": is_organizer,
            "organized_events": organized_events,
        })
        return context
