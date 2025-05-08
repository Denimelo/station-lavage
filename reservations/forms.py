from django import forms
from .models import Reservation
from .models import Evaluation
from clients.models import Vehicule
from services.models import Service
from accounts.models import CustomUser

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['vehicule', 'service', 'heure_debut', 'heure_fin']
        widgets = {
            'heure_debut': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'heure_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # client passé depuis la vue
        super().__init__(*args, **kwargs)

        # 🔹 Limite aux véhicules du client
        self.fields['vehicule'].queryset = Vehicule.objects.filter(client=user)

        # 🔹 Pas encore de service affiché, filtré dynamiquement en JS après choix du véhicule
        self.fields['service'].queryset = Service.objects.none()

        if 'vehicule' in self.data:
            try:
                vehicule_id = int(self.data.get('vehicule'))
                vehicule = Vehicule.objects.get(id=vehicule_id, client=user)
                self.fields['service'].queryset = Service.objects.filter(type_vehicule=vehicule.type_vehicule)
            except (ValueError, Vehicule.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['service'].queryset = Service.objects.filter(type_vehicule=self.instance.vehicule.type_vehicule)

    def clean(self):
        cleaned_data = super().clean()
        debut = cleaned_data.get('heure_debut')
        fin = cleaned_data.get('heure_fin')

        if debut and fin and fin <= debut:
            self.add_error('heure_fin', "L'heure de fin doit être après l'heure de début.")

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['note', 'commentaire_evaluation']
        widgets = {
            'commentaire_evaluation': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Votre commentaire...'}),
        }
        labels = {
            'commentaire_evaluation': 'Commentaire (optionnel)'
        }

class JustificationAnnulationForm(forms.Form):
    commentaire = forms.CharField(
        label="Motif de l’annulation",
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True
    )

class AssignationForm(forms.Form):
    employe = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='employe', is_active=True),
        label="Employé à assigner"
    )
    heure_debut = forms.DateTimeField(
        label="Heure de début d’assignation",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    def __init__(self, *args, **kwargs):
        self.reservation = kwargs.pop('reservation', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        employe = cleaned_data.get('employe')
        heure_debut = cleaned_data.get('heure_debut')

        if self.reservation and employe and heure_debut:
            if not self.reservation.est_assignable_a(employe, heure_debut):
                raise forms.ValidationError(
                    f"L’employé {employe} n’est pas disponible de {heure_debut} à {heure_debut + self.reservation.duree_estimee()}"
                )
        return cleaned_data

