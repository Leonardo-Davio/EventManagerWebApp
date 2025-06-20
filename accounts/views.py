from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib import messages
from django.views import View

from django.contrib.auth import get_user_model

from event.models import Participation, Event
from .forms import RegistrationForm, CustomPasswordChangeForm, UserUpdateForm, MotorcycleFormSetNew, MotorcycleFormSet
from .models import Motorcycle, User

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        motorcycle_formset = MotorcycleFormSetNew(queryset=Motorcycle.objects.none())
        return render(request, self.template_name, {'form': form, 'motorcycle_formset': motorcycle_formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        motorcycle_formset = MotorcycleFormSetNew(request.POST, queryset=Motorcycle.objects.none())
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
            login(request, user)
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
        for event in events:
            event.date_formatted = event.date.strftime("%d/%m/%Y %H:%M")
        for event in organized_events:
            event.date_formatted = event.date.strftime("%d/%m/%Y %H:%M")
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
            user_form = self.form_class(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)
            moto_formset = MotorcycleFormSet(request.POST, queryset=Motorcycle.objects.filter(owner=request.user))
            if moto_formset.is_valid():
                instances = moto_formset.save(commit=False)
                for instance in instances:
                    instance.owner = request.user
                    instance.save()
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
        is_organizer = self.request.user.is_authenticated and self.request.user.groups.filter(name='Organizer').exists()
        is_profile_organizer = user_profile.groups.filter(name='Organizer').exists()
        # Usa il campo is_owner del modello
        is_owner_user = getattr(user_profile, "is_owner", False)
        context.update({
            'motorcycles': motorcycles,
            'is_owner': is_owner,
            'is_organizer': is_organizer,
            'is_profile_organizer': is_profile_organizer,
            'is_owner_user': is_owner_user,
        })
        return context

    def post(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.groups.filter(name='Organizer').exists()):
            return self.get(request, *args, **kwargs)
        user_profile = self.get_object()
        is_owner_user = getattr(user_profile, "is_owner", False)
        organizer_group, _ = Group.objects.get_or_create(name='Organizer')
        action = request.POST.get("action")
        if action == "add_organizer":
            if not user_profile.groups.filter(name='Organizer').exists():
                user_profile.groups.add(organizer_group)
        elif action == "remove_organizer" and not is_owner_user:
            if user_profile.groups.filter(name='Organizer').exists():
                user_profile.groups.remove(organizer_group)
        return self.get(request, *args, **kwargs)

class FakePasswordResetConfirmView(View):
    template_name = 'accounts/recoveryPassword/passwordResetConfirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        email = request.session.get('reset_email')
        username = request.session.get('reset_username')
        User = get_user_model()
        if not new_password or not confirm_password:
            messages.error(request, "Inserisci e conferma la nuova password.")
        elif new_password != confirm_password:
            messages.error(request, "Le password non coincidono.")
        elif not email or not username:
            messages.error(request, "Sessione scaduta. Ripeti la procedura di recupero.")
            return redirect('password_reset')
        else:
            try:
                user = User.objects.get(email=email, username=username)
                if len(new_password) < 8:
                    messages.error(request, "La password deve contenere almeno 8 caratteri.")
                elif new_password.isdigit() or new_password.isalpha():
                    messages.error(request, "La password deve contenere sia lettere che numeri.")
                else:
                    user.set_password(new_password)
                    user.save()
                    del request.session['reset_email']
                    del request.session['reset_username']
                    messages.success(request, "Password aggiornata con successo. Ora puoi accedere.")
                    return redirect('password_reset_complete_fake')
            except User.DoesNotExist:
                messages.error(request, "Utente non trovato. Ripeti la procedura.")
                return redirect('password_reset')
        return render(request, self.template_name)

class FakePasswordResetView(View):
    template_name = 'accounts/recoveryPassword/passwordReset.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': None})

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        username = request.POST.get("username")
        User = get_user_model()
        if not email or not username:
            messages.error(request, "Inserisci sia username che email.")
            return render(request, self.template_name, {'form': None})
        try:
            user = User.objects.get(email=email, username=username)
            request.session['reset_confirmed'] = True
            request.session['reset_email'] = email
            request.session['reset_username'] = username
        except User.DoesNotExist:
            request.session['reset_confirmed'] = False
        return redirect('password_reset_done')

class FakePasswordResetDoneView(View):
    template_name = 'accounts/recoveryPassword/passwordResetDone.html'

    def get(self, request, *args, **kwargs):
        if request.session.pop('reset_confirmed', False):
            return redirect('password_reset_confirm_fake')
        return render(request, self.template_name)

class FakePasswordResetCompleteView(View):
    template_name = 'accounts/recoveryPassword/passwordResetComlete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
