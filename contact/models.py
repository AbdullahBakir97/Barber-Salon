from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
#from accounts.models import OwnerProfile 
from django.conf import settings
#from phonenumber_field.modelfields import PhoneNumberField



class Owner(models.Model):
    #user = models.OneToOneField('accounts.OwnerProfile', related_name='owner_user', on_delete=models.CASCADE, verbose_name=_('Eigentümer'))
    name = models.CharField(_('Name'),max_length=255)
    email = models.EmailField(_('Email'),)
    phone = models.CharField(_('Telefon'),max_length=15)
    address = models.TextField(_('Adresse'),)
    logo = models.ImageField(_('Logo'),upload_to='owner_logos/')
    website = models.URLField(_('Webseite'),blank=True, null=True)
    about = models.TextField(_('Über'),blank=True, null=True)
    social_media_links = models.JSONField(_('Social Links'),blank=True, null=True)

class Barber(models.Model):
    name = models.CharField(_('Name'),max_length=255)
    expertise = models.CharField(_('Erfahrung'),max_length=255)
    experience_years = models.IntegerField(_('Erfahrung Jahre'),)
    image = models.ImageField(_('Foto'),upload_to='barber_images/')

class Review(models.Model):
    barber = models.ForeignKey(Barber,related_name='barber_review', on_delete=models.SET_NULL, null=True, verbose_name=_('Friseur'))
    customer_name = models.CharField(_('Name'),max_length=255)
    comment = models.TextField(_('Kommentare'),)
    rating = models.IntegerField(_('Bewertung'),)


SERVICE_TYPES = (
        ('HairCut','Haarschnitt'),
        ('Beard','Bart'),
        ('Hair coloring','haare Färben'),
        ('Massage','Massage'),
        ('Maskes','Masken'),
        ('Stayling Products','Styling Produkte'),
        ('Skin Cleaning','Gesicht Reinigung'),
        
        )
CATEGORY_TYPES = (
    ('Stayling','Styling'),
    ('Massage','Massage'),
    ('Skin Care','Hautpflege'),
)
class GalleryItem(models.Model):
    name = models.CharField(_('Element'),max_length=255, default='Galerie Element')
    image = models.ImageField(_('Foto'),upload_to='gallery_images/')
    description = models.TextField(_('Beschriebeung'),)
    category = models.CharField(_('Kategorie'),max_length=20,choices=CATEGORY_TYPES,default=CATEGORY_TYPES[0][0])
    service = models.CharField(_('Service'),max_length=20,choices=SERVICE_TYPES,default=SERVICE_TYPES[0][0])

class Appointment(models.Model):
    name = models.CharField(_('Name'),max_length=255)
    barber = models.ForeignKey(Barber,related_name='barber_appointment', on_delete=models.SET_NULL, null=True, verbose_name=_('Friseur'))
    date = models.DateField(_('Datum'),)
    time = models.TimeField(_('Zeit'),)
    service_type = models.CharField(_('Service'),max_length=20, choices=SERVICE_TYPES,default=SERVICE_TYPES[0][0])
    phone = models.CharField(_('Telefon'),max_length=15)
    email = models.EmailField(_('Email'),default='no-reply@example.com')
    message = models.TextField(_('Nachricht'),)



