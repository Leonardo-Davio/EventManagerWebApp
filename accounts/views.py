from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from main.models import Participation
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
    return render(request, "accounts/dashboard.html", {"events": events})
