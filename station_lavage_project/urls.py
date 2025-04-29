
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.http import HttpResponse
from station_lavage_project.views import home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('personnel/', include('personnel.urls', namespace='personnel')),
    path('services/', include('services.urls', namespace='services')),
    path('statistiques/', include('statistiques.urls', namespace='statistiques')),

    # 🔐 Modification de mot de passe
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    # Vues de mot de passe oublié
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Page d'accueil
    path('', home, name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

