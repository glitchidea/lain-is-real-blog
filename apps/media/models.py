from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid
import os
from django.core.validators import FileExtensionValidator


def get_upload_path(instance, filename):
    """Generate upload path for media files."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', instance.upload_type, filename)


class MediaFile(models.Model):
    """Model for storing various media files."""
    
    class UploadType(models.TextChoices):
        IMAGE = 'images', _("Image")
        DOCUMENT = 'documents', _("Document")
        VIDEO = 'videos', _("Video")
        AUDIO = 'audio', _("Audio")
    
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    file = models.FileField(
        _("File"), 
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg', 'pdf', 'doc', 'docx', 'mp4', 'mp3']
        )]
    )
    upload_type = models.CharField(
        _("Type"), 
        max_length=20, 
        choices=UploadType.choices, 
        default=UploadType.IMAGE
    )
    alt_text = models.CharField(_("Alt Text"), max_length=255, blank=True)
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='media_files',
        verbose_name=_("Uploaded By")
    )
    file_size = models.PositiveIntegerField(_("File Size (bytes)"), default=0)
    mime_type = models.CharField(_("MIME Type"), max_length=100, blank=True)
    is_public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Media File")
        verbose_name_plural = _("Media Files")
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"{self.upload_type.capitalize()} {self.id}"
    
    def save(self, *args, **kwargs):
        # Set file size if file is provided
        if self.file and not self.file_size and hasattr(self.file, 'size'):
            self.file_size = self.file.size
            
        # Set MIME type based on file extension
        if self.file and not self.mime_type:
            ext = os.path.splitext(self.file.name)[1].lower()
            mime_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.pdf': 'application/pdf',
                '.doc': 'application/msword',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.mp4': 'video/mp4',
                '.mp3': 'audio/mpeg',
            }
            self.mime_type = mime_map.get(ext, 'application/octet-stream')
        
        super().save(*args, **kwargs)
    
    @property
    def file_extension(self):
        """Return the file extension."""
        return os.path.splitext(self.file.name)[1].lower()[1:]
    
    @property
    def human_readable_size(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024 or unit == 'GB':
                return f"{size:.1f} {unit}"
            size /= 1024
    
    @property
    def is_image(self):
        """Check if the file is an image."""
        return self.upload_type == self.UploadType.IMAGE
    
    @property
    def thumbnail_url(self):
        """Return URL for thumbnail if it's an image."""
        if self.is_image:
            return self.file.url
        # Return placeholder based on file type
        return f"/static/img/{self.upload_type}-placeholder.png"


class Gallery(models.Model):
    """Model for creating image galleries."""
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='galleries',
        verbose_name=_("Created By")
    )
    is_public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    @property
    def cover_image(self):
        """Return the first image in the gallery as cover image."""
        first_item = self.items.filter(media_file__upload_type=MediaFile.UploadType.IMAGE).first()
        if first_item:
            return first_item.media_file
        return None
    
    @property
    def item_count(self):
        """Return the number of items in the gallery."""
        return self.items.count()


class GalleryItem(models.Model):
    """Model representing an item in a gallery."""
    gallery = models.ForeignKey(
        Gallery, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name=_("Gallery")
    )
    media_file = models.ForeignKey(
        MediaFile, 
        on_delete=models.CASCADE, 
        related_name='gallery_items',
        verbose_name=_("Media File")
    )
    caption = models.CharField(_("Caption"), max_length=255, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Gallery Item")
        verbose_name_plural = _("Gallery Items")
        ordering = ['order', 'created_at']
        unique_together = ('gallery', 'media_file')

    def __str__(self):
        return f"{self.media_file} in {self.gallery}"
