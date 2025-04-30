from django.db import models
from datetime import timedelta

class Service(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('voiture', 'Voiture'),
        ('moto', 'Moto'),
        ('tricycle', 'Tricycle'),
        ('utilitaire', 'Utilitaire'),
    ]

    NOM_SERVICE_CHOICES = [
        ('Lavage Intérieur', 'Lavage Intérieur'),
        ('Lavage Extérieur', 'Lavage Extérieur'),
        ('Lavage Complet', 'Lavage Complet'),
        ('Aspiration', 'Aspiration'),
        ('Désinfection', 'Désinfection'),
    ]

    DUREE_CHOICES = [
        (timedelta(minutes=30), '30 min'),
        (timedelta(hours=1), '1h'),
        (timedelta(minutes=90), '1h30'),
        (timedelta(hours=2), '2h'),
        (timedelta(minutes=150), '2h30'),
        (timedelta(hours=3), '3h'),
    ]

    nom = models.CharField(max_length=50, choices=NOM_SERVICE_CHOICES)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES)
    prix = models.PositiveIntegerField(help_text="Prix en francs CFA")
    duree_estimee = models.DurationField(choices=DUREE_CHOICES)

    def prix_affiche(self):
        return f"{self.prix:,} F CFA"

    def __str__(self):
        return f"{self.nom} ({self.get_type_vehicule_display()})"


    class Meta:
        unique_together = ('nom', 'type_vehicule')
        ordering = ['type_vehicule', 'nom']

