from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['nom', 'type_vehicule', 'prix', 'duree_estimee']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type_vehicule': forms.Select(attrs={'class': 'form-select'}),
            'prix': forms.NumberInput(attrs={'step': '50','min': '0', 'class': 'form-control', 'placeholder': 'Ex : 1500 F CFA'}),
            'duree_estimee': forms.TextInput(attrs={'placeholder': 'HH:MM:SS', 'class': 'form-control'}),
        }
