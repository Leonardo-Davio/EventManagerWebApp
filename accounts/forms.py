from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Motorcycle, User
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(required=True, max_length=20)
    first_name = forms.CharField(required=True, max_length=30, label="Nome")
    last_name = forms.CharField(required=True, max_length=30, label="Cognome")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']


class MotorcycleForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = ['brand', 'model', 'year', 'displacement', 'notes']
        labels = {
            'brand': 'Marca',
            'model': 'Modello',
            'year': 'Anno',
            'displacement': 'Cilindrata',
            'notes': 'Note',
        }


MotorcycleFormSet = modelformset_factory(
    Motorcycle,
    form=MotorcycleForm,
    extra=0,
    can_delete=True
)


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username")

    # Usa il comportamento standard di AuthenticationForm
    # quindi non serve ridefinire clean()


class CustomPasswordChangeForm(PasswordChangeForm):
    # Puoi personalizzare le label o i widget se vuoi
    pass


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    phone = forms.CharField(required=True, max_length=20, label="Telefono")
    first_name = forms.CharField(required=True, max_length=30, label="Nome")
    last_name = forms.CharField(required=True, max_length=30, label="Cognome")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']


class MotorcycleUpdateForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = ['brand', 'model', 'year', 'displacement', 'notes']
        labels = {
            'brand': 'Marca',
            'model': 'Modello',
            'year': 'Anno',
            'displacement': 'Cilindrata',
            'notes': 'Note',
        }