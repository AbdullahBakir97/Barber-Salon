from django.db import models
from django_filters import rest_framework as filters
from .models import Owner, Barber, Review, GalleryItem, Appointment, Message, Service, Category


class OwnerFilter(filters.FilterSet):
    class Meta:
        model = Owner
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'phone': ['icontains'],
        }


class BarberFilter(filters.FilterSet):
    review_count = filters.NumberFilter(field_name='barber_review__count', method='filter_by_review_count')

    class Meta:
        model = Barber
        fields = {
            'name': ['icontains'],
            'expertise': ['icontains'],
            'experience_years': ['exact', 'gte', 'lte'],
        }

    def filter_by_review_count(self, queryset, name, value):
        return queryset.annotate(review_count=models.Count('barber_review')).filter(review_count__gte=value)


class ReviewFilter(filters.FilterSet):
    barber_name = filters.CharFilter(field_name='barber__name', lookup_expr='icontains')


    class Meta:
        model = Review
        fields = {
            'customer_name': ['icontains'],
            'rating': ['exact', 'gte', 'lte'],
        }


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
            'service_category__name': ['icontains'],
        }


class ServiceFilter(filters.FilterSet):
    class Meta:
        model = Service
        fields = {
            'name': ['icontains'],
            'category__name': ['icontains'],
            'price': ['exact', 'gte', 'lte'],
        }


class GalleryItemFilter(filters.FilterSet):
    class Meta:
        model = GalleryItem
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'category__name': ['icontains'],
            'service__name': ['icontains'],
        }


class AppointmentFilter(filters.FilterSet):
    service_type__name = filters.CharFilter(field_name='service_type__name', lookup_expr='icontains')

    class Meta:
        model = Appointment
        fields = {
            'name': ['icontains'],
            'barber__name': ['icontains'],
            'date': ['exact'],
            'time': ['exact'],
            'service_type__name': ['icontains'],
            'phone': ['icontains'],
            'email': ['icontains'],
            'message': ['icontains'],
        }


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'phone': ['icontains'],
            'message': ['icontains'],
            'timestamp': ['exact', 'gte', 'lte'],
        }
