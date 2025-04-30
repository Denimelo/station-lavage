from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Service
from .forms import ServiceForm
from reservations.models import Reservation
from services.models import Service

def is_gestionnaire(user):
    return user.is_authenticated and user.role == 'gestionnaire'

@login_required
@user_passes_test(is_gestionnaire)
def liste_services(request):
    services = Service.objects.all()

    for service in services:
        total_seconds = service.duree_estimee.total_seconds()
        service.duree_heures = int(total_seconds // 3600)
        service.duree_minutes = int((total_seconds % 3600) // 60)

    return render(request, 'services/liste_services.html', {'services': services})

@login_required
@user_passes_test(is_gestionnaire)
def ajouter_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services:liste_services')
    else:
        form = ServiceForm()
    return render(request, 'services/ajouter_service.html', {'form': form})

@login_required
@user_passes_test(is_gestionnaire)
def modifier_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services:liste_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/modifier_service.html', {'form': form, 'service': service})

@login_required
@user_passes_test(is_gestionnaire)
def supprimer_service(request, id):
    service = get_object_or_404(Service, id=id)

    # Vérifie si le service est lié à une réservation
    if Reservation.objects.filter(service=service).exists():
        error = "Ce service est utilisé dans une ou plusieurs réservations et ne peut pas être supprimé."
        return render(request, 'services/erreur_suppression.html', {'message': error, 'service': service})

    if request.method == 'POST':
        service.delete()
        return redirect('services:liste_services')

    return render(request, 'services/confirmer_suppression.html', {'service': service})

