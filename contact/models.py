from django.db import models
from django.shortcuts import get_object_or_404


class Owner(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    logo = models.ImageField(upload_to='owner_logos/')
    website = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)

class Barber(models.Model):
    name = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    image = models.ImageField(upload_to='barber_images/')

class Review(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField()

class GalleryItem(models.Model):
    image = models.ImageField(upload_to='gallery_images/')
    description = models.TextField()

class Appointment(models.Model):
    name = models.CharField(max_length=255)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    service_type = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    message = models.TextField()



