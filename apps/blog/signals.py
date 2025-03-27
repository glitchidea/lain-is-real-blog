from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Post, Category
from django.utils.text import slugify
from django.utils import timezone


@receiver(pre_save, sender=Post)
def set_published_date(sender, instance, **kwargs):
    """Set published_at date when a post is published for the first time."""
    try:
        # Get the existing post if it exists
        old_instance = Post.objects.get(pk=instance.pk)
        
        # If the post status is changed from draft to published
        if old_instance.status != instance.status and instance.status == Post.Status.PUBLISHED:
            if not instance.published_at:
                instance.published_at = timezone.now()
    except Post.DoesNotExist:
        # For new posts, if status is published but no published_at date
        if instance.status == Post.Status.PUBLISHED and not instance.published_at:
            instance.published_at = timezone.now()


@receiver(pre_save, sender=Category)
def set_category_slug(sender, instance, **kwargs):
    """Generate slug for a category if not provided."""
    if not instance.slug:
        instance.slug = slugify(instance.name)
        
        # Check for uniqueness
        original_slug = instance.slug
        counter = 1
        while Category.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1 