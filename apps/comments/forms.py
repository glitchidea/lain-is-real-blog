from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    """Form for creating and editing comments."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Share your thoughts about this article...'),
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        self.post = kwargs.pop('post', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_content(self):
        """Validate and clean the content field."""
        content = self.cleaned_data.get('content')
        
        # Check minimum length
        if len(content) < 3:
            raise forms.ValidationError(
                _("Comment is too short. Please write at least 3 characters.")
            )
            
        # Check maximum length
        if len(content) > 2000:
            raise forms.ValidationError(
                _("Comment is too long. Please keep it under 2000 characters.")
            )
            
        return content
    
    def save(self, commit=True):
        """Save the comment with the specified post and user."""
        comment = super().save(commit=False)
        
        # Set post and author
        if self.post:
            comment.post = self.post
        
        if self.user:
            comment.author = self.user
            
        if commit:
            comment.save()
            
        return comment


class ReplyForm(forms.ModelForm):
    """Form for creating replies to comments."""
    
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Write your reply...'),
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        self.comment = kwargs.pop('comment', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_content(self):
        """Validate and clean the content field."""
        content = self.cleaned_data.get('content')
        
        # Check minimum length
        if len(content) < 3:
            raise forms.ValidationError(
                _("Reply is too short. Please write at least 3 characters.")
            )
            
        # Check maximum length
        if len(content) > 1000:
            raise forms.ValidationError(
                _("Reply is too long. Please keep it under 1000 characters.")
            )
            
        return content
    
    def save(self, commit=True):
        """Save the reply with the specified comment and user."""
        reply = super().save(commit=False)
        
        # Set comment and author
        if self.comment:
            reply.comment = self.comment
        
        if self.user:
            reply.author = self.user
            
        if commit:
            reply.save()
            
        return reply


class CommentModerationForm(forms.ModelForm):
    """Form for moderating comments."""
    
    class Meta:
        model = Comment
        fields = ['is_approved']
        widgets = {
            'is_approved': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        super().__init__(*args, **kwargs)
        self.fields['is_approved'].label = _('Approve this comment')


class ReplyModerationForm(forms.ModelForm):
    """Form for moderating replies."""
    
    class Meta:
        model = Reply
        fields = ['is_approved']
        widgets = {
            'is_approved': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        super().__init__(*args, **kwargs)
        self.fields['is_approved'].label = _('Approve this reply') 