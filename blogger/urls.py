"""
Blogger URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import PostSitemap, CategorySitemap, TagSitemap

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Blog URLs
    path('blog/', include('apps.blog.urls')),
    
    # Accounts URLs
    path('accounts/', include('apps.accounts.urls')),
    
    # Django AllAuth URLs
    path('accounts/', include('allauth.urls')),
    
    # Comments URLs
    path('comments/', include('apps.comments.urls')),
    
    # Media URLs
    path('media-manager/', include('apps.media.urls')),
    
    # CKEditor URLs
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # About page
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    
    # Privacy Policy
    path('privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    
    # Terms of Service
    path('terms/', TemplateView.as_view(template_name='terms.html'), name='terms'),
]

# Add debug toolbar URLs in debug mode
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
