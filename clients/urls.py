from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('vehicules/', views.liste_vehicules, name='vehicules'),
    path('vehicule/ajouter/', views.ajouter_vehicule, name='ajouter_vehicule'),
    path('vehicule/<str:plaque>/modifier/', views.modifier_vehicule, name='modifier_vehicule'),
    path('vehicule/<str:plaque>/supprimer/', views.supprimer_vehicule, name='supprimer_vehicule'),
    path('vehicule/<str:plaque>/', views.details_vehicule, name='details_vehicule'),
]
