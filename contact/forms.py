from django import forms
from .models import Owner, Review, Appointment, Barber, GalleryItem
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'email', 'phone', 'address', 'logo', 'website', 'about', 'social_media_links']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'social_media_links': forms.JSONField(),
        }

        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone': _('Telefon'),
            'address': _('Adresse'),
            'logo': _('Logo'),
            'website': _('Webseite'),
            'about': _('Über'),
            'social_media_links': _('Social Links'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Owner.objects.filter(email=email).exists():
            raise ValidationError(_('Ein Eigentümer mit dieser E-Mail existiert bereits.'))
        return email


class BarberForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = ['name', 'expertise', 'experience_years', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        labels = {
            'name': _('Name'),
            'expertise': _('Fachkenntnisse'),
            'experience_years': _('Berufserfahrung in Jahren'),
            'image': _('Bild'),
        }

    def __init__(self, *args, **kwargs):
        super(BarberForm, self).__init__(*args, **kwargs)

    def clean_experience_years(self):
        experience_years = self.cleaned_data['experience_years']
        if experience_years < 0:
            raise ValidationError(_('Die Berufserfahrung darf nicht negativ sein.'))
        return experience_years
    
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            # Check if the file is an image
            try:
                Image.open(image)
            except Exception as e:
                raise ValidationError(_('Invalid image file. Please upload a valid image.'))

            # Check the file size
            if image.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError(_('File size must be no more than 5 MB.'))

        return image
    

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['name', 'image', 'description', 'category', 'service']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': _('Name'),
            'image': _('Bild'),
            'description': _('Beschreibung'),
            'category': _('Kategorie'),
            'service': _('Dienstleistung'),
        }

    def __init__(self, *args, **kwargs):
        super(GalleryItemForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        service = cleaned_data.get('service')

        if category == 'A' and not service:
            raise ValidationError(_('Bitte wählen Sie eine Dienstleistung für die Kategorie A aus.'))
        return cleaned_data


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['image', 'barber', 'customer_name', 'comment', 'rating']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '1', 'max': '5'}),
        }

        labels = {
            'image': _('Foto'),
            'barber': _('Friseur'),
            'customer_name': _('Kundenname'),
            'comment': _('Kommentar'),
            'rating': _('Bewertung'),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewCreateForm, self).__init__(*args, **kwargs)
        
    
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            # Check if the file is an image
            try:
                Image.open(image)
            except Exception as e:
                raise ValidationError(_('Invalid image file. Please upload a valid image.'))

            # Check the file size
            if image.size > 5 * 1024 * 1024:  # 5 MB
                raise ValidationError(_('File size must be no more than 5 MB.'))

        return image

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise ValidationError(_('Die Bewertung muss zwischen 1 und 5 liegen.'))
        return rating


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'barber', 'email', 'date', 'time', 'service_type', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': _('Ihr Name'),
            'barber': _('Friseur auswählen'),
            'email': _('Ihre E-Mail'),
            'date': _('Bevorzugtes Datum'),
            'time': _('Bevorzugte Uhrzeit'),
            'service_type': _('Dienstleistungsart'),
            'phone': _('Ihre Telefonnummer'),
            'message': _('Zusätzliche Nachricht'),
        }
        
        error_messages = {
            'name': {
                'required': _('Bitte geben Sie Ihren Namen ein.'),
            },
            'barber': {
                'required': _('Bitte wählen Sie einen Friseur aus.'),
            },
            'email': {
                'required': _('Bitte geben Sie Ihre E-Mail-Adresse ein.'),
                'invalid': _('Bitte geben Sie eine gültige E-Mail-Adresse ein.'),
            },
            'date': {
                'invalid': _('Bitte geben Sie ein gültiges Datum ein.'),
            },
            'time': {
                'invalid': _('Bitte geben Sie eine gültige Uhrzeit ein.'),
            },
            'service_type': {
                'required': _('Bitte wählen Sie eine Dienstleistungsart aus.'),
            },
            'phone': {
                'required': _('Bitte geben Sie Ihre Telefonnummer ein.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError(_('Das Datum darf nicht in der Vergangenheit liegen.'))
        return date


