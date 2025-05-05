from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeForm, GestionnaireForm
from .models import Employe, Gestionnaire
from reservations.models import Reservation
from accounts.models import CustomUser
from personnel.forms import EmployeCreationForm

@login_required
def ajouter_employe(request):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')  # protection d'accès

    if request.method == 'POST':
        form = EmployeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personnel:liste_employes')
    else:
        form = EmployeCreationForm()
    return render(request, 'personnel/gestionnaire/ajouter_employe.html', {'form': form})

@login_required
def profil_employe(request):
    employe = get_object_or_404(Employe, user=request.user)
    return render(request, 'personnel/profil_employe.html', {'employe': employe})

@login_required
def profil_gestionnaire(request):
    gestionnaire = get_object_or_404(Gestionnaire, user=request.user)
    return render(request, 'personnel/profil_gestionnaire.html', {'gestionnaire': gestionnaire})


@login_required
def liste_employes(request):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')  # ou autre vue selon le rôle

    employes = CustomUser.objects.filter(role='employe')
    return render(request, 'personnel/gestionnaire/liste_employes.html', {'employes': employes})

@login_required
def toggle_activation_employe(request, employe_id):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    employe = get_object_or_404(CustomUser, id=employe_id, role='employe')
    employe.is_active = not employe.is_active
    employe.save()

    messages.success(request, f"L'employé a été {'réactivé' if employe.is_active else 'désactivé'}.")
    return redirect('personnel:liste_employes')

@login_required
def recompenser_employe(request, employe_id):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    employe = get_object_or_404(CustomUser, id=employe_id, role='employe')
    employe.prime += 10000  # exemple : ajouter 10 000 F
    employe.save()

    messages.success(request, "Une prime de 10 000 F a été ajoutée à cet employé.")
    return redirect('personnel:liste_employes')

@login_required
def detail_employe(request, employe_id):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    employe = get_object_or_404(CustomUser, id=employe_id, role='employe')
    reservations = Reservation.objects.filter(employe=employe).order_by('-heure_debut')
    nb_terminees = reservations.filter(statut='terminee').count()
    nb_annulees = reservations.filter(statut='annulee').count()

    context = {
        'employe': employe,
        'reservations': reservations,
        'nb_terminees': nb_terminees,
        'nb_annulees': nb_annulees,
    }
    return render(request, 'personnel/gestionnaire/detail_employe.html', context)

@login_required
def historique_employe(request, employe_id):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    employe = get_object_or_404(CustomUser, id=employe_id, role='employe')
    historique = Reservation.objects.filter(employe=employe).order_by('-heure_debut')

    return render(request, 'personnel/gestionnaire/historique_employe.html', {
        'employe': employe,
        'historique': historique
    })

@login_required
def liste_clients(request):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    clients = CustomUser.objects.filter(role='client')
    return render(request, 'personnel/gestionnaire/liste_clients.html', {'clients': clients})

@login_required
def detail_client(request, client_id):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    client = get_object_or_404(CustomUser, id=client_id, role='client')
    reservations = Reservation.objects.filter(client=client).order_by('-heure_debut')

    # Programme fidélité : remise disponible ?
    remise_disponible = client.points_fidelite >= 100

    context = {
        'client': client,
        'reservations': reservations,
        'remise_disponible': remise_disponible,
    }
    return render(request, 'personnel/gestionnaire/detail_client.html', context)
