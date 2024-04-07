from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, OwnerProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'barber', 'phone', 'date_of_birth', 'gender', 'address']
        labels = {
            'profile_image': _('Profile Foto'),
            'barber': _('Friseur'),
            'phone': _('Telefon'),
            'date_of_birth': _('Geburtsdatum'),
            'gender': _('Geschlecht'),
            'address': _('Adresse'),
        }
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['image', 'phone', 'date_of_birth', 'gender', 'address']
        labels = {
            'image': _('Foto'),
            'phone': _('Telefon'),
            'date_of_birth': _('Geburtsdatum'),
            'gender': _('Geschlecht'),
            'address': _('Adresse'),
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields
