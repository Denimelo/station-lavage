from django.db import models

class Service(models.Model):
    TYPE_VEHICULE_CHOICES = [
        ('voiture', 'Voiture'),
        ('moto', 'Moto'),
        ('tricycle', 'Tricycle'),
        ('utilitaire', 'Utilitaire'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    duree_estimee = models.DurationField(help_text="Durée estimée du service, ex: 01:00:00 pour 1 heure")

    @property
    def prix_affiche(self):
        return f"{self.prix:.0f} F CFA"

    def __str__(self):
        return f"{self.nom} ({self.get_type_vehicule_display()}) - {self.prix_affiche}"

    class Meta:
        unique_together = ('nom', 'type_vehicule')
        ordering = ['type_vehicule', 'nom']

