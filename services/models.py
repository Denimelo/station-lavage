from django.db import models

# Create your models here.
from django.db import models

class Service(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('voiture', 'Voiture'),
        ('moto', 'Moto'),
        ('utilitaire', 'Utilitaire'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES)
    prix = models.DecimalField(max_digits=8, decimal_places=2, help_text="En francs CFA")
    duree_estimee = models.DurationField(help_text="Exemple: 00:30:00 pour 30 minutes")

    def __str__(self):
        return f"{self.nom} ({self.type_vehicule}) - {self.prix} FCFA"