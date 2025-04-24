from django.db import models
from django.conf import settings
from services.models import Service
from clients.models import Vehicule
from personnel.models import Employe

class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_heure = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    employe = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Réservation pour {self.client} le {self.date_heure.strftime('%d/%m/%Y %H:%M')}"
