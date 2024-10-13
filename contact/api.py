from rest_framework import generics, filters, status
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from django.template.loader import render_to_string 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import (
    Owner, Barber, Review, GalleryItem, Appointment, Message, Service, Category
)
from .serializers import (
    OwnerSerializer, BarberSerializer, ReviewSerializer, GalleryItemSerializer,
    AppointmentSerializer, MessageSerializer, ServiceSerializer, CategorySerializer
)
from .mypagination import MyPagination
from .myfilter import (
    OwnerFilter, BarberFilter, ReviewFilter, CategoryFilter,
    ServiceFilter, GalleryItemFilter, AppointmentFilter, MessageFilter
)
from django.http import Http404


class ContactAPIView(APIView):
    def get(self, request):
        owner = Owner.objects.first()
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = []

    def get_queryset(self):
        return self.queryset

class ModelCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset
    
class ModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset

class BarberListAPIView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().prefetch_related('barber_appointment')
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer
    filterset_fields = ['name', 'expertise', 'experience_years']
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'expertise', 'experience_years']
    filterset_class = BarberFilter
    

class BarberCreateAPIView(ModelCreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class BarberRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class ReviewListAPIView(ModelListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filterset_fields = ['barber', 'customer_name', 'rating']
    search_fields = ['barber__name', 'customer_name', 'rating']
    filterset_class = ReviewFilter
    pagination_class = MyPagination

class ReviewCreateAPIView(ModelCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class GalleryItemListAPIView(ModelListAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    filterset_fields = ['name', 'category', 'service']
    search_fields = ['name', 'category__name', 'service__name']
    filterset_class = GalleryItemFilter
    pagination_class = MyPagination
    
     

class GalleryItemCreateAPIView(ModelCreateAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

class GalleryItemRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

class AppointmentListAPIView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    search_fields = ['barber__name', 'date', 'service_type__name']
    filterset_class = AppointmentFilter
    pagination_class = MyPagination

class AppointmentCreateAPIView(ModelCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        service_type_id = self.request.data.get('service_type')
        if service_type_id is None:
            return Response({"service_type": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service_type = Service.objects.get(pk=service_type_id)
        except Service.DoesNotExist:
            return Response({"service_type": ["Invalid service type ID."]}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(service_type=service_type)

class AppointmentRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class MessageListAPIView(ModelListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_fields = ['name', 'email', 'phone', 'message']
    search_fields = ['name', 'email', 'phone', 'message']
    filterset_class = MessageFilter
    pagination_class = MyPagination

class MessageCreateAPIView(ModelCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ServiceListAPIView(ModelListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = ['name', 'category__name', 'price']
    search_fields = ['name', 'category__name', 'price']
    filterset_class = ServiceFilter
    pagination_class = MyPagination

class ServiceCreateAPIView(ModelCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class CategoryListAPIView(ModelListAPIView):
    queryset = Category.objects.prefetch_related('service_category').all()
    serializer_class = CategorySerializer
    filterset_fields = ['name','service_category__name']
    search_fields = ['name','service_category__name']   
    filterset_class = CategoryFilter
    pagination_class = MyPagination

class CategoryCreateAPIView(ModelCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyAPIView(ModelRetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class VisitorAppointmentCreateAPIView(CreateAPIView):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):

        existing_appointment = Appointment.objects.filter(
            date=serializer.validated_data['date'],
            time=serializer.validated_data['time']
        ).first()

        if existing_appointment:
            return Response({'error': 'Sie haben bereits einen Termin für dieses Datum und diese Uhrzeit.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()


class VisitorReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        

        existing_review = Review.objects.filter(
            
            barber=serializer.validated_data['barber'],
            customer_name=serializer.validated_data['customer_name']
        ).first()

        if existing_review:
            return Response({'error': 'Sie haben bereits eine Bewertung für diesen Friseur mit dem gleichen Namen abgegeben.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        review_data = response.data
        # Render the new review HTML
        new_review_html = render_to_string('include/reviews.html', {'review': review_data})
        return Response({'html': new_review_html})


class VisitorAppointmentListAPIView(ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
    
        email = self.request.POST.get('email')

        if email:
            return Appointment.objects.filter(Q(email=email))
        return Appointment.objects.filter()


class VisitorReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        
        return Review.objects.filter()


class ManagementAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def get_queryset(self):
        appointment_queryset = Appointment.objects.all()
        barber_queryset = Barber.objects.all()
        review_queryset = Review.objects.all()
        gallery_item_queryset = GalleryItem.objects.all()
        category_queryset = Category.objects.all()
        service_queryset = Service.objects.all()

        return {
            'appointment_list': appointment_queryset,
            'barber_list': barber_queryset,
            'review_list': review_queryset,
            'gallery_item_list': gallery_item_queryset,
            'category_list': category_queryset,
            'service_list': service_queryset,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = {
            'appointment_list': AppointmentSerializer(queryset['appointment_list'], many=True).data,
            'barber_list': BarberSerializer(queryset['barber_list'], many=True).data,
            'review_list': ReviewSerializer(queryset['review_list'], many=True).data,
            'gallery_item_list': GalleryItemSerializer(queryset['gallery_item_list'], many=True).data,
            'category_list': CategorySerializer(queryset['category_list'], many=True).data,
            'service_list': ServiceSerializer(queryset['service_list'], many=True).data,
        }
        return Response(data)