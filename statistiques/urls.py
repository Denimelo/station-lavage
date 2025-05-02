from django.urls import path
from . import views

app_name = 'statistiques'

urlpatterns = [
    path('', views.tableau_bord, name='tableau_bord'),
    path('static_dash', views.static_dashboard, name='static_dashboard'),
    path('generer-rapport/', views.generer_rapport, name='generer_rapport'),
    path('rapports/', views.liste_rapports, name='liste_rapports'),
    path('rapports/<int:rapport_id>/', views.detail_rapport, name='detail_rapport'),
]