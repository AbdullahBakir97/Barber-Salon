from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Owner, Barber, Review, GalleryItem, Appointment
from .forms import ReviewCreateForm, AppointmentForm, BarberForm, GalleryItemForm
from django.contrib.auth.decorators import login_required

class OwnerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'owner_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(user=self.request.user)
        context['reviews'] = Review.objects.filter(user=self.request.user)
        context['barbers'] = Barber.objects.filter(owner__user=self.request.user)
        context['gallery_items'] = GalleryItem.objects.filter(user=self.request.user)
        return context

class AppointmentManagementView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'appointment_management.html'
    paginate_by = 10

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    
class GalleryItemListView(LoginRequiredMixin, ListView):
    model = GalleryItem
    template_name = 'galleryitem_list.html'
    context_object_name = 'gallery_items'
    paginate_by = 10
    
    
class BarberListView(LoginRequiredMixin, ListView):
    model = Barber
    template_name = 'barber_list.html'
    context_object_name = 'barbers'
    paginate_by = 10
    

class BarberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Barber
    form_class = BarberForm
    template_name = 'barber_form.html'
    success_message = 'Barber created successfully.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GalleryItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'galleryitem_form.html'
    success_message = 'Gallery item created successfully.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OwnerManagementView(LoginRequiredMixin, DetailView):
    model = Owner
    template_name = 'owner_management.html'

def add_review(request, barber_id):
    barber = get_object_or_404(Barber, id=barber_id)

    if request.method == 'POST':
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.barber = barber

            # Check if the user is authenticated (owner)
            if request.user == barber.owner.user:
                review.save()  # Owner can save the review
                messages.success(request, 'Review added successfully.')
                return redirect('barber_detail', pk=barber_id)

            # If the user is a guest, handle accordingly
            else:
                try:
                    review.save()
                    messages.success(request, 'Review added successfully.')
                except IntegrityError:
                    messages.error(request, 'You have already submitted a review for this barber.')

    else:
        form = ReviewCreateForm()

    return render(request, 'add_review.html', {'form': form, 'barber': barber})

class AppointmentCreateView(SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_message = 'Appointment created successfully.'

    def form_valid(self, form):
        # If user is authenticated, set the user field in the appointment
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

            # Check for duplicate appointment
            if Appointment.objects.filter(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                barber=form.cleaned_data['barber']
            ).exists():
                messages.error(self.request, 'Appointment with the same name, date, time, and barber already exists.')
                return redirect('appointment_create')

        return super().form_valid(form)

    def get_success_url(self):
        pass
    
class OwnerAccessMixin(UserPassesTestMixin):
    raise_exception = True  # Raise PermissionDenied if the test fails

    def test_func(self):
        # Check if the user is the owner of the related object
        user = self.request.user
        obj = self.get_object()
        return user == obj.owner.user

class AppointmentDeleteView(OwnerAccessMixin, DeleteView):
    model = Appointment
    template_name = 'appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_management')  # Redirect after successful deletion

class BarberDeleteView(OwnerAccessMixin, DeleteView):
    model = Barber
    template_name = 'barber_confirm_delete.html'
    success_url = reverse_lazy('barber_list')  # Redirect after successful deletion

class GalleryItemDeleteView(OwnerAccessMixin, DeleteView):
    model = GalleryItem
    template_name = 'galleryitem_confirm_delete.html'
    success_url = reverse_lazy('gallery_list')  # Redirect after successful deletion

class ReviewDeleteView(OwnerAccessMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')  # Redirect after successful deletion

class AppointmentUpdateView(OwnerAccessMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_message = 'Appointment updated successfully.'


class BarberUpdateView(OwnerAccessMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Barber
    form_class = BarberForm
    template_name = 'barber_form.html'
    success_message = 'Barber updated successfully.'

class GalleryItemUpdateView(OwnerAccessMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'galleryitem_form.html'
    success_message = 'Gallery item updated successfully.'


class OwnerProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Owner
    fields = ['name', 'email', 'phone', 'address', 'logo', 'website', 'about', 'social_media_links']
    template_name = 'owner_form.html'
    success_message = 'Profile updated successfully.'
    

