from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, OwnerProfile
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'barber']
        labels = {
            'profile_image': _('Profile Foto'),
            'barber': _('Friseur'),
        }
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
        }

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['image']
        labels = {
            'image': _('Foto'),
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields

