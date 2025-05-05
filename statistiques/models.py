from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

class RapportPeriodique(models.Model):
    TYPE_PERIODE_CHOICES = [
        ('journalier', 'Journalier'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('annuel', 'Annuel'),
    ]
    
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    type_periode = models.CharField(max_length=20, choices=TYPE_PERIODE_CHOICES)
    nombre_reservations = models.PositiveIntegerField(default=0)
    nombre_reservations_terminees = models.PositiveIntegerField(default=0)
    nombre_reservations_annulees = models.PositiveIntegerField(default=0)
    revenu_total = models.PositiveIntegerField(default=0, help_text="Revenu en francs CFA")
    nombre_employes_actifs = models.PositiveIntegerField(default=0)
    nombre_clients_actifs = models.PositiveIntegerField(default=0)
    
    # Champs pour le suivi des performances
    taux_occupation = models.FloatField(default=0, help_text="Pourcentage d'occupation des employés")
    note_moyenne = models.FloatField(default=0, help_text="Note moyenne des évaluations")
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rapport {self.get_type_periode_display()} du {self.date_debut.strftime('%d/%m/%Y')} au {self.date_fin.strftime('%d/%m/%Y')}"
    
    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['type_periode', 'date_debut']),
        ]

class ServicePopularite(models.Model):
    rapport = models.ForeignKey(RapportPeriodique, on_delete=models.CASCADE, related_name='services_popularite')
    service_id = models.PositiveIntegerField()
    service_nom = models.CharField(max_length=50)
    service_type_vehicule = models.CharField(max_length=20)
    nombre_reservations = models.PositiveIntegerField(default=0)
    pourcentage = models.FloatField(default=0, help_text="Pourcentage du total des réservations")
    revenu_genere = models.PositiveIntegerField(default=0, help_text="Revenu en francs CFA")
    
    def __str__(self):
        return f"{self.service_nom} ({self.service_type_vehicule}) - {self.nombre_reservations} réservations"
    
    class Meta:
        ordering = ['-nombre_reservations']

class PerformanceEmploye(models.Model):
    rapport = models.ForeignKey(RapportPeriodique, on_delete=models.CASCADE, related_name='performances_employes')
    employe = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'employe'},
    )
    services_realises = models.PositiveIntegerField(default=0)
    note_moyenne = models.FloatField(default=0)
    duree_travail_total = models.DurationField(default=datetime.timedelta())
    
    def __str__(self):
        return f"Performance de {self.employe.prenom} {self.employe.nom} - {self.services_realises} services"
    
    class Meta:
        ordering = ['-services_realises']