from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from services.models import Service
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# 🔹 Vue d'inscription client
def register_client(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Compte client créé avec succès.")
            return redirect(get_dashboard_redirect(user))
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# 🔹 Vue de connexion
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
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
