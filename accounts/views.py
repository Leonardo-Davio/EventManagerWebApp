from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator

from event.models import Participation, Event
from .forms import RegistrationForm, CustomPasswordChangeForm, UserUpdateForm, MotorcycleUpdateForm, MotorcycleFormSet
from .models import Motorcycle, User

# Create your views here.

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'  # Corretto: reindirizza alla home

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        motorcycle_formset = MotorcycleFormSet(queryset=Motorcycle.objects.none())
        return render(request, self.template_name, {'form': form, 'motorcycle_formset': motorcycle_formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        motorcycle_formset = MotorcycleFormSet(request.POST, queryset=Motorcycle.objects.none())
        if form.is_valid() and motorcycle_formset.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.phone = form.cleaned_data.get('phone')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            attendee_group, created = Group.objects.get_or_create(name='Attendee')
            user.groups.add(attendee_group)
            for moto_form in motorcycle_formset:
                if moto_form.cleaned_data and not moto_form.cleaned_data.get('DELETE', False):
                    moto = moto_form.save(commit=False)
                    moto.owner = user
                    moto.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'motorcycle_formset': motorcycle_formset})

class DashboardView(TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        participates = Participation.objects.filter(user=user).select_related("event")
        events = [p.event for p in participates]
        is_organizer = user.groups.filter(name='Organizer').exists()
        organized_events = []
        if is_organizer:
            organized_events = Event.objects.filter(organizer=user)
        context.update({
            "events": events,
            "is_organizer": is_organizer,
            "organized_events": organized_events,
        })
        return context

@method_decorator(login_required, name='dispatch')
class SettingsView(FormView):
    template_name = 'accounts/settings.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('settings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        user_form = self.get_form()
        password_form = CustomPasswordChangeForm(user=request.user)
        moto_formset = MotorcycleFormSet(queryset=Motorcycle.objects.filter(owner=request.user))
        return render(request, self.template_name, {
            'form': user_form,
            'password_form': password_form,
            'moto_formset': moto_formset,
        })

    def post(self, request, *args, **kwargs):
        if 'old_password' in request.POST:
            # Cambio password
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            user_form = self.get_form()
            moto_formset = MotorcycleFormSet(queryset=Motorcycle.objects.filter(owner=request.user))
            if password_form.is_valid():
                password_form.save()
                return render(request, self.template_name, {
                    'form': user_form,
                    'password_form': CustomPasswordChangeForm(user=request.user),
                    'moto_formset': moto_formset,
                    'success': True
                })
            return render(request, self.template_name, {
                'form': user_form,
                'password_form': password_form,
                'moto_formset': moto_formset,
            })
        elif 'moto_submit' in request.POST:
            # Gestione aggiunta/modifica/eliminazione moto
            user_form = self.form_class(instance=request.user)  # <-- NON passare request.POST!
            password_form = CustomPasswordChangeForm(user=request.user)
            moto_formset = MotorcycleFormSet(request.POST, queryset=Motorcycle.objects.filter(owner=request.user))
            if moto_formset.is_valid():
                instances = moto_formset.save(commit=False)
                # Assegna l'owner alle nuove moto
                for instance in instances:
                    instance.owner = request.user
                    instance.save()
                # Elimina le moto segnate per la cancellazione
                for obj in moto_formset.deleted_objects:
                    obj.delete()
                return render(request, self.template_name, {
                    'form': user_form,
                    'password_form': password_form,
                    'moto_formset': MotorcycleFormSet(queryset=Motorcycle.objects.filter(owner=request.user)),
                    'success_moto': True
                })
            return render(request, self.template_name, {
                'form': user_form,
                'password_form': password_form,
                'moto_formset': moto_formset,
            })
        else:
            # Update dati utente
            user_form = self.get_form()
            password_form = CustomPasswordChangeForm(user=request.user)
            moto_formset = MotorcycleFormSet(queryset=Motorcycle.objects.filter(owner=request.user))
            if user_form.is_valid():
                user_form.save()
                return render(request, self.template_name, {
                    'form': user_form,
                    'password_form': password_form,
                    'moto_formset': moto_formset,
                    'success': True
                })
            return render(request, self.template_name, {
                'form': user_form,
                'password_form': password_form,
                'moto_formset': moto_formset,
            })

class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        motorcycles = user_profile.motorcycles.all()
        is_owner = self.request.user.is_authenticated and self.request.user == user_profile
        context.update({
            'motorcycles': motorcycles,
            'is_owner': is_owner,
        })
        return context
