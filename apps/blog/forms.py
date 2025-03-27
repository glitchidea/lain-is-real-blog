from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Category, Image
from taggit.forms import TagField, TagWidget


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts."""
    
    # Custom TagField with custom widget
    tags = TagField(
        required=False, 
        help_text=_("Enter tags separated by commas."),
        widget=TagWidget(attrs={
            'class': 'form-control',
            'placeholder': _('Tags (comma-separated)'),
        })
    )
    
    # Use a MultipleChoiceField for categories with custom widget
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text=_("Select one or more categories for this post.")
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'featured_image', 
            'featured_image_caption', 'status', 'categories', 
            'tags', 'is_featured', 'allow_comments'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Post Title'),
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control markdown-editor',
                'rows': 15,
                'placeholder': _('Write your post content in Markdown...')
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('A brief summary of your post (optional). If left blank, it will be auto-generated.')
            }),
            'featured_image_caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Image caption (optional)')
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'title': _('Make it catchy and relevant to your content.'),
            'content': _('You can use Markdown for formatting. See the toolbar above for common formatting options.'),
            'excerpt': _('A brief summary of your post. If left blank, it will be auto-generated from content.'),
            'status': _('Draft = only you can see it. Published = visible to everyone.'),
            'is_featured': _('Featured posts appear on the home page in the featured section.'),
            'allow_comments': _('Allow readers to comment on this post.'),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        super().__init__(*args, **kwargs)
        
        # Make certain fields not required
        self.fields['excerpt'].required = False
        self.fields['featured_image'].required = False
        self.fields['featured_image_caption'].required = False
        
        # Initialize with custom behaviors
        self.fields['is_featured'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
        self.fields['allow_comments'].widget = forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
        
        # Add "Save as Draft" button state
        self.fields['save_as_draft'] = forms.BooleanField(
            required=False, 
            initial=True,
            widget=forms.HiddenInput()
        )
    
    def clean_content(self):
        """Validate and clean the content field."""
        content = self.cleaned_data.get('content')
        # Check minimum length
        if len(content) < 50:
            raise forms.ValidationError(
                _("Content is too short. Please write at least 50 characters.")
            )
        return content
    
    def save(self, commit=True, user=None):
        """Save the post with the specified user as author."""
        post = super().save(commit=False)
        
        # Set the author if provided and not already set
        if user and not post.author_id:
            post.author = user
        
        # Handle save_as_draft flag
        save_as_draft = self.cleaned_data.get('save_as_draft')
        if save_as_draft and not self.cleaned_data.get('status'):
            post.status = Post.Status.DRAFT
            
        if commit:
            post.save()
            self.save_m2m()  # Save many-to-many relationships
        
        return post


class ImageUploadForm(forms.ModelForm):
    """Form for uploading images to use in blog posts."""
    
    class Meta:
        model = Image
        fields = ['file', 'title', 'alt_text']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Image Title (optional)')
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Alternative Text for accessibility (optional)')
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make certain fields not required
        self.fields['title'].required = False
        self.fields['alt_text'].required = False
    
    def save(self, commit=True):
        """Save the image with the current user as uploader."""
        image = super().save(commit=False)
        
        if self.user and not image.uploaded_by_id:
            image.uploaded_by = self.user
            
        if commit:
            image.save()
            
        return image


class CategoryForm(forms.ModelForm):
    """Form for creating and editing blog categories."""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'icon', 'parent', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Category Name')
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('URL-friendly name (optional)')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Brief description of this category')
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Font Awesome icon class (e.g. fas fa-book)')
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }
        help_texts = {
            'slug': _('Leave blank to auto-generate from name.'),
            'icon': _('Font Awesome icon class, e.g. "fas fa-book". See fontawesome.com for options.'),
            'order': _('Categories are sorted by this number (lower numbers appear first).'),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        super().__init__(*args, **kwargs)
        
        # Make certain fields not required
        self.fields['slug'].required = False
        self.fields['description'].required = False
        self.fields['icon'].required = False
        self.fields['parent'].required = False
        
        # Exclude the current category from parent options (to prevent circular references)
        if self.instance.pk:
            self.fields['parent'].queryset = Category.objects.exclude(pk=self.instance.pk)


class SearchForm(forms.Form):
    """Form for searching blog posts."""
    
    q = forms.CharField(
        label=_("Search"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search articles...'),
            'aria-label': _('Search'),
        })
    )
    
    category = forms.ModelChoiceField(
        label=_("Category"),
        queryset=Category.objects.all(),
        required=False,
        empty_label=_("All Categories"),
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    tag = forms.CharField(
        label=_("Tag"),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Filter by tag'),
        })
    )
    
    sort = forms.ChoiceField(
        label=_("Sort By"),
        choices=[
            ('latest', _('Latest')),
            ('oldest', _('Oldest')),
            ('popular', _('Most Popular')),
            ('a-z', _('A-Z')),
            ('z-a', _('Z-A')),
        ],
        required=False,
        initial='latest',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with active categories."""
        super().__init__(*args, **kwargs)
        
        # Update category queryset to only include categories with posts
        self.fields['category'].queryset = Category.objects.filter(
            posts__status=Post.Status.PUBLISHED
        ).distinct() 