from django import forms
from .models import Vehicule

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = [
            'photo',
            'plaque_immatric',
            'nb_roues',
            'couleur',
            'marque',
            'modele',
            'type_vehicule',
        ]
        widgets = {
            'type_vehicule': forms.Select(attrs={'class': 'form-select'}),
            'plaque_immatric': forms.TextInput(attrs={'placeholder': 'Ex : AA-123-BB'}),
            'nb_roues': forms.NumberInput(attrs={'min': 2, 'max': 6}),
        }

    def clean_plaque_immatric(self):
        plaque = self.cleaned_data['plaque_immatric'].upper()
        if Vehicule.objects.filter(plaque_immatric=plaque).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Un véhicule avec cette plaque est déjà enregistré.")
        return plaque
