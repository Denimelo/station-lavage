# reservations/urls.py

from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('client/', views.liste_reservations_client, name='reservations_client'),
    path('nouvelle/', views.creer_reservation, name='creer_reservation'),
    path('reservation/<int:id>/suivi/', views.suivi_reservation, name='suivi_reservation'),
    path('reservation/<int:id>/evaluer/', views.evaluer_reservation, name='evaluer_reservation'),
    path('employe/reservations/', views.reservations_employe, name='reservations_employe'),
    path('employe/reservation/<int:id>/commencer/', views.commencer_service, name='commencer_service'),
    path('employe/reservation/<int:id>/terminer/', views.terminer_service, name='terminer_service'),
    path('employe/api/planning/', views.api_planning_employe, name='api_planning_employe'),
    path('employe/emploi-temps/', views.emploi_temps, name='emploi_temps'),
    path('employe/reservation/<int:id>/', views.detail_reservation_employe, name='detail_reservation_employe'),
    path('gestionnaire/reservation/<int:id>/assigner/', views.assigner_employe, name='assigner_employe'),
    path('gestionnaire/reservations/', views.liste_reservations_gestionnaire, name='liste_reservations_gestionnaire'),
    # API pour HTMX
    path('api/services-by-type/', views.api_services_by_type_htmx, name='api_services_by_type_htmx'),
]
