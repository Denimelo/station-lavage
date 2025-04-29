from django.db import models
from django.conf import settings

class Vehicule(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('voiture', 'Voiture'),
        ('moto', 'Moto'),
        ('tricycle', 'Tricycle'),
        ('utilitaire', 'Utilitaire'),
        ('autre', 'Autre'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicules',
        limit_choices_to={'role': 'client'}
    )
    photo = models.ImageField(upload_to='vehicules_photos/')
    plaque_immatric = models.CharField(max_length=20, unique=True)
    nb_roues = models.PositiveIntegerField()
    couleur = models.CharField(max_length=30)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES, default='voiture')

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.plaque_immatric}) - {self.type_vehicule}"
