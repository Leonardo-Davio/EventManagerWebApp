from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import Event



# Create your views here.

def index(response):
    today = timezone.now()
    events = Event.objects.filter(date__gte=today)
    return render(response, "main/homepage.html", {"events": events})

def detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, "main/event.html", {"event": event})