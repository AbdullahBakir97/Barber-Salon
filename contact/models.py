from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
#from phonenumber_field.modelfields import PhoneNumberField



class Owner(models.Model):
    name = models.CharField(_('Name'),max_length=255)
    email = models.EmailField(_('Email'),)
    phone = models.CharField(_('Telefon'),max_length=15)
    address = models.TextField(_('Adresse'),)
    logo = models.ImageField(_('Logo'),upload_to='owner_logos/')
    website = models.URLField(_('Webseite'),blank=True, null=True)
    work_days = models.CharField(_('Arbeits Tage'),max_length=255, default='Montag-Freitag')
    about = models.TextField(_('Über'),blank=True, null=True)
    social_media_links = models.JSONField(_('Social Links'),blank=True, null=True)
    
    def __str__(self):
        return self.name

class Barber(models.Model):
    name = models.CharField(_('Name'),max_length=255)
    appointment = models.ForeignKey('Appointment',related_name='barber_appointment', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Termine'))
    expertise = models.CharField(_('Erfahrung'),max_length=255)
    experience_years = models.IntegerField(_('Erfahrung Jahre'),)
    image = models.ImageField(_('Foto'),upload_to='barber_images/')

    def __str__(self):
        return self.name

class Review(models.Model):
    visitor_hash = models.CharField(max_length=64, null=True, blank=True)
    image = models.ImageField(_('Foto'),upload_to='review_images/', null=True, blank=True)
    barber = models.ForeignKey(Barber,related_name='barber_review', on_delete=models.SET_NULL, null=True, verbose_name=_('Friseur'))
    customer_name = models.CharField(_('Name'),max_length=255)
    comment = models.TextField(_('Kommentare'),)
    rating = models.IntegerField(_('Bewertung'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
        
        super().save(*args, **kwargs)


    def __str__(self):
        if self.barber:
            return f"{self.customer_name} - {self.barber.name}"
        else:
            return f"{self.customer_name} - No associated barber"



class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255, default='Default Category Name')
    
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(_('Name'), max_length=255, default='Default Service Name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='service_category')
    price = models.DecimalField(_('Preis'),max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    name = models.CharField(_('Element'),max_length=255, default='Galerie Element')
    image = models.ImageField(_('Foto'),upload_to='gallery_images/')
    description = models.TextField(_('Beschriebeung'),)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='gallery_category')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='gallery_service')

    def __str__(self):
        return self.name

class Appointment(models.Model):
    visitor_hash = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(_('Name'),max_length=255)
    barber = models.ForeignKey(Barber,related_name='barber_reserved', on_delete=models.SET_NULL, null=True, verbose_name=_('Friseur'))
    date = models.DateField(_('Datum'),)
    time = models.TimeField(_('Zeit'),)
    service_type = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointment_service')
    phone = models.CharField(_('Telefon'),max_length=15)
    email = models.EmailField(_('Email'),default='no-reply@example.com')
    message = models.TextField(_('Nachricht'),)

    def __str__(self):
        if self.barber:
            return f"{self.name} - {self.barber.name}"
        else:
            return f"{self.name} - No associated barber"
    

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"