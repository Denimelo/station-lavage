import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('employe', 'Employé'),
        ('gestionnaire', 'Gestionnaire'),
    )

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)  # ❗ Obligatoire maintenant
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    prime = models.PositiveIntegerField(default=0)  # bonus facultatif
    points_fidelite = models.PositiveIntegerField(default=0)
    email_confirmed = models.BooleanField(default=False)  # Nouveau champ

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role', 'telephone']  # Ajouté ici aussi

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"


class EmailConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Confirmation pour {self.user.email}"
    
    @property
    def is_expired(self):
        # Expiration après 24 heures
        expiration_time = self.created_at + timezone.timedelta(hours=24)
        return timezone.now() > expiration_time