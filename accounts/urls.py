from django.urls import path
from .views import register_client, login_view, logout_view, profile_view, dashboard, dashboard_client, dashboard_gestionnaire, dashboard_employe, confirm_email, resend_confirmation
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_client, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('client/dashboard/', dashboard_client, name='dashboard_client'),
    path('employe/dashboard/', dashboard_employe, name='dashboard_employe'),
    path('gestionnaire/dashboard/', dashboard_gestionnaire, name='dashboard_gestionnaire'),
    
    # Nouvelles routes pour la confirmation d'email
    path('confirm-email/<uuid:token>/', confirm_email, name='confirm_email'),
    path('resend-confirmation/', resend_confirmation, name='resend_confirmation'),
    
    # Routes pour la réinitialisation de mot de passe
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/email/password_reset_email.html',
            subject_template_name='accounts/email/password_reset_subject.txt'
        ), 
        name='password_reset'
    ),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ), 
        name='password_reset_confirm'
    ),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ), 
        name='password_reset_complete'
    ),
]
