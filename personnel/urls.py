from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    path('employe/', views.profil_employe, name='profil_employe'),
    path('gestionnaire/', views.profil_gestionnaire, name='profil_gestionnaire'),
]