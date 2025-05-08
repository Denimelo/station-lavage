from django.db import models
from django.conf import settings
from clients.models import Vehicule
from services.models import Service
from datetime import timedelta



class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('assignee', 'Assignée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
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

    # Enregistré lors du clic "Commencer" et "Terminer"
    temps_reel_debut = models.DateTimeField(null=True, blank=True)
    temps_reel_fin = models.DateTimeField(null=True, blank=True)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    remise_appliquee = models.PositiveIntegerField(default=0)  # En F CFA
    commentaire_evaluation = models.TextField(blank=True, null=True)
    commentaire_annulation = models.TextField(blank=True, null=True)

    def duree_estimee(self):
        return self.service.duree_estimee if self.service else timedelta(minutes=0)

    def est_assignable_a(self, employe, date_debut):
        date_fin = date_debut + self.duree_estimee()
        conflits = Reservation.objects.filter(
            employe=employe,
            statut__in=['assignee', 'en_cours'],
            heure_debut__lt=date_fin,
            heure_fin__gt=date_debut
        )
        return not conflits.exists()

    def __str__(self):
        return f"Réservation {self.id} - {self.service.nom} - {self.client.prenom} - {self.statut} - {self.vehicule.plaque_immatric}"


class Evaluation(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE, related_name='evaluation')
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # de 1 à 5
    commentaire_evaluation = models.TextField(blank=True, null=True)
    date_evaluation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Évaluation de la réservation #{self.reservation.id} - {self.note}/5"

