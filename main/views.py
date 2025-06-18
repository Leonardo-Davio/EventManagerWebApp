from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Participation

def index(request):
    today = timezone.now()
    events = Event.objects.filter(date__gte=today).order_by('date')
    return render(request, "main/homepage.html", {"events": events})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    is_participating = False
    if request.user.is_authenticated:
        is_participating = Participation.objects.filter(user=request.user, event=event).exists()
    return render(request, "main/event.html", {"event": event, "is_participating": is_participating})

def list_event(request):
    today = timezone.now()
    events = Event.objects.filter(date__gte=today).order_by('date')
    events_passed = Event.objects.filter(date__lt=today).order_by('date')
    return render(request, "main/listEvents.html", {"events": events, "events_passed": events_passed})

@login_required
def participation_event(request, id):
    event = get_object_or_404(Event, id=id)
    Participation.objects.get_or_create(user=request.user, event=event)
    return redirect('detail', id=id)

@login_required
def cancel_participation(request, id):
    event = get_object_or_404(Event, id=id)
    Participation.objects.filter(user=request.user, event=event).delete()
    # Controlla se il form ha il campo 'from_dashboard'
    if request.POST.get('from_dashboard') == '1':
        return redirect('dashboard')
    return redirect('detail', id=id)