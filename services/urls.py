from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.liste_services, name='liste_services'),
    path('ajouter/', views.ajouter_service, name='ajouter_service'),
    path('<int:id>/modifier/', views.modifier_service, name='modifier_service'),
    path('<int:id>/supprimer/', views.supprimer_service, name='supprimer_service'),
]