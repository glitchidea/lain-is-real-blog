from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
import os
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when user is created or updated."""
    try:
        if created:
            UserProfile.objects.create(user=instance)
            logger.debug(f"Created new profile for user {instance.username}")
        else:
            # Just save the profile if it exists
            if hasattr(instance, 'profile'):
                instance.profile.save()
                logger.debug(f"Updated profile for user {instance.username}")
    except Exception as e:
        logger.error(f"Error in create_or_update_user_profile: {e}")


@receiver(pre_delete, sender=UserProfile)
def delete_profile_image(sender, instance, **kwargs):
    """Delete profile image file when profile is deleted."""
    if instance.avatar:
        # Check if the file exists on disk
        if os.path.isfile(instance.avatar.path):
            # Delete the file
            os.remove(instance.avatar.path) 