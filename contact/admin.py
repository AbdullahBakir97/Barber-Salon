from django.contrib import admin
from .models import Owner, Barber, Review, GalleryItem, Appointment



@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'website')
    search_fields = ('name', 'email', 'phone', 'website')

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('name', 'expertise', 'experience_years')
    search_fields = ('name', 'expertise')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('barber', 'customer_name', 'rating')
    search_fields = ('barber__name', 'customer_name', 'rating')

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'barber', 'date', 'time', 'service_type', 'phone')
    search_fields = ('name', 'barber__name', 'service_type', 'phone')

