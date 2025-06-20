from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Motorcycle, User
from django.forms import modelformset_factory, BaseModelFormSet
from django.contrib.auth.forms import AuthenticationForm
import re


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(
        required=True,
        max_length=20,
        label="Telefono",
        widget=forms.TextInput(attrs={'inputmode': 'numeric', 'pattern': r'(\+39)?\d{9,15}'}),
        help_text="Inserisci solo numeri. Esempio: 3331234567"
    )
    first_name = forms.CharField(required=True, max_length=30, label="Nome")
    last_name = forms.CharField(required=True, max_length=30, label="Cognome")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Rimuovi spazi e trattini
        phone = phone.replace(" ", "").replace("-", "")
        # Regex: opzionale +39, poi 9-15 cifre
        if not re.fullmatch(r'(\+39)?\d{9,15}', phone):
            raise forms.ValidationError("Inserisci un numero di telefono italiano valido (9-15 cifre, opzionale +39).")
        return phone


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


class RequiredMotorcycleFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        # Almeno una moto deve essere compilata e valida
        valid_forms = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
               and any(form.cleaned_data.get(field) for field in ['brand', 'model', 'year', 'displacement', 'notes'])
        ]
        if len(valid_forms) < 1:
            raise forms.ValidationError("Devi inserire almeno una moto.")


MotorcycleFormSet = modelformset_factory(
    Motorcycle,
    form=MotorcycleForm,
    extra=0,
    can_delete=True
)

MotorcycleFormSetNew = modelformset_factory(
    Motorcycle,
    form=MotorcycleForm,
    extra=1,
    can_delete=False,
    formset=RequiredMotorcycleFormSet
)


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username")


class CustomPasswordChangeForm(PasswordChangeForm):
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