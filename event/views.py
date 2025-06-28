from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Participation
from django.db.models import Sum
from .forms import ParticipationForm, ParticipationUpdateForm, EventForm
from datetime import timedelta



def index(request):
    today = timezone.now()
    upcoming_events = (
        Event.objects.filter(date__gte=today)
        .annotate(num_participates=Sum('registrations__num_participates'))
        .order_by('date')[:3]
    )
    popular_events = (
        Event.objects.filter(date__gte=today)
        .annotate(num_participates=Sum('registrations__num_participates'))
        .filter(registration_start__lte=today, registration_end__gte=today, is_cancelled=False)
        .order_by('num_participates')[:3]
    )

    for event in upcoming_events:
        event.date_formatted = event.date.strftime("%d/%m/%Y %H:%M")
    for event in popular_events:
        event.date_formatted = event.date.strftime("%d/%m/%Y %H:%M")

    return render(request, "event/homepage.html", {
        "upcoming_events": upcoming_events,
        "popular_events": popular_events,
    })

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    event.date_formatted = event.date.strftime("%d/%m/%Y %H:%M")
    event.registration_start_formatted = event.registration_start.strftime("%d/%m/%Y %H:%M") if event.registration_start else ""
    event.registration_end_formatted = event.registration_end.strftime("%d/%m/%Y %H:%M") if event.registration_end else ""
    is_participating = False
    is_organizer_owner = False
    if request.user.is_authenticated:
        participation = Participation.objects.filter(user=request.user, event=event).first()
        is_participating = participation is not None
        is_organizer = request.user.groups.filter(name="Organizer").exists()
        user = request.user

        if event.organizer_id == user.id:
            is_organizer_owner = True

        if participation:
            form = ParticipationUpdateForm(user=request.user, instance=participation)
        else:
            form = ParticipationForm(user=request.user)
    else:
        is_organizer = False
        form = None
    num_participates = Participation.objects.filter(event=event).aggregate(Sum('num_participates'))[
                           'num_participates__sum'] or 0

    participants = []
    if is_organizer:
        participants = Participation.objects.filter(event=event).select_related('user')

    return render(
        request,
        "event/event.html",
        {
            "event": event,
            "is_participating": is_participating,
            "num_participates": num_participates,
            "is_organizer": is_organizer,
            "form": form,
            "participants": participants,
            "is_organizer_owner": is_organizer_owner,
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

    for event in events:
        event.date_formatted = event.date.strftime("%d/%m/%Y")
    for event in events_passed:
        event.date_formatted = event.date.strftime("%d/%m/%Y")

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
    if request.POST.get('from_dashboard') == '1':
        return redirect('dashboard')
    return redirect('detail', id=id)

@login_required
def new_event(request):
    if request.user.is_authenticated:
        is_organizer = request.user.groups.filter(name="Organizer").exists()
        if is_organizer:
            if request.method == 'POST':
                form = EventForm(request.POST, request.FILES)
                if form.is_valid():
                    event = form.save(commit=False)
                    event.organizer = request.user
                    event.save()
                    return redirect('detail', id=event.id)
            else:
                from django.utils import timezone
                now = timezone.now()
                tomorrow_9 = (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
                def round_to_next_quarter(dt):
                    minute = (dt.minute + 14) // 15 * 15
                    if minute == 60:
                        dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                    else:
                        dt = dt.replace(minute=minute, second=0, microsecond=0)
                    return dt
                tomorrow_9 = round_to_next_quarter(tomorrow_9)
                form = EventForm(initial={'date': tomorrow_9.strftime('%Y-%m-%dT%H:%M')})
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
            event = form.save(commit=False)
            event.is_cancelled = form.cleaned_data.get('is_cancelled', False)
            event.save()
            form.save_m2m()
            return redirect('detail', id=event.id)
    else:
        def round_to_quarter(dt):
            minute = (dt.minute + 7) // 15 * 15
            if minute == 60:
                dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            else:
                dt = dt.replace(minute=minute, second=0, microsecond=0)
            return dt
        initial = {}
        if event.date:
            initial['date'] = round_to_quarter(event.date).strftime('%Y-%m-%dT%H:%M')
        if event.registration_start:
            initial['registration_start'] = round_to_quarter(event.registration_start).strftime('%Y-%m-%dT%H:%M')
        if event.registration_end:
            initial['registration_end'] = round_to_quarter(event.registration_end).strftime('%Y-%m-%dT%H:%M')
        initial['is_cancelled'] = event.is_cancelled
        form = EventForm(instance=event, initial=initial)
    return render(request, "event/manageEvent.html", {"form": form, "event": event})