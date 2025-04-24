# reservations/urls.py

from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('prendre/', views.prendre_rdv, name='prendre'),
    path('create/', views.create_reservation, name='create'),
    path('mes-reservations/', views.list_reservations, name='list'),
    path('employe/', views.reservations_employe, name='reservations_employe'),
    path('gestionnaire/', views.reservations_gestionnaire, name='reservations_gestionnaire'),
    path('assigner/<int:pk>/', views.assigner_employe, name='assigner_employe'),
]
