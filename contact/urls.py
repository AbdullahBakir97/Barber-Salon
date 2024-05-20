from django.urls import path
from .views import (
    OwnerCreateView,    OwnerUpdateView, OwnerDeleteView, OwnerDetailView,
    BarberCreateView,   BarberUpdateView, BarberDeleteView, BarberListView, BarberManagementView,
    GalleryItemCreateView,  GalleryItemUpdateView, GalleryItemDeleteView, GalleryItemListView, GalleryItemManagementView,
    ReviewCreateView,   ReviewUpdateView ,ReviewDeleteView, ReviewListView, ReviewManagementView,
    AppointmentCreateView,  AppointmentUpdateView, AppointmentDeleteView, AppointmentListView, AppointmentManagementView,
    VisitorAppointmentCreateView,   VisitorReviewCreateView, VisitorAppointmentListView, VisitorReviewListView,visitor_appointment_create,
    CategoryCreateView,     CategoryUpdateView, CategoryDeleteView,
    ServiceCreateView,  ServiceUpdateView, ServiceDeleteView, ServiceManagementView,

    management_view,
    create_visitor_review,
    appointment_create,
    submit_review,
    contact_view,
    MessageDeleteView,
    pricing_view
)

from .api import (
    ContactAPIView,
    BarberListAPIView, BarberCreateAPIView, BarberRetrieveUpdateDestroyAPIView,
    ReviewListAPIView, ReviewCreateAPIView, ReviewRetrieveUpdateDestroyAPIView,
    GalleryItemListAPIView, GalleryItemCreateAPIView, GalleryItemRetrieveUpdateDestroyAPIView,
    AppointmentListAPIView, AppointmentCreateAPIView, AppointmentRetrieveUpdateDestroyAPIView,
    MessageListAPIView, MessageCreateAPIView, MessageRetrieveUpdateDestroyAPIView,
    ServiceListAPIView, ServiceCreateAPIView, ServiceRetrieveUpdateDestroyAPIView,
    CategoryListAPIView, CategoryCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    VisitorAppointmentCreateAPIView, VisitorReviewCreateAPIView,
    VisitorAppointmentListAPIView, VisitorReviewListAPIView,
    ManagementAPIView,
)

app_name = 'contact'

urlpatterns = [
    # Owner Views
    path('owners/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/update/', OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
    path('owners/<int:pk>', OwnerDetailView.as_view(), name='owner_detail'),

    # Barber Views
    path('barbers/create/', BarberCreateView.as_view(), name='barber_create'),
    path('barbers/<int:pk>/update/', BarberUpdateView.as_view(), name='barber_update'),
    path('barbers/<int:pk>/delete/', BarberDeleteView.as_view(), name='barber_delete'),
    path('barbers/', BarberListView.as_view(), name='barber_list'),
    path('barbers/management', BarberManagementView.as_view(), name='barber_management'),

    # GalleryItem Views
    path('items/create/', GalleryItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/update/', GalleryItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', GalleryItemDeleteView.as_view(), name='item_delete'),
    path('items/', GalleryItemListView.as_view(), name='item_list'),
    path('items/management', GalleryItemManagementView.as_view(), name='item_management'),
    
    # Review Views
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/management', ReviewManagementView.as_view(), name='review_management'),

    # Appointment Views
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/add/', appointment_create, name='create_appointment'),
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/management', AppointmentManagementView.as_view(), name='appointment_management'),
    
    # Category Views
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
    
    path('service/add/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    path('service/management', ServiceManagementView.as_view(), name='service_management'),

    # Visitor Views
    path('visitor/appointments/create/', visitor_appointment_create, name='visitor_appointment_create'),
    path('visitor/reviews/create/', create_visitor_review, name='visitor_review_create'),
    path('visitor/appointments/', VisitorAppointmentListView.as_view(), name='visitor_appointment_list'),
    path('visitor/reviews/', VisitorReviewListView.as_view(), name='visitor_review_list'),

    path('management/', management_view, name='management'),
    
    path('contact/', contact_view, name='contact'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('pricing/', pricing_view, name='pricing'),
    
    
    # API Views
    path('api/contact/', ContactAPIView.as_view(), name='contact-api'),
    
    path('api/barbers/', BarberListAPIView.as_view({'get': 'list'}), name='barber-list-api'),
    path('api/barbers/create/', BarberCreateAPIView.as_view(), name='barber-create-api'),
    path('api/barbers/<int:pk>/', BarberRetrieveUpdateDestroyAPIView.as_view(), name='barber-detail-api'),
    
    path('api/reviews/', ReviewListAPIView.as_view(), name='review-list-api'),
    path('api/reviews/create/', ReviewCreateAPIView.as_view(), name='review-create-api'),
    path('api/reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail-api'),
    
    path('api/items/', GalleryItemListAPIView.as_view(), name='gallery-item-list-api'),
    path('api/items/create/', GalleryItemCreateAPIView.as_view(), name='gallery-item-create-api'),
    path('api/items/<int:pk>/', GalleryItemRetrieveUpdateDestroyAPIView.as_view(), name='gallery-item-detail-api'),
    
    path('api/appointments/', AppointmentListAPIView.as_view({'get': 'list'}), name='appointment-list-api'),
    path('api/appointments/create/', AppointmentCreateAPIView.as_view(), name='appointment-create-api'),
    path('api/appointments/<int:pk>/', AppointmentRetrieveUpdateDestroyAPIView.as_view(), name='appointment-detail-api'),
    
    path('api/messages/', MessageListAPIView.as_view(), name='message-list-api'),
    path('api/messages/create/', MessageCreateAPIView.as_view(), name='message-create-api'),
    path('api/messages/<int:pk>/', MessageRetrieveUpdateDestroyAPIView.as_view(), name='message-detail-api'),
    
    path('api/services/', ServiceListAPIView.as_view(), name='service-list-api'),
    path('api/services/create/', ServiceCreateAPIView.as_view(), name='service-create-api'),
    path('api/services/<int:pk>/', ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail-api'),
    
    path('api/categories/', CategoryListAPIView.as_view(), name='category-list-api'),
    path('api/categories/create/', CategoryCreateAPIView.as_view(), name='category-create-api'),
    path('api/categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail-api'),
    
    path('api/visitors/appointments/create/', VisitorAppointmentCreateAPIView.as_view(), name='visitor-appointment-create-api'),
    path('api/visitors/reviews/create/', VisitorReviewCreateAPIView.as_view(), name='visitor-review-create-api'),
    path('api/visitors/appointments/', VisitorAppointmentListAPIView.as_view(), name='visitor-appointment-list-api'),
    path('api/visitors/reviews/', VisitorReviewListAPIView.as_view(), name='visitor-review-list-api'),
    
    path('api/management/', ManagementAPIView.as_view(), name='management-list-api'),
]

