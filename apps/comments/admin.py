from django.contrib import admin
from .models import Comment, Reply
from django.utils.html import format_html


class ReplyInline(admin.TabularInline):
    """Inline admin for replies in a comment."""
    model = Reply
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('content', 'author', 'is_approved', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""
    list_display = ('truncated_content', 'author', 'post_link', 'created_at', 
                    'is_approved', 'reply_count_display')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReplyInline]
    actions = ['approve_comments', 'reject_comments']
    
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def truncated_content(self, obj):
        """Display truncated comment content."""
        if len(obj.content) > 75:
            return obj.content[:75] + '...'
        return obj.content
    
    truncated_content.short_description = 'Comment'
    
    def post_link(self, obj):
        """Display a link to the post."""
        return format_html('<a href="{}">{}</a>', 
                          obj.post.get_absolute_url(), obj.post.title[:40])
    
    post_link.short_description = 'Post'
    
    def reply_count_display(self, obj):
        """Display the number of replies with a link to filter them."""
        count = obj.reply_count
        if count > 0:
            return format_html('{} replies', count)
        return 'No replies'
    
    reply_count_display.short_description = 'Replies'
    
    def approve_comments(self, request, queryset):
        """Approve selected comments."""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments were approved.')
    
    approve_comments.short_description = 'Approve selected comments'
    
    def reject_comments(self, request, queryset):
        """Reject selected comments."""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments were rejected.')
    
    reject_comments.short_description = 'Reject selected comments'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """Admin configuration for Reply model."""
    list_display = ('truncated_content', 'author', 'comment_link', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author__username', 'comment__content')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_replies', 'reject_replies']
    
    fieldsets = (
        (None, {
            'fields': ('comment', 'author', 'content', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def truncated_content(self, obj):
        """Display truncated reply content."""
        if len(obj.content) > 75:
            return obj.content[:75] + '...'
        return obj.content
    
    truncated_content.short_description = 'Reply'
    
    def comment_link(self, obj):
        """Display a link to the original comment."""
        if len(obj.comment.content) > 40:
            content = obj.comment.content[:40] + '...'
        else:
            content = obj.comment.content
        
        post_url = obj.comment.post.get_absolute_url()
        return format_html('<a href="{}#comment-{}">{}</a>', 
                          post_url, obj.comment.id, content)
    
    comment_link.short_description = 'In reply to'
    
    def approve_replies(self, request, queryset):
        """Approve selected replies."""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} replies were approved.')
    
    approve_replies.short_description = 'Approve selected replies'
    
    def reject_replies(self, request, queryset):
        """Reject selected replies."""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} replies were rejected.')
    
    reject_replies.short_description = 'Reject selected replies'
