from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , AuthenticationForm 
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile, OwnerProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        labels = {
            'profile_image': _('Profile Foto'),
        }

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ['image']
        labels = {
            'image': _('Foto'),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'email', 'phone', 'date_of_birth', 'gender', 'address',
            'password1', 'password2',  # Include password fields
            'is_staff', 'is_active',  # Include staff and active status
        )
        labels = {
            'email': _('Email'),
            'phone': _('Telefon'),
            'date_of_birth': _('Geburtsdatum'),
            'gender': _('Geschlecht'),
            'address': _('Adresse'),
            'password1': _('Passwort'),
            'password2': _('Passwort bestätigen'),
            'is_staff': _('Staff status'),
            'is_active': _('Active status'),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser