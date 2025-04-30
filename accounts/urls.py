from django.urls import path
from .views import register_client, login_view, logout_view, profile_view, dashboard, dashboard_client, dashboard_gestionnaire

urlpatterns = [
    path('register/', register_client, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('client/dashboard/', dashboard_client, name='dashboard_client'),
    path('gestionnaire/dashboard/', dashboard_gestionnaire, name='dashboard_gestionnaire'),
]
