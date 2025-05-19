from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# 🔹 Formulaire d'inscription pour les clients
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'nom', 'prenom', 'telephone']  # 👈 on ne met pas le role ici volontairement

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()  # Normaliser l'email en minuscules
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = 'client'  # 👈 Rôle fixé côté serveur
        user.is_active = False  # L'utilisateur sera activé après confirmation
        if commit:
            user.save()
        return user

# 🔹 Formulaire de connexion basé sur l'email
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Adresse e-mail", widget=forms.EmailInput(attrs={'autofocus': True}))
