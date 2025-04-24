from django.urls import path
from . import views

app_name = 'statistiques'

urlpatterns = [
    # Exemple de route (à personnaliser plus tard)
    path('', views.dashboard_statistiques, name='dashboard'),
]