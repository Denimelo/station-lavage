from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, EvaluationForm, JustificationAnnulationForm, AssignationForm
from .models import Evaluation,Vehicule, Service, Reservation
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime

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
        return redirect('reservations:suivi_reservation', id=reservation.id)

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
def commencer_service(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, employe=request.user)
    reservation.statut = 'en_cours'
    reservation.temps_reel_debut = now()
    reservation.save()
    return redirect('reservations:reservations_employe')

@login_required
@user_passes_test(is_employe)
def terminer_service(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, employe=request.user)
    reservation.statut = 'terminee'
    reservation.temps_reel_fin = now()
    reservation.save()

    # Ajouter points fidélité ici si nécessaire
    if reservation.client:
        reservation.client.points_fidelite += 10
        reservation.client.save()

    return redirect('reservations:reservations_employe')

@login_required
@user_passes_test(is_employe)
def api_planning_employe(request):
    reservations = Reservation.objects.filter(
        employe=request.user
    ).exclude(
        statut='annulee'
    ).exclude(
        heure_debut__isnull=True, heure_fin__isnull=True
    )

    events = []
    for r in reservations:
        events.append({
            'title': f"{r.service.nom} ({r.vehicule.plaque_immatric})",
            'start': r.heure_debut.isoformat(),
            'end': r.heure_fin.isoformat(),
            'url': f"/reservations/reservation/{r.id}/",  # page de détail employé/gestionnaire
            'color': (
                '#0d6efd' if r.statut == 'en_cours'
                else '#198754' if r.statut == 'terminee'
                else '#6c757d'  # assignée ou autre
            )
        })

    return JsonResponse(events, safe=False)

@login_required
@user_passes_test(lambda u: u.role == 'gestionnaire')
def api_employes_disponibles(request):
    heure_debut = request.GET.get('heure_debut')
    if not heure_debut:
        return JsonResponse({'error': 'heure_debut manquant'}, status=400)

    heure_debut = parse_datetime(heure_debut)
    if not heure_debut:
        return JsonResponse({'error': 'format invalide'}, status=400)

    # Récupère la durée estimée de la réservation courante (via param GET ou session)
    reservation_id = request.GET.get('reservation_id')
    if not reservation_id:
        return JsonResponse({'error': 'reservation_id manquant'}, status=400)

    from .models import Reservation
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    heure_fin = heure_debut + reservation.duree_estimee()

    # Filtrer les employés occupés
    employes = CustomUser.objects.filter(role='employe', is_active=True)
    disponibles = []

    for emp in employes:
        conflits = Reservation.objects.filter(
            employe=emp,
            statut__in=['assignee', 'en_cours'],
            heure_debut__lt=heure_fin,
            heure_fin__gt=heure_debut
        )
        if not conflits.exists():
            disponibles.append({
                'id': emp.id,
                'nom': f"{emp.prenom} {emp.nom}"
            })

    return JsonResponse(disponibles, safe=False)

@login_required
@user_passes_test(is_employe)
def emploi_temps(request):
    return render(request, 'reservations/planning.html')

@login_required
@user_passes_test(lambda u: u.role == 'gestionnaire')
def assigner_employe(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    if request.method == 'POST':
        form = AssignationForm(request.POST, reservation=reservation)
        if form.is_valid():
            employe = form.cleaned_data['employe']
            heure_debut = form.cleaned_data['heure_debut']
            reservation.employe = employe
            reservation.heure_debut = heure_debut
            reservation.heure_fin = heure_debut + reservation.duree_estimee()
            reservation.statut = 'assignee'
            reservation.save()
            messages.success(request, f"Réservation assignée à {employe}.")
            return redirect('reservations/liste_reservations.html')
    else:
        form = AssignationForm(reservation=reservation)

    return render(request, 'reservations/assigner_employe.html', {
        'reservation': reservation,
        'form': form
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
    
@login_required
def detail_reservation_employe(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, employe=request.user)
    return render(request, 'personnel/employe/detail_reservation.html', {'reservation': reservation})

@login_required
def detail_reservation_gestionnaire(request, reservation_id):
    if request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'personnel/gestionnaire/detail_reservation.html', {'reservation': reservation})

    
@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Autoriser client ou gestionnaire
    if request.user != reservation.client and request.user.role != 'gestionnaire':
        return redirect('dashboard_client')

    if request.method == 'POST':
        form = JustificationAnnulationForm(request.POST)
        if form.is_valid():
            reservation.commentaire_annulation = form.cleaned_data['commentaire']
            reservation.statut = 'annulee'
            reservation.save()
            return redirect('reservations:liste_reservations_client' if request.user.role == 'client' else 'personnel:liste_reservations')
    else:
        form = JustificationAnnulationForm()

    return render(request, 'reservations/annuler_reservation.html', {'reservation': reservation, 'form': form})