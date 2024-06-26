from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from drug_insights_hub.accounts.models import UserProfile

USER_MODEL: Type[User] = get_user_model()


@receiver(post_save, sender=USER_MODEL)
def create_and_save_user_profile(sender, instance, created, **kwargs) -> None:
    if created:
        UserProfile.objects.get_or_create(user=instance)
