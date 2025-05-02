from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib import messages

from .models import RapportPeriodique, ServicePopularite, PerformanceEmploye
from .forms import RapportForm
from reservations.models import Reservation, Evaluation
from services.models import Service
from clients.models import Vehicule
from accounts.models import CustomUser

def is_gestionnaire(user):
    return user.is_authenticated and user.role == 'gestionnaire'


@login_required
@user_passes_test(is_gestionnaire)
def static_dashboard(request):
    return render(request, 'statistiques/static_dashboard.html')


@login_required
@user_passes_test(is_gestionnaire)
def tableau_bord(request):
    # Récupération de la date actuelle
    aujourdhui = timezone.now().date()
    debut_semaine = aujourdhui - timedelta(days=aujourdhui.weekday())
    debut_mois = aujourdhui.replace(day=1)
    
    # Statistiques journalières
    stats_jour = Reservation.objects.filter(
        created_at__date=aujourdhui
    ).aggregate(
        nb_reservations=Count('id'),
        nb_terminees=Count('id', filter=Q(statut='terminee')),
        revenus=Sum('service__prix', filter=Q(statut='terminee')),
    )
    
    # Statistiques hebdomadaires
    stats_semaine = Reservation.objects.filter(
        created_at__date__gte=debut_semaine,
        created_at__date__lte=aujourdhui
    ).aggregate(
        nb_reservations=Count('id'),
        nb_terminees=Count('id', filter=Q(statut='terminee')),
        revenus=Sum('service__prix', filter=Q(statut='terminee')),
    )
    
    # Statistiques mensuelles
    stats_mois = Reservation.objects.filter(
        created_at__date__gte=debut_mois,
        created_at__date__lte=aujourdhui
    ).aggregate(
        nb_reservations=Count('id'),
        nb_terminees=Count('id', filter=Q(statut='terminee')),
        revenus=Sum('service__prix', filter=Q(statut='terminee')),
    )
    
    # Services les plus populaires ce mois-ci
    services_populaires = Service.objects.filter(
        reservations__created_at__date__gte=debut_mois,
        reservations__created_at__date__lte=aujourdhui
    ).annotate(
        nombre_reservations=Count('reservations'),
        revenus=Sum('prix', filter=Q(reservations__statut='terminee'))
    ).order_by('-nombre_reservations')[:5]
    
    # Employés les plus performants
    employes_performances = CustomUser.objects.filter(
        role='employe',
        reservations_employe__created_at__date__gte=debut_mois,
        reservations_employe__created_at__date__lte=aujourdhui
    ).annotate(
        nb_services=Count('reservations_employe', filter=Q(reservations_employe__statut='terminee')),
        note_moyenne=Avg('reservations_employe__evaluation__note')
    ).order_by('-nb_services')[:5]
    
    context = {
        'stats_jour': stats_jour,
        'stats_semaine': stats_semaine,
        'stats_mois': stats_mois,
        'services_populaires': services_populaires,
        'employes_performances': employes_performances,
        'date_aujourdhui': aujourdhui,
    }
    
    return render(request, 'statistiques/tableau_bord.html', context)

