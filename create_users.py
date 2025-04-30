from django.contrib.auth import get_user_model

User = get_user_model()

def create_default_users():
    # Gestionnaire
    gestionnaire_email = 'gestionnaire@example.com'
    if not User.objects.filter(email=gestionnaire_email).exists():
        User.objects.create_user(
            email=gestionnaire_email,
            password='gestion123',
            nom='Admin',
            prenom='Gestionnaire',
            telephone='901234567',
            role='gestionnaire',
            is_staff=True
        )
        print(f"✔ Gestionnaire créé : {gestionnaire_email} / gestion123")
    else:
        print(f"ℹ Gestionnaire déjà existant : {gestionnaire_email}")

    # Employé
    employe_email = 'employe@example.com'
    if not User.objects.filter(email=employe_email).exists():
        User.objects.create_user(
            email=employe_email,
            password='employe123',
            nom='Employé',
            prenom='Démo',
            telephone='902345678',
            role='employe'
        )
        print(f"✔ Employé créé : {employe_email} / employe123")
    else:
        print(f"ℹ Employé déjà existant : {employe_email}")
