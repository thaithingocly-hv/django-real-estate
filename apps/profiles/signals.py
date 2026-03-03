import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from realEstate.settings.base import AUTH_USER_MODEL
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     logger.info(f"Profile saved for user: {instance.username}")


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()
        logger.info(f"Profile saved for user: {instance.username}")


# có thể thay thế signal bằng service layer
