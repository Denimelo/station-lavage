from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from services.models import Service
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmailConfirmation, CustomUser
from .utils import send_confirmation_email
from .forms import CustomUser, CustomUserCreationForm, CustomAuthenticationForm

# 🔹 Vue d'inscription client
# 🔹 Vue d'inscription client modifiée
def register_client(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Envoyer l'email de confirmation
            send_confirmation_email(user, request)
            messages.success(
                request, 
                "Compte créé avec succès! Veuillez vérifier votre email pour activer votre compte."
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# 🔹 Vue de confirmation d'email
def confirm_email(request, token):
    try:
        confirmation = get_object_or_404(EmailConfirmation, token=token)
        
        if confirmation.is_confirmed:
            messages.info(request, "Votre email a déjà été confirmé. Vous pouvez vous connecter.")
            return redirect('login')
        
        if confirmation.is_expired:
            messages.error(
                request, 
                "Ce lien de confirmation a expiré. Un nouveau lien a été envoyé à votre adresse email."
            )
            send_confirmation_email(confirmation.user, request)
            return redirect('login')
        
        # Activer le compte
        user = confirmation.user
        user.is_active = True
        user.email_confirmed = True
        user.save()
        
        confirmation.is_confirmed = True
        confirmation.save()
        
        messages.success(
            request, 
            "Votre email a été confirmé avec succès! Vous pouvez maintenant vous connecter."
        )
        return redirect('login')
    
    except Exception as e:
        messages.error(request, "Lien de confirmation invalide.")
        return redirect('login')

# 🔹 Vue pour renvoyer l'email de confirmation
def resend_confirmation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if user.email_confirmed:
                messages.info(request, "Votre email a déjà été confirmé. Vous pouvez vous connecter.")
            else:
                send_confirmation_email(user, request)
                messages.success(request, "Un nouveau lien de confirmation a été envoyé à votre adresse email.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Aucun compte n'est associé à cette adresse email.")
    
    return render(request, 'accounts/resend_confirmation.html')

# 🔹 Vue de connexion
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            # Vérifier si l'email est confirmé
            if not user.email_confirmed:
                messages.error(
                    request, 
                    "Votre email n'a pas été confirmé. Veuillez vérifier votre boîte mail ou demander un nouvel email de confirmation."
                )
                return render(request, 'accounts/login.html', {'form': form})
            
            login(request, user)
            return redirect(get_dashboard_redirect(user))
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 🔹 Vue de déconnexion
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# 🔄 Fonction de redirection dynamique
def get_dashboard_redirect(user):
    if user.role == 'client':
        return reverse('dashboard_client')
    elif user.role == 'employe':
        return reverse('dashboard_employe')
    elif user.role == 'gestionnaire':
        return reverse('dashboard_gestionnaire')
    return reverse('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    return HttpResponse("Bienvenue dans votre tableau de bord.")

@login_required
def dashboard_client(request):
    return render(request, 'accounts/dashboard_client.html')

@login_required
def dashboard_gestionnaire(request):
    if request.user.role != 'gestionnaire':
        return redirect('login')

    services = Service.objects.all()
    return render(request, 'accounts/dashboard_gestionnaire.html', {
        'services': services
    })

@login_required
def dashboard_employe(request):
    return render(request, 'accounts/dashboard_employe.html')
