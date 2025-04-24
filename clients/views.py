from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VehiculeForm
from .models import Vehicule

@login_required
def mes_vehicules(request):
    vehicules = Vehicule.objects.filter(client=request.user)
    return render(request, 'clients/liste_vehicules.html', {'vehicules': vehicules})

@login_required
def ajouter_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            vehicule = form.save(commit=False)
            vehicule.client = request.user
            vehicule.save()
            return redirect('clients:liste_vehicules')
    else:
        form = VehiculeForm()
    return render(request, 'clients/ajouter_vehicule.html', {'form': form})

@login_required
def modifier_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk, client=request.user)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('clients:liste_vehicules')
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'clients/modifier_vehicule.html', {'form': form})

@login_required
def supprimer_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk, client=request.user)
    if request.method == 'POST':
        vehicule.delete()
        return redirect('clients:liste_vehicules')
    return render(request, 'clients/confirmer_suppression.html', {'vehicule': vehicule})
