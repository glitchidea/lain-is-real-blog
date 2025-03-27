from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.blog.models import Post


class Comment(models.Model):
    """Model representing a comment on a blog post."""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name=_("Post")
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name=_("Author")
    )
    content = models.TextField(_("Content"))
    is_approved = models.BooleanField(_("Approved"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    @property
    def reply_count(self):
        """Return the number of replies to this comment."""
        return self.replies.count()


class Reply(models.Model):
    """Model representing a reply to a comment."""
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='replies', 
        verbose_name=_("Comment")
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='replies', 
        verbose_name=_("Author")
    )
    content = models.TextField(_("Content"))
    is_approved = models.BooleanField(_("Approved"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.author.username} to {self.comment}"
