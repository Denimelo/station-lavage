from django import forms
from .models import Employe, Gestionnaire
from accounts.models import CustomUser
class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['poste']

class GestionnaireForm(forms.ModelForm):
    class Meta:
        model = Gestionnaire
        fields = ['bureau']

class EmployeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = CustomUser
        fields = ['prenom', 'nom', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'employe'
        if commit:
            user.save()
        return user