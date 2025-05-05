from django import forms
from .models import RapportPeriodique
from django.utils import timezone

class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class RapportForm(forms.Form):
    type_periode = forms.ChoiceField(
        choices=RapportPeriodique.TYPE_PERIODE_CHOICES,
        label="Type de période",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_debut = forms.DateTimeField(
        label="Date de début",
        widget=DateInput(attrs={'class': 'form-control'}),
        initial=timezone.now().replace(hour=0, minute=0, second=0)
    )
    
    date_fin = forms.DateTimeField(
        label="Date de fin",
        widget=DateInput(attrs={'class': 'form-control'}),
        initial=timezone.now()
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_fin < date_debut:
                raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")
            
            if date_fin > timezone.now():
                raise forms.ValidationError("La date de fin ne peut pas être dans le futur.")
            
        return cleaned_data