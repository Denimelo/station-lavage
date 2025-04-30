from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, EvaluationForm
from .models import Evaluation,Vehicule, Service, Reservation
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

@login_required
def creer_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user
            reservation.statut = 'en_attente'
            reservation.save()
            return redirect('reservations:reservations_client')
    else:
        form = ReservationForm(user=request.user)
    
    return render(request, 'reservations/creer_reservation.html', {'form': form})

@login_required
def liste_reservations_client(request):
    reservations = Reservation.objects.filter(client=request.user).select_related('vehicule', 'service').order_by('heure_debut')
    return render(request, 'reservations/liste_reservations_client.html', {
        'reservations': reservations
    })

@login_required
def suivi_reservation(request, id):
    reservation = get_object_or_404(
        Reservation.objects.select_related('vehicule', 'service', 'employe'),
        id=id,
        client=request.user
    )
    return render(request, 'reservations/suivi_reservation.html', {
        'reservation': reservation
    })

@login_required
def evaluer_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id, client=request.user, statut='terminee')

    if hasattr(reservation, 'evaluation'):
        return redirect('reservations:suivi_reservation', id=reservation.id)  # déjà évalué

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.client = request.user
            evaluation.reservation = reservation
            evaluation.save()
            return redirect('reservations:suivi_reservation', id=reservation.id)
    else:
        form = EvaluationForm()

    return render(request, 'reservations/evaluation.html', {
        'form': form,
        'reservation': reservation
    })

def is_employe(user):
    return user.is_authenticated and user.role == 'employe'

@login_required
@user_passes_test(is_employe)
def reservations_employe(request):
    reservations = Reservation.objects.filter(
        employe=request.user
    ).exclude(statut='annulee').order_by('heure_debut')

    return render(request, 'reservations/reservations_employe.html', {
        'reservations': reservations
    })

@login_required
@user_passes_test(is_employe)
def commencer_service(request, id):
    reservation = get_object_or_404(Reservation, id=id, employe=request.user, statut='assignee')
    reservation.statut = 'en_cours'
    reservation.save()
    return redirect('reservations:reservations_employe')

@login_required
@user_passes_test(is_employe)
def terminer_service(request, id):
    reservation = get_object_or_404(Reservation, id=id, employe=request.user, statut='en_cours')
    reservation.statut = 'terminee'
    reservation.save()
    return redirect('reservations:reservations_employe')

@login_required
@user_passes_test(is_employe)
def api_planning_employe(request):
    reservations = Reservation.objects.filter(employe=request.user).exclude(statut='annulee')

    events = []
    for r in reservations:
        events.append({
            'title': f"{r.service.nom} ({r.vehicule.plaque_immatric})",
            'start': r.heure_debut.isoformat(),
            'end': r.heure_fin.isoformat(),
            'url': f"/reservations/reservation/{r.id}/",  # à créer si tu veux voir les détails
            'color': '#0d6efd' if r.statut == 'en_cours' else '#198754' if r.statut == 'terminee' else '#6c757d'
        })
    
    return JsonResponse(events, safe=False)

@login_required
@user_passes_test(is_employe)
def emploi_temps(request):
    return render(request, 'reservations/planning.html')

@login_required
@user_passes_test(is_employe)
def detail_reservation_employe(request, id):
    reservation = get_object_or_404(
        Reservation.objects.select_related('client', 'vehicule', 'service'),
        id=id,
        employe=request.user
    )
    return render(request, 'reservations/detail_reservation.html', {
        'reservation': reservation
    })

@login_required
@user_passes_test(lambda u: u.role == 'gestionnaire')
def assigner_employe(request, id):
    reservation = get_object_or_404(Reservation, id=id, statut='en_attente')

    # Liste des employés (tu peux filtrer plus finement si besoin)
    employes = CustomUser.objects.filter(role='employe')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'annuler':
            reservation.statut = 'annulee'
            reservation.save()
            messages.warning(request, "Réservation annulée.")
            return redirect('reservations:liste_reservations_gestionnaire')

        elif action == 'assigner':
            employe_id = request.POST.get('employe')
            employe = get_object_or_404(CustomUser, id=employe_id, role='employe')
            reservation.employe = employe
            reservation.statut = 'assignee'
            reservation.save()
            messages.success(request, f"Réservation assignée à {employe.prenom} {employe.nom}.")
            return redirect('reservations:liste_reservations_gestionnaire')

    return render(request, 'reservations/assigner_employe.html', {
        'reservation': reservation,
        'employes': employes
    })

@login_required
@user_passes_test(lambda u: u.role == 'gestionnaire')
def liste_reservations_gestionnaire(request):
    reservations = Reservation.objects.select_related('client', 'vehicule', 'service').order_by('heure_debut')
    return render(request, 'reservations/liste_reservations.html', {
        'reservations': reservations
    })

def api_services_by_type_htmx(request):
    """Vue pour récupérer les services selon le type de véhicule sélectionné"""
    try:
        vehicule_id = request.GET.get('vehicule')
        
        if not vehicule_id:
            return render(request, 'reservations/parts/service_options.html', {
                'services': []
            })
        
        # Récupérer le véhicule avec gestion d'erreur
        try:
            vehicule = Vehicule.objects.get(id=vehicule_id)
        except ObjectDoesNotExist:
            return HttpResponse(
                "<select name='service' id='service-options' class='form-select'>"
                "<option value=''>Véhicule introuvable</option>"
                "</select>"
            )
        
        # Vérifier si le véhicule a un type
        if not hasattr(vehicule, 'type_vehicule'):
            # Si votre modèle utilise une autre structure, adaptez cette partie
            # Par exemple, si vous utilisez un champ 'type' au lieu de 'type_vehicule'
            services = Service.objects.filter(type=vehicule.type)
        else:
            # Récupérer les services pour ce type de véhicule
            services = Service.objects.filter(type_vehicule=vehicule.type_vehicule)
        
        return render(request, 'reservations/parts/service_options.html', {
            'services': services
        })
    
    except Exception as e:
        # En mode DEBUG uniquement, renvoyer l'erreur pour le diagnostic
        import traceback
        error_html = f"""
        <select name='service' id='service-options' class='form-select'>
          <option value=''>Erreur: {str(e)}</option>
        </select>
        """
        return HttpResponse(error_html)