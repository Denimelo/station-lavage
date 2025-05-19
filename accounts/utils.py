import uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .models import EmailConfirmation

def send_confirmation_email(user, request):
    """Envoie un email de confirmation d'inscription"""
    # Créer ou récupérer le token de confirmation
    confirmation, created = EmailConfirmation.objects.get_or_create(user=user)
    if not created:
        # Régénérer un token si on renvoie l'email
        confirmation.token = uuid.uuid4()
        confirmation.is_confirmed = False
        confirmation.created_at = timezone.now()
        confirmation.save()
    
    # Construire l'URL de confirmation
    confirm_url = request.build_absolute_uri(
        reverse('confirm_email', kwargs={'token': confirmation.token})
    )
    
    # Contenu de l'email
    context = {
        'user': user,
        'confirm_url': confirm_url,
        'expiration_hours': 24,
    }
    
    html_message = render_to_string('accounts/email/confirmation_email.html', context)
    plain_message = strip_tags(html_message)
    
    # Envoi de l'email
    send_mail(
        subject='Confirmez votre inscription - AquaNova SARL',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
    )

def send_password_reset_email(user, token, request):
    """Envoie un email de réinitialisation de mot de passe"""
    reset_url = request.build_absolute_uri(
        reverse('password_reset_confirm', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        })
    )
    
    context = {
        'user': user,
        'reset_url': reset_url,
        'expiration_hours': 24,
    }
    
    html_message = render_to_string('accounts/email/password_reset_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject='Réinitialisation de votre mot de passe - AquaNova SARL',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
    )