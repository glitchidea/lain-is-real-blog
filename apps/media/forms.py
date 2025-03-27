from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MediaFile, Gallery, GalleryItem
from django.core.validators import FileExtensionValidator


class MediaFileForm(forms.ModelForm):
    """Form for creating and managing media files."""
    
    class Meta:
        model = MediaFile
        fields = ['title', 'description', 'file', 'upload_type', 'alt_text', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('File Title')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('File description (optional)')
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'upload_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Alternative text for accessibility')
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'alt_text': _('Describe the image for users who cannot see it (for accessibility)'),
            'is_public': _('If checked, other users will be able to see and use this file'),
            'upload_type': _('Select the type of file you are uploading'),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make certain fields not required
        self.fields['description'].required = False
        self.fields['alt_text'].required = False
        
        # Set accept attribute based on upload_type
        self.fields['file'].widget.attrs['accept'] = self.get_accept_attribute()
    
    def get_accept_attribute(self):
        """Get the accept attribute for the file input based on upload type."""
        initial_type = self.initial.get('upload_type', None) if hasattr(self, 'initial') else None
        if initial_type == MediaFile.UploadType.IMAGE:
            return '.jpg,.jpeg,.png,.gif,.svg'
        elif initial_type == MediaFile.UploadType.DOCUMENT:
            return '.pdf,.doc,.docx,.txt,.rtf'
        elif initial_type == MediaFile.UploadType.VIDEO:
            return '.mp4,.webm,.mov,.avi'
        elif initial_type == MediaFile.UploadType.AUDIO:
            return '.mp3,.wav,.ogg'
        else:
            # Default to all supported types
            return '.jpg,.jpeg,.png,.gif,.svg,.pdf,.doc,.docx,.txt,.rtf,.mp4,.webm,.mov,.avi,.mp3,.wav,.ogg'
    
    def clean_file(self):
        """Validate the file."""
        file = self.cleaned_data.get('file')
        if not file:
            return file
            
        if hasattr(file, 'size'):
            # Check file size (10MB limit)
            max_size = 10 * 1024 * 1024  # 10MB
            if file.size > max_size:
                raise forms.ValidationError(_("The file is too large. Maximum size is 10MB."))
                
        # Check file extension based on upload_type
        upload_type = self.cleaned_data.get('upload_type')
        if upload_type == MediaFile.UploadType.IMAGE:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'svg']
        elif upload_type == MediaFile.UploadType.DOCUMENT:
            allowed_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf']
        elif upload_type == MediaFile.UploadType.VIDEO:
            allowed_extensions = ['mp4', 'webm', 'mov', 'avi']
        elif upload_type == MediaFile.UploadType.AUDIO:
            allowed_extensions = ['mp3', 'wav', 'ogg']
        else:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'svg', 'pdf', 'doc', 'docx', 
                                'txt', 'rtf', 'mp4', 'webm', 'mov', 'avi', 'mp3', 'wav', 'ogg']
                                
        # Get the file extension
        filename = file.name
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        
        if extension not in allowed_extensions:
            raise forms.ValidationError(
                _("Invalid file extension. Allowed extensions are: %(extensions)s"),
                params={'extensions': ', '.join(allowed_extensions)}
            )
            
        return file
    
    def save(self, commit=True):
        """Save the media file with the current user as uploader."""
        media_file = super().save(commit=False)
        
        if self.user and not media_file.uploaded_by_id:
            media_file.uploaded_by = self.user
            
        if commit:
            media_file.save()
            
        return media_file


class BulkUploadForm(forms.Form):
    """Form for bulk uploading multiple files at once."""
    
    # Note: In real applications, handle multiple file uploads via JavaScript
    # For simplicity, we're using a single file upload here
    file = forms.FileField(
        label=_("File"),
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.jpg,.jpeg,.png,.gif,.pdf,.doc,.docx,.mp4,.mp3'
        })
    )
    
    upload_type = forms.ChoiceField(
        label=_("Upload Type"),
        choices=MediaFile.UploadType.choices,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    is_public = forms.BooleanField(
        label=_("Public"),
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class GalleryForm(forms.ModelForm):
    """Form for creating and editing galleries."""
    
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Gallery Title')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Gallery description (optional)')
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make description not required
        self.fields['description'].required = False
    
    def save(self, commit=True):
        """Save the gallery with the current user as creator."""
        gallery = super().save(commit=False)
        
        if self.user and not gallery.created_by_id:
            gallery.created_by = self.user
            
        if commit:
            gallery.save()
            
        return gallery


class GalleryItemForm(forms.ModelForm):
    """Form for adding items to a gallery."""
    
    class Meta:
        model = GalleryItem
        fields = ['media_file', 'caption', 'order']
        widgets = {
            'media_file': forms.Select(attrs={
                'class': 'form-control'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Caption (optional)')
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom behaviors."""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter media files by user and type (images only)
        if user:
            self.fields['media_file'].queryset = MediaFile.objects.filter(
                uploaded_by=user, 
                upload_type=MediaFile.UploadType.IMAGE
            )
        
        # Make caption not required
        self.fields['caption'].required = False


class GalleryItemBulkForm(forms.Form):
    """Form for adding multiple items to a gallery at once."""
    
    media_files = forms.ModelMultipleChoiceField(
        queryset=MediaFile.objects.none(),
        label=_("Select Images"),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with user's images."""
        gallery = kwargs.pop('gallery', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Get existing media file IDs in the gallery
            existing_ids = []
            if gallery:
                existing_ids = gallery.items.values_list('media_file_id', flat=True)
            
            # Filter media files by user, type (images only), and exclude existing items
            self.fields['media_files'].queryset = MediaFile.objects.filter(
                uploaded_by=user, 
                upload_type=MediaFile.UploadType.IMAGE
            ).exclude(id__in=existing_ids) 