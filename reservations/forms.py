from django import forms
from .models import Reservation
from personnel.models import Employe

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['vehicule', 'service', 'date_heure']
        widgets = {
            'date_heure': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class AssignationForm(forms.ModelForm):
    employe = forms.ModelChoiceField(queryset=Employe.objects.all(), required=True, label="Affecter un employé")

    class Meta:
        model = Reservation
        fields = ['employe']