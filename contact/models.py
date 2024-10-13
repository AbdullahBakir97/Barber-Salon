from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _ 
from django.conf import settings
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from phonenumber_field.modelfields import PhoneNumberField
import PIL.Image



class Owner(models.Model):
    name = models.CharField(_('Name'),max_length=255)
    email = models.EmailField(_('Email'),)
    phone = PhoneNumberField(_('Telefon'),max_length=15)
    address = models.TextField(_('Adresse'),)
    logo = models.ImageField(_('Logo'),blank=True, null=True, upload_to='owner_logos/')
    website = models.URLField(_('Webseite'),blank=True, null=True)
    work_days = models.CharField(_('Arbeits Tage'),max_length=255, default='Montag-Freitag')
    opening_time = models.TimeField(_('Öffnungszeit'), default=datetime.time(9, 0))
    closing_time = models.TimeField(_('Schließungszeit'), default=datetime.time(20, 0))
    about = models.TextField(_('Über'),blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(_('Slug'), unique=True,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Barber(models.Model):
    name = models.CharField(_('Name'),max_length=255)
    appointment = models.ForeignKey('Appointment',related_name='appointments', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Termine'))
    expertise = models.CharField(_('Erfahrung'),max_length=255)
    experience_years = models.IntegerField(_('Erfahrung Jahre'),)
    image = models.ImageField(_('Foto'),upload_to='barber_images/')
    slug = models.SlugField(_('Slug'), unique=True,blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def review_count(self):
        return self.barber_review.count()

    def avg_rate(self):
        avg = self.barber_review.aggregate(rate_avg=Avg('rating'))
        return round(avg['rate_avg'], 2) if avg['rate_avg'] else 0

    def appointment_count(self):
        return self.barber_appointment.count()
    

    def avg_appointment(self):
        avg = Barber.objects.annotate(avg_count=Count('barber_appointment')).aggregate(avg_appointment=Avg('avg_count'))
        return round(avg['avg_appointment'], 2) if avg['avg_appointment'] else 0

class Review(models.Model):
    image = models.ImageField(_('Foto'),upload_to='review_images/', null=True, blank=True)
    barber = models.ForeignKey(Barber,related_name='barber_review', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Friseur'))
    customer_name = models.CharField(_('Name'),max_length=255)
    email = models.EmailField(_('Email'))
    comment = models.TextField(_('Kommentare'),)
    rating = models.IntegerField(_('Bewertung'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.customer_name}-{self.barber.name}")
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
        
        super().save(*args, **kwargs)


    def __str__(self):
        if self.barber:
            return f"{self.customer_name} - {self.barber.name}"
        return f"{self.customer_name} - No associated barber"
        
    def barber_review_count(self):
        return Review.objects.filter(barber=self.barber).count()



class Category(models.Model):
    name = models.CharField(_('Name'), max_length=255, default='Default Category Name')
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(_('Name'), max_length=255, default='Default Service Name')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_category')
    price = models.DecimalField(_('Preis'),max_digits=10, decimal_places=2)
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    name = models.CharField(_('Element'),max_length=255, default='Galerie Element')
    image = models.ImageField(_('Foto'),upload_to='gallery_images/')
    description = models.TextField(_('Beschriebeung'),)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_category')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_service')
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    


class Appointment(models.Model):
    name = models.CharField(_('Name'),max_length=30)
    barber = models.ForeignKey(Barber,related_name='barber_appointment', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Friseur'))
    date = models.DateField(_('Datum'),)
    time = models.TimeField(_('Zeit'),)
    service_type = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment_service')
    phone = models.CharField(_('Telefon'),max_length=15)
    email = models.EmailField(_('Email'),default='no-reply@example.com')
    message = models.TextField(_('Nachricht'),max_length=200, null=True, blank=True)
    slug = models.SlugField(_('Slug'), blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.barber.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.barber:
            return f"{self.name} - {self.barber.name}"
        return f"{self.name} - No associated barber"
        
    @classmethod
    def total_count(cls):
        return cls.objects.count()

    @classmethod
    def count_with_no_barber(cls):
        return cls.objects.filter(barber__isnull=True).count()
    

class Message(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(_('Slug'),blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.timestamp}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"