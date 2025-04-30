from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'type_vehicule', 'prix', 'duree_estimee']
        widgets = {
            'nom': forms.Select(attrs={'class': 'form-select'}),
            'type_vehicule': forms.Select(attrs={'class': 'form-select'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'duree_estimee': forms.Select(attrs={'class': 'form-select'}),
        }
