from django.urls import path
from .views import (
    OwnerCreateView,
    OwnerUpdateView,
    OwnerDeleteView,
    OwnerListView,
    BarberCreateView,
    BarberUpdateView,
    BarberDeleteView,
    BarberListView,
    BarberManagementView,
    GalleryItemCreateView,
    GalleryItemUpdateView,
    GalleryItemDeleteView,
    GalleryItemListView,
    GalleryItemManagementView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewListView,
    ReviewManagementView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    AppointmentListView,
    AppointmentManagementView,
    VisitorAppointmentCreateView,
    VisitorReviewCreateView,
    VisitorAppointmentListView,
    VisitorReviewListView,
    
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView,
    
    ManagementView,

    create_visitor_review,
    submit_review,
    
    contact_view,
    pricing_view
)

app_name = 'contact'

urlpatterns = [
    # Owner Views
    path('owners/create/', OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/update/', OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
    path('owners/', OwnerListView.as_view(), name='owner_list'),

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
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/management', AppointmentManagementView.as_view(), name='appointment_management'),
    
    path('service/add/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('service/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),

    # Visitor Views
    path('visitor/appointments/create/', VisitorAppointmentCreateView.as_view(), name='visitor_appointment_create'),
    path('visitor/reviews/create/', create_visitor_review, name='visitor_review_create'),
    path('visitor/appointments/', VisitorAppointmentListView.as_view(), name='visitor_appointment_list'),
    path('visitor/reviews/', VisitorReviewListView.as_view(), name='visitor_review_list'),

    path('management/', ManagementView.as_view(), name='management'),
    
    path('contact/', contact_view, name='contact'),
    path('pricing/', pricing_view, name='pricing'),
]
