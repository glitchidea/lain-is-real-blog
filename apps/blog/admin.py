from django.contrib import admin
from .models import Category, Post, Image
from django.utils.html import format_html


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
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    filter_horizontal = ('categories',)
    save_on_top = True
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt'),
            'description': 'İçerik alanına istediğiniz satıra resim eklemek için editör araç çubuğundaki "Resim" butonunu kullanabilirsiniz. Resmi ekledikten sonra boyutunu ve hizalamasını ayarlayabilirsiniz. Otomatik boyutlandırma seçenekleri ile görselin kalitesini koruyabilirsiniz.'
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'featured_image_caption'),
            'classes': ('collapse',)
        }),
        ('Categorization', {
            'fields': ('categories', 'tags')
        }),
        ('Publishing', {
            'fields': ('status', 'published_at', 'is_featured', 'allow_comments', 'created_at', 'updated_at'),
            'description': 'Yazınızı hemen yayınlamak için "Yayınlandı" seçeneğini kullanın. İleri bir tarihte yayınlamak için "Yayınlandı" seçeneğini seçin ve "Yayın Tarihi" alanına istediğiniz tarih ve saati girin. Yazı belirtilen tarih ve saatte otomatik olarak görünür olacaktır.'
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        css = {
            'all': ['css/admin-customizations.css']
        }
        js = ['js/admin-enhancements.js']
    
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


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Admin configuration for Image model."""
    list_display = ('title', 'file', 'image_display', 'uploader', 'created_at')
    search_fields = ('title', 'alt_text')
    list_filter = ('uploader', 'created_at')
    readonly_fields = ('created_at',)
    
    def image_display(self, obj):
        """Display the image as thumbnail."""
        if obj.file:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                              obj.file.url)
        return '—'
    
    image_display.short_description = 'Preview'