@login_required
@user_passes_test(is_gestionnaire)
def generer_rapport(request):
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            type_periode = form.cleaned_data['type_periode']
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']
            
            # Création du rapport
            rapport = RapportPeriodique(
                type_periode=type_periode,
                date_debut=date_debut,
                date_fin=date_fin
            )
            
            # Récupération des statistiques
            reservations = Reservation.objects.filter(
                created_at__gte=date_debut,
                created_at__lte=date_fin
            )
            
            rapport.nombre_reservations = reservations.count()
            rapport.nombre_reservations_terminees = reservations.filter(statut='terminee').count()
            rapport.nombre_reservations_annulees = reservations.filter(statut='annulee').count()
            rapport.revenu_total = reservations.filter(statut='terminee').aggregate(
                total=Sum('service__prix'))['total'] or 0
            
            rapport.nombre_employes_actifs = CustomUser.objects.filter(
                role='employe',
                is_active=True,
                reservations_employe__created_at__gte=date_debut,
                reservations_employe__created_at__lte=date_fin
            ).distinct().count()
            
            rapport.nombre_clients_actifs = CustomUser.objects.filter(
                role='client',
                reservations_client__created_at__gte=date_debut,
                reservations_client__created_at__lte=date_fin
            ).distinct().count()
            
            # Note moyenne des évaluations
            evaluations = Evaluation.objects.filter(
                reservation__created_at__gte=date_debut,
                reservation__created_at__lte=date_fin
            )
            if evaluations.exists():
                rapport.note_moyenne = evaluations.aggregate(avg=Avg('note'))['avg']
            
            # Calcul du taux d'occupation
            if rapport.nombre_employes_actifs > 0:
                duree_totale_services = reservations.filter(statut='terminee').aggregate(
                    total=Sum(F('heure_fin') - F('heure_debut')))['total'] or timedelta()
                
                # Conversion en heures
                duree_totale_heures = duree_totale_services.total_seconds() / 3600
                
                # Calcul des heures de travail théoriques sur la période (8h par jour par employé)
                jours_periode = (date_fin.date() - date_debut.date()).days + 1
                heures_theoriques = jours_periode * 8 * rapport.nombre_employes_actifs
                
                rapport.taux_occupation = (duree_totale_heures / heures_theoriques) * 100 if heures_theoriques > 0 else 0
            
            rapport.save()
            
            # Analyse des services les plus demandés
            services_stats = Service.objects.filter(
                reservations__created_at__gte=date_debut,
                reservations__created_at__lte=date_fin
            ).annotate(
                nb_res=Count('reservations'),
                revenu=Sum('prix', filter=Q(reservations__statut='terminee'))
            ).order_by('-nb_res')
            
            # Enregistrement des popularités des services
            for service in services_stats:
                pourcentage = (service.nb_res / rapport.nombre_reservations) * 100 if rapport.nombre_reservations > 0 else 0
                ServicePopularite.objects.create(
                    rapport=rapport,
                    service_id=service.id,
                    service_nom=service.nom,
                    service_type_vehicule=service.type_vehicule,
                    nombre_reservations=service.nb_res,
                    pourcentage=pourcentage,
                    revenu_genere=service.revenu or 0
                )
            
            # Analyse des performances des employés
            employes = CustomUser.objects.filter(
                role='employe',
                reservations_employe__created_at__gte=date_debut,
                reservations_employe__created_at__lte=date_fin
            ).distinct()
            
            for employe in employes:
                services_realises = Reservation.objects.filter(
                    employe=employe,
                    statut='terminee',
                    created_at__gte=date_debut,
                    created_at__lte=date_fin
                ).count()
                
                note_moy = Evaluation.objects.filter(
                    reservation__employe=employe,
                    reservation__created_at__gte=date_debut,
                    reservation__created_at__lte=date_fin
                ).aggregate(avg=Avg('note'))['avg'] or 0
                
                duree_travail = Reservation.objects.filter(
                    employe=employe,
                    statut='terminee',
                    heure_debut__isnull=False,
                    heure_fin__isnull=False,
                    created_at__gte=date_debut,
                    created_at__lte=date_fin
                ).aggregate(
                    total=Sum(F('heure_fin') - F('heure_debut'))
                )['total'] or timedelta()
                
                PerformanceEmploye.objects.create(
                    rapport=rapport,
                    employe=employe,
                    services_realises=services_realises,
                    note_moyenne=note_moy,
                    duree_travail_total=duree_travail
                )
            
            messages.success(request, f"Rapport {rapport.get_type_periode_display()} généré avec succès")
            return redirect('statistiques:detail_rapport', rapport_id=rapport.id)
    else:
        form = RapportForm()
    
    return render(request, 'statistiques/generer_rapport.html', {'form': form})

@login_required
@user_passes_test(is_gestionnaire)
def liste_rapports(request):
    rapports = RapportPeriodique.objects.all().order_by('-date_creation')
    return render(request, 'statistiques/liste_rapports.html', {'rapports': rapports})

@login_required
@user_passes_test(is_gestionnaire)
def detail_rapport(request, rapport_id):
    rapport = RapportPeriodique.objects.get(id=rapport_id)
    services_popularite = rapport.services_popularite.all()
    performances_employes = rapport.performances_employes.all()
    
    context = {
        'rapport': rapport,
        'services_popularite': services_popularite,
        'performances_employes': performances_employes,
    }
    
    return render(request, 'statistiques/detail_rapport.html', context)