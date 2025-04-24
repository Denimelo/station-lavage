from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('mes-vehicules/', views.mes_vehicules, name='liste_vehicules'),
    path('ajouter/', views.ajouter_vehicule, name='ajouter_vehicule'),
    path('modifier/<int:pk>/', views.modifier_vehicule, name='modifier_vehicule'),
    path('supprimer/<int:pk>/', views.supprimer_vehicule, name='supprimer_vehicule'),
]
