from django import forms
from .models import Review, Appointment, Barber, GalleryItem

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

    def __init__(self, *args, **kwargs):
        super(BarberForm, self).__init__(*args, **kwargs)


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['image', 'description']

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(GalleryItemForm, self).__init__(*args, **kwargs)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'barber', 'date', 'time', 'service_type', 'phone', 'message']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)


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

    def __init__(self, *args, **kwargs):
        super(ReviewCreateForm, self).__init__(*args, **kwargs)
