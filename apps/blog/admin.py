from django.contrib import admin
from .models import Category, Post, Image
from django.utils.html import format_html
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ('name', 'slug', 'parent', 'order', 'post_count_display')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    
    def post_count_display(self, obj):
        """Display the number of posts in a category."""
        count = obj.post_count
        url = f"/admin/blog/post/?categories__id__exact={obj.id}"
        return format_html('<a href="{}">{} posts</a>', url, count)
    
    post_count_display.short_description = 'Posts'


class CategoryInline(admin.TabularInline):
    """Inline admin for categories in post."""
    model = Post.categories.through
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for Post model."""
    list_display = ('title', 'author', 'status', 'featured_image_display', 
                    'published_date', 'is_featured', 'views_count', 'comments_count')
    list_filter = ('status', 'categories', 'created_at', 'published_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'featured_image_preview')
    filter_horizontal = ('categories',)
    save_on_top = True
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default', attrs={'style': 'width: 100%; min-height: 600px;'})},
    }
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt'),
            'description': '''
            <strong>Rich Content Editor Features:</strong>
            <ul>
                <li>Heading styles (H1-H3)</li>
                <li>Text formatting (bold, italic, underline, strikethrough)</li>
                <li>Font size and family</li>
                <li>Text and background color</li>
                <li>Alignment options</li>
                <li>Numbered and bulleted lists</li>
                <li>Indentation settings</li>
                <li>Link insertion</li>
                <li>Block quote</li>
                <li>Table insertion and editing</li>
                <li>Media embedding (YouTube, Vimeo, etc.)</li>
                <li>Horizontal line</li>
                <li>Source code editing</li>
                <li>Image upload and editing features:
                    <ul>
                        <li>Supported formats: JPEG, PNG, GIF, BMP, WEBP, TIFF, SVG</li>
                        <li>Maximum file size: 5MB</li>
                        <li>Image alignment and sizing</li>
                        <li>Alt text and caption addition</li>
                        <li>Image links</li>
                    </ul>
                </li>
            </ul>
            '''
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'featured_image_caption', 'featured_image_preview'),
            'description': '''
            <strong>Featured Image Guidelines:</strong>
            <ul>
                <li>Recommended dimensions: 1200x630 pixels (optimal for social sharing)</li>
                <li>Maximum file size: 5MB</li>
                <li>Supported formats: JPEG, PNG, GIF, BMP, WEBP</li>
                <li>Images will be automatically optimized</li>
                <li>Add a descriptive caption for better SEO</li>
            </ul>
            ''',
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('categories', 'tags')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at', 'is_featured', 'allow_comments', 'created_at', 'updated_at'),
            'description': 'You have been automatically selected as the author.'
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        css = {
            'all': [
                'css/admin-customizations.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            ]
        }
        js = [
            'js/admin-enhancements.js',
        ]
    
    def featured_image_display(self, obj):
        """Display the featured image as thumbnail."""
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                              obj.featured_image.url)
        return '—'
    
    featured_image_display.short_description = 'Image'
    
    def published_date(self, obj):
        """Display the published date formatted."""
        if obj.published_at:
            return obj.published_at.strftime('%Y-%m-%d %H:%M')
        return '—'
    
    published_date.short_description = 'Published At'
    
    def comments_count(self, obj):
        """Display the number of comments on a post."""
        count = obj.comments.count()
        if count > 0:
            url = f"/admin/comments/comment/?post__id__exact={obj.id}"
            return format_html('<a href="{}">{}</a>', url, count)
        return '0'
    
    comments_count.short_description = 'Comments'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch related."""
        return super().get_queryset(request).prefetch_related('categories', 'tags', 'comments')
    
    def save_model(self, request, obj, form, change):
        """Set author if not already set."""
        if not change and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def featured_image_preview(self, obj):
        """Display a larger preview of the featured image."""
        if obj.featured_image:
            return format_html('''
                <div style="margin: 10px 0;">
                    <img src="{}" style="max-width: 500px; max-height: 300px; object-fit: contain;" />
                    <p style="margin-top: 5px; color: #666;">
                        <strong>File name:</strong> {}<br>
                        <strong>File size:</strong> {:.2f} MB<br>
                        <strong>Dimensions:</strong> {}x{} pixels
                    </p>
                </div>
            ''', 
            obj.featured_image.url,
            obj.featured_image.name.split('/')[-1],
            obj.featured_image.size / (1024*1024),
            obj.featured_image.width if hasattr(obj.featured_image, 'width') else 'N/A',
            obj.featured_image.height if hasattr(obj.featured_image, 'height') else 'N/A'
            )
        return '—'
    
    featured_image_preview.short_description = 'Featured Image Preview'


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Admin configuration for Image model."""
    list_display = ('title', 'file', 'image_display', 'uploader', 'created_at')
    search_fields = ('title', 'alt_text')
    list_filter = ('uploader', 'created_at')
    readonly_fields = ('created_at', 'image_preview')
    
    fieldsets = (
        ('Image Details', {
            'fields': ('title', 'file', 'alt_text', 'image_preview'),
            'description': '''
            <strong>Image Upload Guidelines:</strong>
            <ul>
                <li>Supported formats: JPEG, PNG, GIF, BMP, WEBP, TIFF, SVG</li>
                <li>Maximum file size: 5MB</li>
                <li>Recommended dimensions: 1200x800 pixels or larger</li>
                <li>Images will be automatically optimized</li>
                <li>Please provide descriptive titles and alt text for better SEO</li>
            </ul>
            '''
        }),
        ('Metadata', {
            'fields': ('uploader', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_display(self, obj):
        """Display the image as thumbnail in list view."""
        if obj.file:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                              obj.file.url)
        return '—'
    
    image_display.short_description = 'Preview'
    
    def image_preview(self, obj):
        """Display a larger preview of the image in detail view."""
        if obj.file:
            return format_html('''
                <div style="margin: 10px 0;">
                    <img src="{}" style="max-width: 500px; max-height: 300px; object-fit: contain;" />
                    <p style="margin-top: 5px; color: #666;">
                        <strong>File name:</strong> {}<br>
                        <strong>File size:</strong> {:.2f} MB<br>
                        <strong>Dimensions:</strong> {}x{} pixels
                    </p>
                </div>
            ''', 
            obj.file.url,
            obj.file.name.split('/')[-1],
            obj.file.size / (1024*1024),
            obj.file.width if hasattr(obj.file, 'width') else 'N/A',
            obj.file.height if hasattr(obj.file, 'height') else 'N/A'
            )
        return '—'
    
    image_preview.short_description = 'Image Preview'
    
    def save_model(self, request, obj, form, change):
        """Set uploader automatically when saving."""
        if not obj.uploader:
            obj.uploader = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': [
                'css/admin-customizations.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            ]
        }
        js = [
            'js/admin-enhancements.js',
        ]
