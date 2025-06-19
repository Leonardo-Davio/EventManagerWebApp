from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Participation
from django.db.models import Count, Sum
from django import forms
from .forms import ParticipationForm, ParticipationUpdateForm


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
    # Eventi futuri ordinati per data (i 3 più vicini)
    upcoming_events = (
        Event.objects.filter(date__gte=today)
        .annotate(num_participates=Sum('registrations__num_participates'))
        .order_by('date')[:3]
    )
    # Eventi con iscrizioni aperte, ordinati per num partecipanti (i 3 più popolari)
    popular_events = (
        Event.objects.filter(date__gte=today)
        .annotate(num_participates=Sum('registrations__num_participates'))
        .filter(registration_start__lte=today, registration_end__gte=today, is_cancelled=False)
        .order_by('-num_participates', 'date')[:3]
    )

    return render(request, "event/homepage.html", {
        "upcoming_events": upcoming_events,
        "popular_events": popular_events,
    })

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    is_participating = False
    participation = None
    if request.user.is_authenticated:
        participation = Participation.objects.filter(user=request.user, event=event).first()
        is_participating = participation is not None
        is_organizer = request.user.groups.filter(id=2).exists()
        if participation:
            form = ParticipationUpdateForm(user=request.user, instance=participation)
        else:
            form = ParticipationForm(user=request.user)
    else:
        is_organizer = False
        form = None
    num_participates = Participation.objects.filter(event=event).aggregate(Sum('num_participates'))[
                           'num_participates__sum'] or 0
    return render(
        request,
        "event/event.html",
        {
            "event": event,
            "is_participating": is_participating,
            "num_participates": num_participates,
            "is_organizer": is_organizer,
            "form": form,
        }
    )

def list_event(request):
    today = timezone.now()
    events = (
        Event.objects.filter(date__gte=today)
        .annotate(num_participates=Sum('registrations__num_participates'))
        .order_by('date')
    )
    events_passed = (
        Event.objects.filter(date__lt=today)
        .annotate(num_participates=Sum('registrations__num_participates'))
        .order_by('date')
    )
    return render(request, "event/listEvents.html", {
        "events": events,
        "events_passed": events_passed,
        "EVENT_TYPE_CHOICES": Event.EVENT_TYPE_CHOICES,
    })

@login_required
def participation_event(request, id):
    event = get_object_or_404(Event, id=id)
    participation = Participation.objects.filter(user=request.user, event=event).first()
    if request.method == "POST":
        if participation:
            form = ParticipationUpdateForm(request.POST, user=request.user, instance=participation)
        else:
            form = ParticipationForm(request.POST, user=request.user)
        if form.is_valid():
            participation = form.save(commit=False)
            accompagnato = form.cleaned_data.get('accompagnato', 1)
            participation.num_participates = accompagnato
            participation.event = event
            participation.user = request.user
            participation.save()
            return redirect('detail', id=id)
    else:
        if participation:
            form = ParticipationUpdateForm(user=request.user, instance=participation)
        else:
            form = ParticipationForm(user=request.user)
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