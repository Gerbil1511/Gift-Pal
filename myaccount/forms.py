from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import MyAccount

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',  # Add Bootstrap class
                'accept': 'image/*',  # Restrict to image files
            }),
        }
        labels = {
            'profile_image': 'Upload a new profile photo',  # Custom label
        }
        help_texts = {
            'profile_image': 'Allowed formats: JPG, PNG, GIF. Max size: 5MB.',  # Help text
        }

class ProfileStatusForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['status_message']
        widgets = {
            'status_message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'How are you feeling today?'
            })
        }

class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = MyAccount
        fields = ['about_me', 'birthday', 'favorite_links']
        widgets = {
            'birthday': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'about_me': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself...'
            }),
            'favorite_links': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add links, one per line...'
            })
        }