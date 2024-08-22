# core/signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BDUser

# Настройка логирования
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_bd_user(sender, instance, created, **kwargs):
    if created:
        try:
            BDUser.objects.create(
                user=instance,
                user_tel=instance.phone_number,
                user_email=instance.email,
                user_role="user"  # Можно настроить роль по умолчанию
            )
            logger.info(f'User {instance.phone_number} successfully created in bd_user.')
        except Exception as e:
            logger.error(f'Error creating bd_user entry for user {instance.phone_number}: {e}')
