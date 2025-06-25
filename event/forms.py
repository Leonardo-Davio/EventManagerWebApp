from django import forms
from .models import Participation, Event

class ParticipationForm(forms.ModelForm):
    accompagnato = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Numero totale di persone (incluso te)",
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            from accounts.models import Motorcycle
            self.fields['motorcycle'].queryset = Motorcycle.objects.filter(owner=user)
        if instance is not None and hasattr(instance, "num_participates"):
            self.fields['accompagnato'].initial = instance.num_participates

    class Meta:
        model = Participation
        fields = ['motorcycle']
        widgets = {
            'motorcycle': forms.Select(attrs={'class': 'form-select'}),
        }

class ParticipationUpdateForm(forms.ModelForm):
    accompagnato = forms.IntegerField(
        min_value=1,
        label="Numero totale di persone (incluso te)",
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            from accounts.models import Motorcycle
            self.fields['motorcycle'].queryset = Motorcycle.objects.filter(owner=user)
        if instance is not None and hasattr(instance, "num_participates"):
            self.fields['accompagnato'].initial = instance.num_participates
            self.fields['motorcycle'].initial = instance.motorcycle

    class Meta:
        model = Participation
        fields = ['motorcycle']
        widgets = {
            'motorcycle': forms.Select(attrs={'class': 'form-select'}),
        }

class EventForm(forms.ModelForm):
    is_cancelled = forms.BooleanField(required=False, label="Annulla evento")

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'date', 'location', 'location_link',
            'maps_link', 'image', 'event_type', 'registration_start', 'registration_end',
            'is_cancelled',
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        from django.utils import timezone
        from datetime import timedelta
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        registration_start = cleaned_data.get('registration_start')
        registration_end = cleaned_data.get('registration_end')
        now = timezone.now()

        if date:
            tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            if date < tomorrow:
                self.add_error('date', "La data dell'evento deve essere almeno domani.")

        if registration_start:
            if registration_start < now:
                self.add_error('registration_start', "Le iscrizioni possono aprirsi solo da ora in poi.")
            if registration_start.minute % 15 != 0:
                self.add_error('registration_start', "I minuti devono essere 00, 15, 30 o 45.")

        if registration_end:
            if registration_end.minute % 15 != 0:
                self.add_error('registration_end', "I minuti devono essere 00, 15, 30 o 45.")

        if registration_end and registration_start and date:
            if registration_end > date:
                self.add_error('registration_end', "La chiusura iscrizioni non può essere dopo l'inizio dell'evento.")
            if registration_end < registration_start:
                self.add_error('registration_end', "La chiusura iscrizioni non può essere prima dell'apertura iscrizioni.")

        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, '__iter__') and not isinstance(image, str):
            if len(image) > 1:
                raise forms.ValidationError("Puoi caricare solo una immagine.")
            image = image[0]
        return image
