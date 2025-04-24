from django.db import models
from django.conf import settings

class Employe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'employe'})
    poste = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} - {self.poste}"

class Gestionnaire(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'gestionnaire'})
    bureau = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} (Gestionnaire)"