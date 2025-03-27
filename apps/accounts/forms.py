from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import UserProfile
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating a new user."""
    
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
        })
    )
    
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name'),
        })
    )
    
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last Name'),
        })
    )
    
    newsletter_subscription = forms.BooleanField(
        label=_("Subscribe to our newsletter"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Username'),
                'autofocus': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with custom styles and behaviors."""
        super().__init__(*args, **kwargs)
        
        # Apply form-control class to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password')
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Confirm Password')
        })
    
    def save(self, commit=True):
        """Save the user and their profile data."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Update newsletter subscription setting in profile
            newsletter_subscription = self.cleaned_data.get('newsletter_subscription', False)
            user.profile.newsletter_subscription = newsletter_subscription
            user.profile.save()
            
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form with styled widgets."""
    
    username = forms.CharField(
        label=_("Username or Email"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Username or Email'),
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Password'),
        }),
    )
    
    remember_me = forms.BooleanField(
        label=_("Remember me"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information."""
    
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('First Name'),
        })
    )
    
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Last Name'),
        })
    )
    
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email'),
            'readonly': 'readonly',
        })
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'location', 'birth_date', 
            'website', 'twitter', 'linkedin', 'github',
            'newsletter_subscription'
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png, image/jpeg, image/jpg'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Tell us about yourself')
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('City, Country')
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': _('https://example.com')
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': _('https://twitter.com/username')
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': _('https://linkedin.com/in/username')
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': _('https://github.com/username')
            }),
            'newsletter_subscription': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'avatar': _('Profil fotoğrafınız (Sadece PNG, JPG ve JPEG formatları kabul edilir)'),
            'bio': _('A brief description about yourself'),
            'birth_date': _('Your birth date (will not be displayed publicly)'),
            'newsletter_subscription': _('Receive occasional updates about new features and important news')
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with user fields."""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            
            if self.instance and hasattr(self.instance, 'bio'):
                for field_name in self.fields:
                    if field_name in ['first_name', 'last_name', 'email', 'avatar']:
                        continue
                    
                    if hasattr(self.instance, field_name) and getattr(self.instance, field_name):
                        self.fields[field_name].initial = getattr(self.instance, field_name)
    
    def clean_avatar(self):
        """Yüklenen avatar dosyasını doğrula."""
        avatar = self.cleaned_data.get('avatar')
        
        if avatar:
            # Dosya boyut kontrolü (5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_("Dosya boyutu 5MB'ı geçemez."))
            
            # Dosya uzantı kontrolü
            file_ext = avatar.name.split('.')[-1].lower()
            if file_ext not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError(_("Sadece PNG, JPG ve JPEG formatları kabul edilir."))
        
        return avatar
    
    def clean_birth_date(self):
        """Validate birth date to ensure it's not in the future."""
        birth_date = self.cleaned_data['birth_date']
        
        if birth_date and birth_date > date.today():
            raise forms.ValidationError(_("Birth date cannot be in the future."))
            
        return birth_date
    
    def clean_email(self):
        """E-posta adresi değiştirilemesin."""
        return self.initial.get('email')
    
    def save(self, user=None, commit=True):
        """Save profile and user data."""
        profile = super().save(commit=False)
        
        if user:
            # Update user fields
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            
            if commit:
                user.save()
                
                # Avatar için özel işlem
                avatar_file = self.cleaned_data.get('avatar')
                if avatar_file:
                    # Yeni bir avatar yüklendiyse, eski dosya silinmeden önce eski adı kaydet
                    old_avatar = None
                    if profile.avatar:
                        old_avatar = profile.avatar
                    
                    # Yeni avatarı ata
                    profile.avatar = avatar_file
                    
                    # Dosyayı sil
                    if old_avatar:
                        try:
                            storage, path = old_avatar.storage, old_avatar.path
                            storage.delete(path)
                        except Exception:
                            pass  # Dosya silinmezse devam et
                
                profile.save()
                
        elif commit:
            profile.save()
            
        return profile


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form with styled widgets."""
    
    old_password = forms.CharField(
        label=_("Current Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Current Password'),
            'autocomplete': 'current-password'
        }),
    )
    
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('New Password'),
            'autocomplete': 'new-password'
        }),
    )
    
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm New Password'),
            'autocomplete': 'new-password'
        }),
    ) 