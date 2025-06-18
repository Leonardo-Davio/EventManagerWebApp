from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from event.models import Participation, Event
from .forms import RegistrationForm

# Create your views here.

def register(response):
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegistrationForm()

    return render(response, 'accounts/register.html', {"form": form})

@login_required
def dashboard(request):
    participates = Participation.objects.filter(user=request.user).select_related("event")
    events = [p.event for p in participates]
    is_organizer = request.user.groups.filter(id=2).exists()
    organized_events = []
    if is_organizer:
        organized_events = Event.objects.filter(organizer=request.user)
    return render(
        request,
        "accounts/dashboard.html",
        {
            "events": events,
            "is_organizer": is_organizer,
            "organized_events": organized_events,
        }
    )
