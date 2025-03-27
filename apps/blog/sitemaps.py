from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from taggit.models import Tag
from .models import Post, Category


class PostSitemap(Sitemap):
    """Sitemap for blog posts."""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """Return all published posts."""
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        """Return the last modification date of a post."""
        return obj.updated_at


class CategorySitemap(Sitemap):
    """Sitemap for blog categories."""
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        """Return all categories."""
        return Category.objects.all()

    def lastmod(self, obj):
        """Return the last modification date of a category."""
        return obj.updated_at


class TagSitemap(Sitemap):
    """Sitemap for blog tags."""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        """Return all tags that have posts."""
        return Tag.objects.all()

    def location(self, obj):
        """Return the URL for a tag."""
        return reverse('blog:tag', args=[obj.slug])


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        """Return all static page names."""
        return ['home', 'blog:post_list', 'blog:categories', 'blog:tags', 'blog:about', 
                'about', 'privacy', 'terms']

    def location(self, item):
        """Return the URL for a static page."""
        return reverse(item) 