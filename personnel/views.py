from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmployeForm, GestionnaireForm
from .models import Employe, Gestionnaire

@login_required
def profil_employe(request):
    employe = get_object_or_404(Employe, user=request.user)
    return render(request, 'personnel/profil_employe.html', {'employe': employe})

@login_required
def profil_gestionnaire(request):
    gestionnaire = get_object_or_404(Gestionnaire, user=request.user)
    return render(request, 'personnel/profil_gestionnaire.html', {'gestionnaire': gestionnaire})