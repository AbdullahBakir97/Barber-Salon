from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from .models import Owner, Barber, Review, GalleryItem, Appointment
from .forms import ReviewCreateForm, AppointmentForm, BarberForm, GalleryItemForm


class CreateReviewView(SuccessMessageMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_create.html'
    success_message = _('Bewertung erfolgreich hinzugefügt.')

    def form_valid(self, form):
        barber_id = self.kwargs['barber_id']
        barber = get_object_or_404(Barber, id=barber_id)
        form.instance.barber = barber

        try:
            form.save()
            messages.success(self.request, self.success_message)
        except IntegrityError:
            messages.error(self.request, _('Sie haben bereits eine Bewertung für diesen Friseur abgegeben.'))

        return redirect('barber_list')


class CreateAppointmentView(SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment.html'
    success_message = _('Termin erfolgreich erstellt.')

    def form_valid(self, form):
        form.instance.user = None  # Set user to None for guests
        try:
            form.save()
            messages.success(self.request, self.success_message)
        except IntegrityError:
            messages.error(self.request, _('Termin mit denselben Details existiert bereits.'))

        return redirect('about')  # Adjust the redirect URL as needed
class OwnerAccessMixin(UserPassesTestMixin):
    raise_exception = True  # Raise PermissionDenied if the test fails

    def test_func(self):
        # Check if the user is the owner of the related object
        user = self.request.user
        obj = self.get_object()
        return user == obj.owner.user

class CreateUpdateDeleteView(UserPassesTestMixin, SuccessMessageMixin, TemplateView):
    model = None
    form_class = None
    template_name = None
    success_message = None

    def test_func(self):
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(user=self.request.user)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        if 'create' in request.POST:
            return self.create(request, *args, **kwargs)
        elif 'update' in request.POST:
            return self.update(request, *args, **kwargs)
        elif 'delete' in request.POST:
            return self.delete(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, _(f'{self.model.__name__} erfolgreich erstellt.'))
        else:
            messages.error(request, _(f'Fehler beim Erstellen von {self.model.__name__}. Bitte überprüfen Sie das Formular.'))
        return redirect(self.get_success_url())

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, id=request.POST.get('update_id'))
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, _(f'{self.model.__name__} erfolgreich aktualisiert.'))
        else:
            messages.error(request, _(f'Fehler beim Aktualisieren von {self.model.__name__}. Bitte überprüfen Sie das Formular.'))
        return redirect(self.get_success_url())

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, id=request.POST.get('delete_id'))
        instance.delete()
        messages.success(request, _(f'{self.model.__name__} erfolgreich gelöscht.'))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('dashboard')



class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10
    

class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    
    
class GalleryItemListView(ListView):
    model = GalleryItem
    template_name = 'gallery/item_list.html'
    context_object_name = 'gallery_items'
    paginate_by = 10
    
    
class BarberListView(ListView):
    model = Barber
    template_name = 'barber_list.html'
    context_object_name = 'barbers'
    paginate_by = 10

class AppointmentCreateUpdateDeleteView(UserPassesTestMixin, SuccessMessageMixin, TemplateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_management.html'
    success_message = _('Termin erfolgreich erstellt.')

    def test_func(self):
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Assuming you have a related 'Barber' instance for the logged-in user
        barber = getattr(self.request.user, 'barber', None)

        if barber:
            context['object_list'] = self.model.objects.filter(barber=barber)
            context['form'] = self.form_class()
        else:
            context['object_list'] = []
            context['form'] = None

        return context



class BarberCreateUpdateDeleteView(CreateUpdateDeleteView):
    model = Barber
    form_class = BarberForm
    template_name = 'barber_update.html'

class GalleryItemCreateUpdateDeleteView(CreateUpdateDeleteView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'gallery/item_update.html'

class ReviewCreateUpdateDeleteView(CreateUpdateDeleteView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_update.html'

class OwnerProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Owner
    fields = ['name', 'email', 'phone', 'address', 'logo', 'website', 'about', 'social_media_links']
    template_name = 'owner_form.html'
    success_message = _('Profil erfolgreich aktualisiert.')
    
    def get_object(self, queryset=None):
        return self.request.user.owner

class OwnerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the user has a related Barber instance
        barber = getattr(self.request.user, 'barber', None)

        if barber:
            context['appointments'] = Appointment.objects.filter(barber=barber)
        else:
            context['appointments'] = []

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
        try:
            # reverse relation from Barber to Appointments named 'barber_appointments'
            barber_appointments = self.request.user.barber.barber_appointment.all()
            return barber_appointments
        except AttributeError:
            # Handle the case where the user is not a barber or does not have related appointments
            return Appointment.objects.none()

class OwnerManagementView(
    AppointmentCreateUpdateDeleteView,
    BarberCreateUpdateDeleteView,
    GalleryItemCreateUpdateDeleteView,
    ReviewCreateUpdateDeleteView,
    OwnerProfileUpdateView,
    AppointmentManagementView,
    OwnerDashboardView,
    TemplateView
):
    template_name = 'owner_management.html'