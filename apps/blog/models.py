from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from markdown_deux import markdown
import readtime
from taggit.managers import TaggableManager
import math
import uuid
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    """Model representing a blog category."""
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icon Class"), max_length=50, blank=True, help_text=_("Font Awesome icon class"))
    parent = models.ForeignKey('self', verbose_name=_("Parent Category"), on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(_("Order"), default=0)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])
    
    @property
    def post_count(self):
        return self.posts.filter(status=Post.Status.PUBLISHED).count()


class Post(models.Model):
    """Model representing a blog post."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _("Draft")
        PUBLISHED = 'published', _("Published")
    
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=200, unique=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='blog_posts')
    content = CKEditor5Field(_("Content"), config_name='default')
    content_html = models.TextField(_("Content HTML"), blank=True, editable=False)
    excerpt = models.TextField(_("Excerpt"), blank=True, help_text=_("A brief summary of the post. If left blank, it will be auto-generated from content."))
    featured_image = models.ImageField(_("Featured Image"), upload_to='blog/featured_images/%Y/%m/%d/', blank=True, null=True)
    featured_image_caption = models.CharField(_("Image Caption"), max_length=200, blank=True)
    status = models.CharField(_("Status"), max_length=10, choices=Status.choices, default=Status.DRAFT)
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"), related_name='posts')
    tags = TaggableManager(_("Tags"), blank=True)
    is_featured = models.BooleanField(_("Featured"), default=False)
    allow_comments = models.BooleanField(_("Allow Comments"), default=True)
    views_count = models.PositiveIntegerField(_("Views Count"), default=0)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    published_at = models.DateTimeField(_("Published At"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            
            # Check for uniqueness
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # CKEditor kullanıyoruz, content_html artık gerekli değil
        # Ancak geriye dönük uyumluluk için content_html'i koruyalım
        self.content_html = self.content
        
        # Generate excerpt if not provided
        if not self.excerpt:
            # Strip HTML tags from content_html
            from django.utils.html import strip_tags
            text = strip_tags(self.content)
            
            # Truncate to set length
            excerpt_length = getattr(settings, 'BLOG_AUTO_EXCERPT_LENGTH', 150)
            if len(text) > excerpt_length:
                # Truncate at the last space before the limit
                self.excerpt = text[:excerpt_length].rsplit(' ', 1)[0] + '...'
            else:
                self.excerpt = text
        
        # Set published_at if publishing for the first time and no date is set
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
            
        # Status değişikliği durumunda, ileri tarihli yayınları kontrol et
        try:
            # Eğer bu nesne daha önce kaydedilmişse
            if self.pk:
                old_instance = Post.objects.get(pk=self.pk)
                # Eğer durum taslaktan yayına değiştirildiyse ve bir tarih belirtilmediyse 
                if old_instance.status != self.Status.PUBLISHED and self.status == self.Status.PUBLISHED:
                    if not self.published_at:
                        self.published_at = timezone.now()
        except Exception:
            pass
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    @property
    def reading_time(self):
        """Calculate the reading time of the post."""
        result = readtime.of_text(self.content)
        return math.ceil(result.minutes)
    
    @property
    def is_published(self):
        """Check if the post is published."""
        return self.status == self.Status.PUBLISHED
    
    @property
    def related_posts(self):
        """Get related posts based on categories and tags."""
        post_tags_ids = self.tags.values_list('id', flat=True)
        post_categories_ids = self.categories.values_list('id', flat=True)
        
        # Get posts with same tags or categories, excluding this post
        related_posts = Post.objects.filter(
            models.Q(tags__id__in=post_tags_ids) | 
            models.Q(categories__id__in=post_categories_ids),
            status=self.Status.PUBLISHED
        ).exclude(id=self.id).distinct()
        
        # Return up to 3 related posts
        return related_posts[:3]
    
    def increment_views(self):
        """Increment the view count for this post."""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Image(models.Model):
    """Model representing an image that can be used in blog posts."""
    title = models.CharField(_("Title"), max_length=200, blank=True)
    file = models.ImageField(_("File"), upload_to='blog/images/%Y/%m/%d/')
    alt_text = models.CharField(_("Alt Text"), max_length=200, blank=True)
    uploader = models.ForeignKey(User, verbose_name=_("Uploaded By"), on_delete=models.CASCADE, related_name='uploaded_images')
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title or f"Image {self.id}"
    
    @property
    def url(self):
        return self.file.url
