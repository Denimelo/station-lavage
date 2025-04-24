from django import forms
from .models import Employe, Gestionnaire

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['poste']

class GestionnaireForm(forms.ModelForm):
    class Meta:
        model = Gestionnaire
        fields = ['bureau']