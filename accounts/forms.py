from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile, OwnerProfile

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
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'name', 'email', 'phone', 'date_of_birth', 'gender', 'address',
            'password1', 'password2',  
             'is_active',  
        )
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone': _('Telefon'),
            'date_of_birth': _('Geburtsdatum'),
            'gender': _('Geschlecht'),
            'address': _('Adresse'),
            'password1': _('Passwort'),
            'password2': _('Passwort bestätigen'),
            'is_active': _('Active status'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
