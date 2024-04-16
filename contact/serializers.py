from rest_framework import serializers
from .models import Owner, Barber, Review, Category, Service, GalleryItem, Appointment, Message


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    barber = serializers.StringRelatedField(read_only=True)
    service_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        
class BarberSerializer(serializers.ModelSerializer):
    appointments = serializers.StringRelatedField(many=True,read_only=True)
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    appointment_count = serializers.SerializerMethodField()
    avg_appointment = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        return obj.review_count()

    def get_avg_rate(self, obj):
        return obj.avg_rate()

    def get_appointment_count(self, obj):
        return obj.appointment_count()

    def get_avg_appointment(self, obj):
        return obj.avg_appointment()

    class Meta:
        model = Barber
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    barber = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    services = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'


class GalleryItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    service = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GalleryItem
        fields = '__all__'




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'