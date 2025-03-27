from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for user profiles."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    
    fieldsets = (
        (None, {'fields': ('avatar',)}),
        ('Personal Information', {'fields': ('bio', 'location', 'birth_date')}),
        ('Social Media', {'fields': ('website', 'twitter', 'linkedin', 'github')}),
        ('Preferences', {'fields': ('newsletter_subscription',)}),
    )


class CustomUserAdmin(UserAdmin):
    """Customized User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 
                    'is_staff', 'avatar_display', 'date_joined', 'post_count')
    list_select_related = ('profile',)
    
    def avatar_display(self, obj):
        """Display user avatar as thumbnail."""
        if hasattr(obj, 'profile') and obj.profile.avatar:
            return format_html('<img src="{}" width="30" height="30" style="border-radius: 50%;" />', 
                              obj.profile.avatar.url)
        return format_html('<span style="font-size:1.5em;">👤</span>')
    
    avatar_display.short_description = 'Avatar'
    
    def post_count(self, obj):
        """Display the number of posts by user."""
        count = obj.blog_posts.count()
        if count > 0:
            url = f"/admin/blog/post/?author__id__exact={obj.id}"
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0'
    
    post_count.short_description = 'Posts'
    
    def get_inline_instances(self, request, obj=None):
        """Only show inline profile if an user exists."""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
