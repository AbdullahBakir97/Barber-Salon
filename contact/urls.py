from django.urls import path
from .views import (
    OwnerDashboardView, 
    AppointmentManagementView, 
    BarberCreateView, 
    BarberUpdateView, 
    BarberDeleteView,
    BarberListView,
    GalleryItemCreateView, 
    GalleryItemUpdateView, 
    GalleryItemDeleteView,
    GalleryItemListView,
    OwnerProfileUpdateView,
    OwnerManagementView,
    add_review,
    AppointmentListView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    ReviewDeleteView,
    ReviewListView
)

urlpatterns = [
    path('dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('appointments/', AppointmentManagementView.as_view(), name='appointment_management'),
    path('appointments/list/', AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),


    path('barbers/create/', BarberCreateView.as_view(), name='barber_create'),
    path('barbers/list/', BarberListView.as_view(), name='barber_list'),
    path('barbers/<int:pk>/update/', BarberUpdateView.as_view(), name='barber_update'),
    path('barbers/<int:pk>/delete/', BarberDeleteView.as_view(), name='barber_delete'),
    
    path('barbers/<int:barber_id>/reviews/add/', add_review, name='add_review'),
    # path('reviews/add/<int:barber_id>/', add_review, name='add_review'),
    path('reviews/list/', ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    

    path('gallery-items/create/', GalleryItemCreateView.as_view(), name='galleryitem_create'),
    path('gallery-items/list/', GalleryItemListView.as_view(), name='galleryitem_list'),
    path('gallery-items/<int:pk>/update/', GalleryItemUpdateView.as_view(), name='galleryitem_update'),
    path('gallery-items/<int:pk>/delete/', GalleryItemDeleteView.as_view(), name='galleryitem_delete'),
    

    path('owner/<int:pk>/update/', OwnerProfileUpdateView.as_view(), name='owner_update'),
    path('owner/<int:pk>/', OwnerManagementView.as_view(), name='owner_management'),
]
