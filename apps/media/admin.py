from django.contrib import admin
from .models import MediaFile, Gallery, GalleryItem
from django.utils.html import format_html


class GalleryItemInline(admin.TabularInline):
    """Inline admin for gallery items."""
    model = GalleryItem
    extra = 1
    fields = ('media_file', 'caption', 'order', 'preview')
    readonly_fields = ('preview',)
    
    def preview(self, obj):
        """Display a thumbnail preview of the media file."""
        if obj.media_file and obj.media_file.is_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                              obj.media_file.file.url)
        elif obj.media_file:
            return obj.media_file.file_extension.upper()
        return '—'
    
    preview.short_description = 'Preview'


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """Admin configuration for MediaFile model."""
    list_display = ('title', 'upload_type', 'preview', 'uploaded_by', 
                    'file_size_display', 'is_public', 'created_at')
    list_filter = ('upload_type', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'alt_text')
    readonly_fields = ('file_size', 'mime_type', 'created_at', 'updated_at', 'preview_large')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'file', 'upload_type')
        }),
        ('Display Options', {
            'fields': ('alt_text', 'is_public')
        }),
        ('File Information', {
            'fields': ('file_size', 'human_readable_size', 'mime_type', 'preview_large'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview(self, obj):
        """Display a thumbnail preview of the media file."""
        if obj.is_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                              obj.file.url)
        return obj.file_extension.upper()
    
    preview.short_description = 'Preview'
    
    def preview_large(self, obj):
        """Display a larger preview of the media file."""
        if obj.is_image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;" />', 
                              obj.file.url)
        return format_html('<span class="file-icon">{}</span>', obj.file_extension.upper())
    
    preview_large.short_description = 'Preview'
    
    def file_size_display(self, obj):
        """Display human-readable file size."""
        return obj.human_readable_size
    
    file_size_display.short_description = 'Size'
    
    def human_readable_size(self, obj):
        """Display human-readable file size as a field."""
        return obj.human_readable_size
    
    human_readable_size.short_description = 'Size (human readable)'
    
    def save_model(self, request, obj, form, change):
        """Set uploaded_by if not already set."""
        if not change and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Admin configuration for Gallery model."""
    list_display = ('title', 'item_count', 'cover_preview', 'created_by', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description')
    inlines = [GalleryItemInline]
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'is_public')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cover_preview(self, obj):
        """Display a thumbnail of the gallery cover image."""
        cover = obj.cover_image
        if cover and cover.is_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', 
                              cover.file.url)
        return '—'
    
    cover_preview.short_description = 'Cover'
    
    def save_model(self, request, obj, form, change):
        """Set created_by if not already set."""
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
