from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile


def user_avatar_path(instance, filename):
    """
    Her kullanıcı için ayrı dizin oluşturan fonksiyon.
    Örnek: 'profiles/avatars/user_1/profile.jpg'
    """
    # Dosya uzantısını al
    ext = filename.split('.')[-1]
    # Dosya adını standardize et
    filename = f"avatar.{ext}"
    # Kullanıcıya özel yolu döndür
    return f'profiles/avatars/user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    """Model representing a user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(_("Avatar"), upload_to=user_avatar_path, blank=True, null=True)
    bio = models.TextField(_("Bio"), blank=True, help_text=_("A brief description about yourself"))
    website = models.URLField(_("Website"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    github = models.URLField(_("GitHub"), blank=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    birth_date = models.DateField(_("Birth Date"), blank=True, null=True)
    newsletter_subscription = models.BooleanField(_("Subscribe to Newsletter"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        """Profil kaydedilirken avatar resmini sıkıştır ve boyutlandır."""
        is_new = self.pk is None
        
        # Önce modeli kaydet ki dosya yolları oluşsun
        super().save(*args, **kwargs)
        
        # Eğer avatar varsa ve dosya sistem üzerinde mevcutsa işle
        if self.avatar and hasattr(self.avatar, 'path') and os.path.exists(self.avatar.path):
            try:
                self.compress_and_resize_avatar()
            except Exception as e:
                # Hata olsa bile kayıt işlemini devam ettir
                import logging
                logger = logging.getLogger('django')
                logger.error(f"Avatar işleme hatası: {e}")
    
    def compress_and_resize_avatar(self):
        """Avatar resmini optimize eder, boyutlandırır ve sıkıştırır."""
        # Eğer avatar yoksa işlem yapma
        if not self.avatar or not self.avatar.name:
            return
            
        # Eğer dosya henüz fiziksel olarak var değilse (yeni yüklendi ama henüz kaydedilmedi)
        # veya dosya yolu boş ise işlem yapma
        try:
            img = Image.open(self.avatar.path)
            
            # Mevcut format
            img_format = self.avatar.path.split('.')[-1].upper()
            if img_format == 'JPG':
                img_format = 'JPEG'
            
            # Boyut kontrolü ve yeniden boyutlandırma
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
            
            # Kalite düşürme ve sıkıştırma
            output = BytesIO()
            
            # PNG için sıkıştırma yöntemi
            if img_format == 'PNG':
                img = img.convert('RGBA')
                img.save(output, format=img_format, optimize=True, quality=85)
            # JPEG için sıkıştırma yöntemi
            else:
                img = img.convert('RGB')
                img.save(output, format='JPEG', optimize=True, quality=85)
            
            output.seek(0)
            
            # Mevcut dosya adını al
            filename = os.path.basename(self.avatar.name)
            
            # Eski dosyayı sil
            self.avatar.delete(save=False)
            
            # Yeni dosyayı kaydet
            self.avatar.save(filename, ContentFile(output.getvalue()), save=False)
            
            # Değişiklikleri kaydet
            super().save(update_fields=['avatar'])
        except (IOError, OSError, ValueError) as e:
            # Dosya işleme hatası - günlüğe kaydet ve devam et
            import logging
            logger = logging.getLogger('django')
            logger.error(f"Avatar işleme hatası: {e}")
            # Hata olsa bile işlemi durdurmayalım
    
    @property
    def full_name(self):
        """Return user's full name or username if not available."""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    @property
    def social_links(self):
        """Return a list of user's social links."""
        links = []
        if self.website:
            links.append({"name": "Website", "url": self.website, "icon": "fas fa-globe"})
        if self.twitter:
            links.append({"name": "Twitter", "url": self.twitter, "icon": "fab fa-twitter"})
        if self.linkedin:
            links.append({"name": "LinkedIn", "url": self.linkedin, "icon": "fab fa-linkedin"})
        if self.github:
            links.append({"name": "GitHub", "url": self.github, "icon": "fab fa-github"})
        return links
