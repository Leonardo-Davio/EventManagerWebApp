from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Participation
from django.db.models import Count
from django import forms

# Form per la creazione di un nuovo evento
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'location', 'location_link',
            'maps_link', 'image', 'event_type', 'registration_start', 'registration_end'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

def index(request):
    today = timezone.now()
    events = Event.objects.filter(date__gte=today).order_by('date')
    return render(request, "event/homepage.html", {"events": events})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    is_participating = False
    if request.user.is_authenticated:
        is_participating = Participation.objects.filter(user=request.user, event=event).exists()
        is_organizer = request.user.groups.filter(id=2).exists()
    else:
        is_organizer = False
    num_participates = Participation.objects.filter(event=event).count()
    return render(
        request,
        "event/event.html",
        {
            "event": event,
            "is_participating": is_participating,
            "num_participates": num_participates,
            "is_organizer": is_organizer,
        }
    )

def list_event(request):
    today = timezone.now()
    events = Event.objects.filter(date__gte=today).order_by('date').annotate(num_participates=Count('registrations'))
    events_passed = Event.objects.filter(date__lt=today).order_by('date')
    return render(request, "event/listEvents.html", {
        "events": events,
        "events_passed": events_passed,
    })

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

@login_required
def new_event(request):
    if request.user.is_authenticated:
        is_organizer = request.user.groups.filter(id=2).exists()
        if is_organizer:
            if request.method == 'POST':
                form = EventForm(request.POST, request.FILES)
                if form.is_valid():
                    event = form.save(commit=False)
                    event.organizer = request.user
                    event.save()
                    return redirect('detail', id=event.id)
            else:
                form = EventForm()
            return render(request, "event/newEvent.html", {"form": form})
    return redirect('events')

@login_required
def manage_event(request, id):
    event = get_object_or_404(Event, id=id)
    if event.organizer != request.user:
        return redirect('detail', id=event.id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('detail', id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, "event/manageEvent.html", {"form": form, "event": event})