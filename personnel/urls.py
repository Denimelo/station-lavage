from django.urls import path
from .views import liste_employes, profil_employe, profil_gestionnaire, ajouter_employe, toggle_activation_employe, recompenser_employe, detail_employe, historique_employe,liste_clients, detail_client

app_name = 'personnel'

urlpatterns = [
    path('employe/', profil_employe, name='profil_employe'),
    path('gestionnaire/', profil_gestionnaire, name='profil_gestionnaire'),
    path('gestionnaire/employes/', liste_employes, name='liste_employes'),
    path('gestionnaire/employes/ajouter/', ajouter_employe, name='ajouter_employe'),
    path('gestionnaire/employes/<int:employe_id>/toggle/', toggle_activation_employe, name='toggle_employe'),
    path('gestionnaire/employes/<int:employe_id>/recompenser/', recompenser_employe, name='recompenser_employe'),
    path('gestionnaire/employes/<int:employe_id>/', detail_employe, name='detail_employe'),
    path('gestionnaire/employes/<int:employe_id>/historique/', historique_employe, name='historique_employe'),
    path('gestionnaire/clients/', liste_clients, name='liste_clients'),
    path('gestionnaire/clients/<int:client_id>/', detail_client, name='detail_client')
]