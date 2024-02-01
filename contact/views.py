from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Owner, Barber, Review, GalleryItem, Appointment
from .forms import OwnerForm, BarberForm, GalleryItemForm, ReviewCreateForm, AppointmentForm
from django.http import Http404
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages
import uuid
import logging

logger = logging.getLogger(__name__)


# Owner

class OwnerProfileRequiredMixin(LoginRequiredMixin):
    # def dispatch(self, request, *args, **kwargs):
    #     owner_profile = request.user.owner_user_profile
    #     if not owner_profile:
    #         raise Http404(_("Sie dürfen diese Seite nicht anzeigen."))
    #     return super().dispatch(request, *args, **kwargs)
    pass

    
class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    fields = ['name', 'email', 'phone', 'address', 'logo', 'website', 'about', 'social_media_links']
    template_name = 'owner_form.html'
    success_url = reverse_lazy('owner_list') 

    def form_valid(self, form):
        if not self.request.user.is_authenticated or not hasattr(self.request.user, 'owner_user_profile'):
            raise Http404(_("Sie dürfen kein Eigentümerprofil erstellen."))

        # Check if an owner profile already exists for the user
        if Owner.objects.filter(user=self.request.user).exists():
            messages.error(self.request, _('Ein Eigentümerprofil für diesen Benutzer existiert bereits. Sie können es stattdessen bearbeiten.'))
            return self.form_invalid(form)

        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('Ein Eigentümer mit dieser E-Mail existiert bereits.'))
            return self.form_invalid(form)


class OwnerUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Owner
    fields = ['name', 'email', 'phone', 'address', 'logo', 'website', 'about', 'social_media_links']
    template_name = 'owner_form.html'
    success_url = reverse_lazy('owner_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.owner
        if (
            request.user != owner_profile.user
            or Owner.objects.filter(user=request.user).exclude(pk=obj.pk).exists()
        ):
            raise Http404(_("Sie dürfen dieses Eigentümerprofil nicht bearbeiten."))
        return super().dispatch(request, *args, **kwargs)
        
        
class OwnerDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Owner
    template_name = 'owner_confirm_delete.html'
    success_url = reverse_lazy('owner_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.user:
            raise Http404(_("Sie dürfen dieses Eigentümerprofil nicht löschen."))
        return super().dispatch(request, *args, **kwargs)

class OwnerListView(OwnerProfileRequiredMixin, ListView):
    model = Owner
    template_name = 'owner_list.html'
    
    

# Barber
class BarberCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Barber
    form_class = BarberForm
    template_name = 'barber_form.html'
    success_url = reverse_lazy('barber_list')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        barber_id = self.kwargs.get('barber_id')
        barber = get_object_or_404(Barber, id=barber_id)
        form.instance.barber = barber
        if owner_profile:
            form.instance.owner = owner_profile
            try:
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Ein Friseur mit diesem Namen existiert bereits.'))
                return self.form_invalid(form)
        else:
            raise Http404(_("Sie dürfen kein Friseurprofil erstellen."))

class BarberUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Barber
    form_class = BarberForm
    template_name = 'barber_form.html'
    success_url = reverse_lazy('barber_list')



class BarberDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Barber
    template_name = 'barber_confirm_delete.html'
    success_url = reverse_lazy('contact/barber/barber_list.html')



class BarberListView(OwnerProfileRequiredMixin, ListView):
    model = Barber
    template_name = 'contact/barber/barber_list.html'
    
    def get_queryset(self):
        return Barber.objects.all()
    
    
class BarberManagementView(
    OwnerProfileRequiredMixin,
    CreateView,
    UpdateView,
    DeleteView,
    ListView
):
    model = Barber
    form_class = BarberForm
    template_name = 'barber_form.html'
    success_url = reverse_lazy('barber_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all()
        return context

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        barber_id = self.kwargs.get('barber_id')
        barber = get_object_or_404(Barber, id=barber_id)
        form.instance.barber = barber
        if owner_profile:
            form.instance.owner = owner_profile
            try:
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Ein Friseur mit diesem Namen existiert bereits.'))
                return self.form_invalid(form)
        else:
            raise Http404(_("Sie dürfen kein Friseurprofil erstellen."))

    def delete(self, request, *args, **kwargs):
        # Add custom delete logic if needed
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('barber_list')
    
    


# GalleryItem
class GalleryItemCreateView(OwnerProfileRequiredMixin, CreateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'galleryitem_form.html'
    success_url = reverse_lazy('galleryitem_list')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        if owner_profile:
            form.instance.user = self.request.user
            try:
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Ein Element mit diesem Titel existiert bereits.'))
                return self.form_invalid(form)
        else:
            raise Http404(_("Sie dürfen kein Galerieelement erstellen."))

class GalleryItemUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'galleryitem_form.html'
    success_url = reverse_lazy('galleryitem_list')



class GalleryItemDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = GalleryItem
    template_name = 'galleryitem_confirm_delete.html'
    success_url = reverse_lazy('galleryitem_list')



class GalleryItemListView(OwnerProfileRequiredMixin, ListView):
    model = GalleryItem
    template_name = 'galleryitem_list.html'
    

# Review
class ReviewCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        if owner_profile:
            form.instance.user = self.request.user
            try:
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Eine Bewertung von diesem Benutzer für denselben Friseur existiert bereits.'))
                return self.form_invalid(form)
        else:
            raise Http404(_("Sie dürfen keine Bewertung erstellen."))

class ReviewUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list')



class ReviewDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')



class ReviewListView(OwnerProfileRequiredMixin, ListView):
    model = Review
    template_name = 'review_list.html'
    

# Appointment
class AppointmentCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'contact/appointment/appointment_create.html'
    success_url = reverse_lazy('contact:appointment_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            raise Http404(_("Sie müssen angemeldet sein, um einen Termin zu erstellen."))

class AppointmentUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'contact/appointment/appointment_update.html'

    def get_success_url(self):
        return reverse('contact:appointment_list')
    


class AppointmentDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'contact/appointment/appointment_delete.html'
    
    def get_success_url(self):
        return reverse('contact:appointment_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Appointment, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        appointment.delete()
        return HttpResponseRedirect(self.get_success_url())



class AppointmentListView(OwnerProfileRequiredMixin, ListView):
    model = Appointment
    template_name = 'contact/appointment/appointment_management.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title()
        return context


# Visitor Views
class VisitorIdMixin:
    def get_visitor_id(self):
        visitor_id = self.request.session.get('visitor_id', None)
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
            self.request.session['visitor_id'] = visitor_id
        return visitor_id
    
    
class VisitorAppointmentCreateView(VisitorIdMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        visitor_id = self.get_visitor_id()
        form.instance.visitor_id = visitor_id
        try:
            self.object = form.save()
            success_message = _('Termin erfolgreich hinzugefügt.')
            messages.success(self.request, success_message)
            return super().form_valid(form)
        except IntegrityError:
            error_message = _('Sie haben bereits einen Termin für dieses Datum und diese Uhrzeit.')
            messages.error(self.request, error_message)
            return self.form_invalid(form)

class VisitorReviewCreateView(VisitorIdMixin,CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list_visitor')

    def form_valid(self, form):
        
        visitor_id = self.get_visitor_id()
        form.instance.visitor_id = visitor_id
        
        try:
            self.object = form.save()
            messages.success(self.request, _('Bewertung erfolgreich hinzugefügt.'))
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('Sie haben diesen Friseur bereits bewertet.'))
            return self.form_invalid(form)

class VisitorAppointmentListView(VisitorIdMixin, ListView):
    model = Appointment
    template_name = 'appointment_list.html'

    def get_queryset(self):
        visitor_id = self.get_visitor_id()
        return Appointment.objects.filter(visitor_id=visitor_id)
        

class VisitorReviewListView(VisitorIdMixin, ListView):
    model = Review
    template_name = 'review_list_visitor.html'

    def get_queryset(self):

            visitor_id = self.get_visitor_id()
            visitor_reviews = Review.objects.filter(visitor_id=visitor_id)
            other_reviews = Review.objects.exclude(visitor_id=visitor_id)
            return list(visitor_reviews) + list(other_reviews)


# Owner Views
class OwnerAppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list_owner')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        form.instance.user = self.request.user
        try:
            self.object = form.save()
            messages.success(self.request, _('Termin erfolgreich hinzugefügt.'))
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('Ein Termin für dieses Datum, diese Uhrzeit und diesen Friseur existiert bereits.'))
        else:
            raise Http404("Sie dürfen keinen Termin hinzufügen.")

        return redirect('appointment_list_owner')

class OwnerReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list_owner')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        if owner_profile:
            form.instance.user = self.request.user
            try:
                self.object = form.save()
                messages.success(self.request, _('Bewertung erfolgreich hinzugefügt.'))
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Sie haben diesen Friseur bereits bewertet.'))
        else:
            raise Http404("Sie dürfen keine Bewertung hinzufügen.")

        return redirect('review_list_owner')

class OwnerAppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointment_list_owner.html'

    def get_queryset(self):
        # Zeige alle Termine für den Besitzer
        owner_profile = self.request.user.owner_user_profile
        if owner_profile:
            return Appointment.objects.all()
        return Appointment.objects.none()

class OwnerReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review_list_owner.html'

    def get_queryset(self):
        # Zeige alle Bewertungen für den Besitzer
        owner_profile = self.request.user.owner_user_profile
        if owner_profile:
            return Review.objects.all()
        return Review.objects.none()