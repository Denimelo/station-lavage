from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ServiceForm
from .models import Service

def est_gestionnaire(user):
    return user.role == 'gestionnaire'

@login_required
@user_passes_test(est_gestionnaire)
def liste_services(request):
    services = Service.objects.all()
    return render(request, 'services/liste_services.html', {'services': services})

@login_required
@user_passes_test(est_gestionnaire)
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
@user_passes_test(est_gestionnaire)
def modifier_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services:liste_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/modifier_service.html', {'form': form})

@login_required
@user_passes_test(est_gestionnaire)
def supprimer_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('services:liste_services')
    return render(request, 'services/confirmer_suppression.html', {'service': service})