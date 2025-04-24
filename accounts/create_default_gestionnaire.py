from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Crée un gestionnaire par défaut si aucun n'existe"

    def handle(self, *args, **kwargs):
        email = "narcisseapelete12@gmail.com"
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING("Le gestionnaire existe déjà."))
        else:
            user = CustomUser.objects.create_user(
                first_name="Narcisse",
                last_name="APELETE",
                email=email,
                telephone="98029887",
                password="Narcisse@29102004",
                role="gestionnaire"
            )
            user.is_staff = True  # Optionnel selon ton usage
            user.save()
            self.stdout.write(self.style.SUCCESS("Gestionnaire créé avec succès."))