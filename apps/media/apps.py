from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.media'
    verbose_name = _('Media Management')
    
    def ready(self):
        """Import signal handlers when app is ready."""
        import apps.media.signals
