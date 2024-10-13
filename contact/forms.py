from django import forms
from .models import Owner, Review, Appointment, Barber, GalleryItem, Service, Category , Message
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image

class OwnerForm(forms.ModelForm):
    work_days = forms.CharField(label=_('Arbeits Tage'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    opening_time = forms.TimeField(label=_('Öffnungszeit'), widget=forms.TimeInput(attrs={'class': 'form-control', 'autofocus': True}))
    closing_time = forms.TimeField(label=_('Schließungszeit'), widget=forms.TimeInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Owner
        fields = ['name', 'email', 'phone', 'address', 'logo', 'website', 'about','work_days', 'opening_time', 'closing_time', 'tax_id']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'work_days': forms.TextInput(attrs={'class': 'form-control'}),
            'opening_time': forms.TimeInput(attrs={'class': 'form-control', 'autofocus': True}),
            'closing_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone': _('Telefon'),
            'address': _('Adresse'),
            'logo': _('Logo'),
            'website': _('Webseite'),
            'about': _('Über'),
            'work_days': _('Arbeits Tage'),
            'opening_time': _('Öffnungszeit'),
            'closing_time': _('Schließungszeit'),
            'tax_id': _('Steuernummer'),
        }
        
        error_messages = {
            'name': {
                'required': _("Der Name ist erforderlich."),
            },
            'email': {
                'required': _("Die E-Mail ist erforderlich."),
                'unique': _("Ein Eigentümer mit dieser E-Mail existiert bereits."),
            },
            'phone': {
                'required': _("Die Telefonnummer ist erforderlich."),
            },
            'address': {
                'required': _("Die Adresse ist erforderlich."),
            },
            'logo': {
                'required': _("Das Logo ist erforderlich."),
            },
            'website': {
                'required': _("Die Webseite ist erforderlich."),
            },
            'about': {
                'required': _("Informationen über den Eigentümer sind erforderlich."),
            },
            'work_days': {
                'required': _("Die Arbeits Tage sind erforderlich."),
            },
            'opening_time': {
                'required': _("Die Öffnungszeit ist erforderlich."),
            },
            'closing_time': {
                'required': _("Die Schließungszeit ist erforderlich."),
            },
            'tax_id': {
                'required': _("Die Steuernummer ist erforderlich."),
            },
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Owner.objects.filter(email=email).exists():
            raise ValidationError(_('Ein Besitzer mit dieser E-Mail existiert bereits.'))
        return email

    def clean(self):
        cleaned_data = super().clean()
        opening_time = cleaned_data.get('opening_time')
        closing_time = cleaned_data.get('closing_time')

        if opening_time and closing_time:
            if opening_time >= closing_time:
                raise forms.ValidationError(_('Die Schließzeit muss nach der Öffnungszeit liegen.'))

        return cleaned_data

class MessageForm(forms.ModelForm):
    name = forms.CharField(label='Your Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Your Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Your Phone', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Message  
        fields = ['name', 'email', 'phone', 'message']


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
    
    # def clean_image(self):
    #     image = self.cleaned_data.get('image', False)
    #     if image:
    #         # Check if the file is an image
    #         try:
    #             Image.open(image)
    #         except Exception as e:
    #             raise ValidationError(_('Invalid image file. Please upload a valid image.'))

    #         # Check the file size
    #         if image.size > 5 * 1024 * 1024:  # 5 MB
    #             raise ValidationError(_('File size must be no more than 5 MB.'))

    #     return image
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': _('Name'),
        }

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
        return cleaned_data





class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['image', 'barber', 'customer_name', 'email', 'comment', 'rating']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'barber': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.HiddenInput(),
        
            
        }

        labels = {
            'image': _('Foto'),
            'barber': _('Friseur'),
            'customer_name': _('Kundenname'),
            'email': _('Email'),
            'comment': _('Kommentar'),
            'rating': _('Bewertung'),
            
        }
        
        error_messages = {
        'customer_name': {
            'required': _('Bitte geben Sie Ihren Namen ein.'),
        },
        'barber': {
            'required': _('Bitte wählen Sie einen Friseur aus.'),
        },
        'email': {
            'required': _('Bitte geben Sie Ihre E-Mail-Adresse ein.'),
            'invalid': _('Bitte geben Sie eine gültige E-Mail-Adresse ein.'),
        },
        'comment':{
            'required': _('Bitte geben Sie einen Kommentar ein.'),
        },
        'rating': {
            'required': _('Bitte geben Sie eine Bewertung ein.'),
        },
    }
        
    def __init__(self, *args, **kwargs):
        super(ReviewCreateForm, self).__init__(*args, **kwargs)
        self.fields['barber'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')
        email = cleaned_data.get('email')
        barber = cleaned_data.get('barber')

        # Check if there is already a review with the same name, email, and barber
        if Review.objects.filter(customer_name=customer_name, email=email, barber=barber).exists():
            raise ValidationError(_('Es existiert bereits eine Bewertung mit demselben Namen, derselben E-Mail und demselben Friseur.'))

        return cleaned_data
    
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
        rating = self.cleaned_data.get('rating')
        if not 1 <= rating <= 5:
            raise ValidationError(_('Die Bewertung muss zwischen 1 und 5 liegen.'))
        return rating


class AppointmentForm(forms.ModelForm):
    default_message = _('Bitte geben Sie alle zusätzlichen Informationen oder besondere Wünsche an.')

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
                'required': _('Bitte geben Sie Datum ein.'),
            },
            'time': {
                'required': _('Bitte geben Sie Uhrzeit ein.'),
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
        self.fields['message'].initial = self.default_message

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message == self.default_message:
            return '' 
        return message
        
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        barber = cleaned_data.get('barber')
        email = cleaned_data.get('email')

        # Check if an appointment with the same name, date, time, and barber already exists
        if Appointment.objects.filter(name=name, date=date, time=time, barber=barber, email=email).exists():
            raise forms.ValidationError("Es gibt bereits einen Termin für Sie zu diesem Datum und dieser Uhrzeit mit dem ausgewählten Friseur.")

        # Check if there is already an appointment with the same date and time
        if Appointment.objects.filter(date=date, time=time, barber=barber).exists():
            raise forms.ValidationError("Doppelter Termin gefunden. Bitte wählen Sie eine andere Uhrzeit oder einen anderen Friseur.")

        return cleaned_data

    def clean_date(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data.get('date')       
        if date is None:
            return date       
        if date < timezone.now().date():
            raise ValidationError(_('Das Datum darf nicht in der Vergangenheit liegen.'))        
        if date > timezone.now().date() + timezone.timedelta(days=365):
             raise ValidationError(_('Das Datum darf nicht mehr als ein Jahr in der Zukunft liegen.'))         
        return date
    
    def clean_time(self):
        cleaned_data = self.cleaned_data
        time = cleaned_data.get('time')
        date = cleaned_data.get('date')       
        if time is None or date is None:
            return time
        current_datetime = timezone.now()
        if date == current_datetime.date() and time < current_datetime.time():
            raise ValidationError(_('Die Uhrzeit kann nicht in der Vergangenheit liegen.'))         
        owner = Owner.objects.first()  # Get the owner instance
        if owner:
            work_days = owner.work_days
            opening_time = owner.opening_time
            closing_time = owner.closing_time
            # Get the day of the week (0 = Monday, 6 = Sunday)
            day_of_week = date.weekday()
            # Check if it's Sunday (day_of_week == 6)
            if day_of_week == 6:
                raise ValidationError(_('Am Sonntag sind wir geschlossen.'))
            # Check if the time is between opening and closing time
            if time < opening_time or time > closing_time:
                raise ValidationError(_('Wir sind von {} von {} bis {} Uhr geöffnet.'.format(work_days, opening_time.strftime('%H:%M'), closing_time.strftime('%H:%M'))))
        return time
    
class ServiceForm(forms.ModelForm):


    class Meta:
        model = Service
        fields = ['name', 'price', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Name'),
            'price': _('Price'),
            'category': _('Category'),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')

        if not category:
            raise forms.ValidationError(_('Please select a category.'))

        return cleaned_data
