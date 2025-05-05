from django.db import models
from django.conf import settings
from clients.models import Vehicule
from services.models import Service



class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('assignee', 'Assignée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),  # ✅ Ajout
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations_client',
        limit_choices_to={'role': 'client'}
    )
    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    employe = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reservations_employe',
        limit_choices_to={'role': 'employe'}
    )
    heure_debut = models.DateTimeField(null=True, blank=True)
    heure_fin = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    remise_appliquee = models.PositiveIntegerField(default=0)  # en F CFA

    def __str__(self):
        return f"Réservation {self.id} - {self.client.prenom} - {self.statut}"


class Evaluation(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE, related_name='evaluation')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # de 1 à 5
    commentaire = models.TextField(blank=True)
    date_evaluation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Évaluation de la réservation #{self.reservation.id} - {self.note}/5"

