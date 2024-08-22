# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BDUser

@receiver(post_save, sender=User)
def create_bd_user(sender, instance, created, **kwargs):
    if created:
        BDUser.objects.create(
            user=instance,
            user_tel=instance.phone_number,
            user_email=instance.email,
            user_role="user"  # Можно настроить роль по умолчанию
        )
