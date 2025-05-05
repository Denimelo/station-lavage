from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

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

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role', 'telephone']  # Ajouté ici aussi

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"

