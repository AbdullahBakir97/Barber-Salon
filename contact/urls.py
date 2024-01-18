from django.urls import path
from .views import (
    OwnerDashboardView,
    AppointmentManagementView,
    BarberCreateUpdateDeleteView,
    GalleryItemCreateUpdateDeleteView,
    ReviewCreateUpdateDeleteView,
    OwnerProfileUpdateView,
    OwnerManagementView,
    AppointmentListView,
    AppointmentCreateUpdateDeleteView,
    ReviewListView,
    BarberListView,
    GalleryItemListView,
    CreateReviewView,
    CreateAppointmentView
)

urlpatterns = [
    path('dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),

    path('appointments/', AppointmentManagementView.as_view(), name='appointment_management'),
    path('appointments/list/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', AppointmentCreateUpdateDeleteView.as_view(), name='appointment_management'),
    path('appointments/<int:pk>/update/', AppointmentCreateUpdateDeleteView.as_view(), name='appointment_management'),
    path('appointments/<int:pk>/delete/', AppointmentCreateUpdateDeleteView.as_view(), name='appointment_delete'),

    path('appointments/geust/', CreateAppointmentView.as_view(), name='appointment_create'),
    
    path('barbers/list/', BarberListView.as_view(), name='barber_list'),
    path('barbers/create/', BarberCreateUpdateDeleteView.as_view(), name='barber_create'),
    path('barbers/<int:pk>/update/', BarberCreateUpdateDeleteView.as_view(), name='barber_update'),
    path('barbers/<int:pk>/delete/', BarberCreateUpdateDeleteView.as_view(), name='barber_delete'),
    
    path('barbers/<int:barber_id>/reviews/add/', CreateReviewView.as_view(), name='add_review'),

    path('reviews/list/', ReviewListView.as_view(), name='review_list'),
    path('appointments/create/', ReviewCreateUpdateDeleteView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewCreateUpdateDeleteView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewCreateUpdateDeleteView.as_view(), name='review_delete'),
    
    
    path('gallery-items/list/', GalleryItemListView.as_view(), name='galleryitem_list'),
    path('gallery-items/create/', GalleryItemCreateUpdateDeleteView.as_view(), name='galleryitem_create'),
    path('gallery-items/<int:pk>/update/', GalleryItemCreateUpdateDeleteView.as_view(), name='galleryitem_update'),
    path('gallery-items/<int:pk>/delete/', GalleryItemCreateUpdateDeleteView.as_view(), name='galleryitem_delete'),

    path('owner/<int:pk>/update/', OwnerProfileUpdateView.as_view(), name='owner_update'),
    path('owner/<int:pk>/', OwnerManagementView.as_view(), name='owner_management'),
]

