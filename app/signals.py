from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import UserSession

@receiver(user_logged_out)
def clear_session(sender, request, user, **kwargs):
    UserSession.objects.filter(user=user).delete()
