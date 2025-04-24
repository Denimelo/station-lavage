from django.db import models
from django.conf import settings

class Vehicule(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('voiture', 'Voiture'),
        ('moto', 'Moto'),
        ('utilitaire', 'Utilitaire'),
        ('autre', 'Autre'),
    ]
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES, default='voiture')
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    plaque_immatric = models.CharField(max_length=20, unique=True)
    couleur = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.type_vehicule} ({self.plaque_immatric})"
