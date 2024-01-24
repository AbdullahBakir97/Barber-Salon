from django import forms
from .models import Review, Appointment, Barber, GalleryItem
from django.utils.translation import gettext_lazy as _

class BarberForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = ['name', 'expertise', 'experience_years', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

        labels = {
            'name': _('Name'),
            'expertise': _('Fachkenntnisse'),
            'experience_years': _('Berufserfahrung in Jahren'),
            'image': _('Bild'),
        }

    def __init__(self, *args, **kwargs):
        super(BarberForm, self).__init__(*args, **kwargs)


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['image', 'description', 'category', 'service']

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'image': _('Bild'),
            'description': _('Beschreibung'),
            'category': _('Kategorie'),
            'service': _('Dienstleistung'),
        }

    def __init__(self, *args, **kwargs):
        super(GalleryItemForm, self).__init__(*args, **kwargs)


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['barber', 'customer_name', 'comment', 'rating']

        widgets = {
            'barber': forms.HiddenInput(),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'barber': _('Friseur'),
            'customer_name': _('Kundenname'),
            'comment': _('Kommentar'),
            'rating': _('Bewertung'),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewCreateForm, self).__init__(*args, **kwargs)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'barber', 'email', 'date', 'time', 'service_type', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
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

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)



