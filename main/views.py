from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Event



# Create your views here.

def index(response):
    today = timezone.now()
    print(today)
    events = Event.objects.filter(date__gte=today)
    print(events)
    return render(response, "main/homepage.html", {"events": events})