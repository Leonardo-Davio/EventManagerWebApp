from django import forms
from .models import Participation

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
            # Import qui per evitare import circolare
            from accounts.models import Motorcycle
            self.fields['motorcycle'].queryset = Motorcycle.objects.filter(owner=user)
        # Imposta il valore iniziale di accompagnato su num_participates se instance è presente
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
            # Import qui per evitare import circolare
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
