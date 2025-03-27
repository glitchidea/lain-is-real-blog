from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import MediaFile, GalleryItem
import os


@receiver(pre_delete, sender=MediaFile)
def delete_media_file(sender, instance, **kwargs):
    """Delete the actual file when a MediaFile instance is deleted."""
    if instance.file:
        # Check if the file exists on disk
        if os.path.isfile(instance.file.path):
            # Delete the file
            os.remove(instance.file.path)


@receiver(post_save, sender=MediaFile)
def update_file_metadata(sender, instance, created, **kwargs):
    """Update file metadata after the MediaFile is saved."""
    # Only do this for newly created files to avoid infinite recursion
    if created and instance.file:
        # Update the file size if not set
        if not instance.file_size and hasattr(instance.file, 'size'):
            instance.file_size = instance.file.size
            
            # Save without triggering this signal again
            MediaFile.objects.filter(pk=instance.pk).update(file_size=instance.file_size)
        
        # Set a title if not provided
        if not instance.title:
            filename = os.path.basename(instance.file.name)
            base_name = os.path.splitext(filename)[0]
            
            # Clean up the base name (replace underscores with spaces, title case)
            clean_title = base_name.replace('_', ' ').replace('-', ' ').title()
            
            # Update the title without triggering this signal again
            MediaFile.objects.filter(pk=instance.pk).update(title=clean_title) 