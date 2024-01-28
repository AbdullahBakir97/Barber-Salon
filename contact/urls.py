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
    GalleryItemCreateView,
    GalleryItemUpdateView,
    GalleryItemDeleteView,
    GalleryItemListView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewListView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    AppointmentListView,
    VisitorAppointmentCreateView,
    VisitorReviewCreateView,
    VisitorAppointmentListView,
    VisitorReviewListView,
    OwnerAppointmentCreateView,
    OwnerReviewCreateView,
    OwnerAppointmentListView,
    OwnerReviewListView
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

    # GalleryItem Views
    path('galleryitems/create/', GalleryItemCreateView.as_view(), name='galleryitem_create'),
    path('galleryitems/<int:pk>/update/', GalleryItemUpdateView.as_view(), name='galleryitem_update'),
    path('galleryitems/<int:pk>/delete/', GalleryItemDeleteView.as_view(), name='galleryitem_delete'),
    path('galleryitems/', GalleryItemListView.as_view(), name='galleryitem_list'),

    # Review Views
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),

    # Appointment Views
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/', AppointmentListView.as_view(), name='appointment_list'),

    # Visitor Views
    path('visitor/appointments/create/', VisitorAppointmentCreateView.as_view(), name='visitor_appointment_create'),
    path('visitor/reviews/create/', VisitorReviewCreateView.as_view(), name='visitor_review_create'),
    path('visitor/appointments/', VisitorAppointmentListView.as_view(), name='visitor_appointment_list'),
    path('visitor/reviews/', VisitorReviewListView.as_view(), name='visitor_review_list'),

    # Owner Views
    path('owner/appointments/create/', OwnerAppointmentCreateView.as_view(), name='owner_appointment_create'),
    path('owner/reviews/create/', OwnerReviewCreateView.as_view(), name='owner_review_create'),
    path('owner/appointments/', OwnerAppointmentListView.as_view(), name='owner_appointment_list'),
    path('owner/reviews/', OwnerReviewListView.as_view(), name='owner_review_list'),
]
