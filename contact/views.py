from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Owner, Barber, Review, GalleryItem, Appointment
from .forms import OwnerForm, BarberForm, GalleryItemForm, ReviewCreateForm, AppointmentForm
from django.http import Http404
from django.db import IntegrityError
from django.contrib import messages
import uuid


# Owner

class OwnerProfileRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        owner_profile = request.user.owner_user_profile
        if not owner_profile:
            raise Http404(_("Sie dürfen diese Seite nicht anzeigen."))
        return super().dispatch(request, *args, **kwargs)
    
    
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

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.owner
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen dieses Friseurprofil nicht bearbeiten."))
        return super().dispatch(request, *args, **kwargs)

class BarberDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Barber
    template_name = 'barber_confirm_delete.html'
    success_url = reverse_lazy('barber_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.owner
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen dieses Friseurprofil nicht löschen."))
        return super().dispatch(request, *args, **kwargs)

class BarberListView(OwnerProfileRequiredMixin, ListView):
    model = Barber
    template_name = 'barber_list.html'


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

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.user.owner_user_profile
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen dieses Galerieelement nicht bearbeiten."))
        return super().dispatch(request, *args, **kwargs)

class GalleryItemDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = GalleryItem
    template_name = 'galleryitem_confirm_delete.html'
    success_url = reverse_lazy('galleryitem_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.user.owner_user_profile
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen dieses Galerieelement nicht löschen."))
        return super().dispatch(request, *args, **kwargs)

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

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.user.owner_user_profile
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen diese Bewertung nicht bearbeiten."))
        return super().dispatch(request, *args, **kwargs)

class ReviewDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.user.owner_user_profile
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen diese Bewertung nicht löschen."))
        return super().dispatch(request, *args, **kwargs)

class ReviewListView(OwnerProfileRequiredMixin, ListView):
    model = Review
    template_name = 'review_list.html'

# Appointment
class AppointmentCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        barber_id = self.kwargs.get('barber_id')
        barber = get_object_or_404(Barber, id=barber_id)
        form.instance.barber = barber
        if owner_profile:
            form.instance.user = self.request.user
            try:
                self.object = form.save()
                messages.success(self.request, _('Termin erfolgreich hinzugefügt.'))
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Ein Termin für diesen Benutzer für denselben Friseur und dasselbe Datum existiert bereits.'))
                return self.form_invalid(form)
        else:
            raise Http404(_("Sie dürfen keinen Termin erstellen."))
        
        
class AppointmentUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.user.owner_user_profile
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen diesen Termin nicht bearbeiten."))
        return super().dispatch(request, *args, **kwargs)

class AppointmentDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner_profile = obj.user.owner_user_profile
        if request.user != owner_profile.user:
            raise Http404(_("Sie dürfen diesen Termin nicht löschen."))
        return super().dispatch(request, *args, **kwargs)

class AppointmentListView(OwnerProfileRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointment_list.html'



# Visitor Views
class VisitorAppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list_visitor')

    def form_valid(self, form):
        
        visitor_id = self.request.session.get('visitor_id', None)
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
            self.request.session['visitor_id'] = visitor_id

        form.instance.visitor_id = visitor_id
        
        try:
            self.object = form.save()
            messages.success(self.request, _('Termin erfolgreich hinzugefügt.'))
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('Sie haben bereits einen Termin für dieses Datum und diese Uhrzeit.'))
            return self.form_invalid(form)

class VisitorReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list_visitor')

    def form_valid(self, form):
        
        visitor_id = self.request.session.get('visitor_id', str(uuid.uuid4()))
        self.request.session['visitor_id'] = visitor_id
            
        form.instance.visitor_id = visitor_id
        
        try:
            self.object = form.save()
            messages.success(self.request, _('Bewertung erfolgreich hinzugefügt.'))
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('Sie haben diesen Friseur bereits bewertet.'))
            return self.form_invalid(form)

class VisitorAppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_list_visitor.html'

    def get_queryset(self):
        
        visitor_id = self.request.session.get('visitor_id', None)
        if visitor_id:
            return Appointment.objects.filter(visitor_id=visitor_id)
        return Appointment.objects.none()
        

class VisitorReviewListView(ListView):
    model = Review
    template_name = 'review_list_visitor.html'

    def get_queryset(self):
        visitor_id = self.request.session.get('visitor_id', None)
        if visitor_id:
            
            visitor_reviews = Review.objects.filter(visitor_id=visitor_id)
            other_reviews = Review.objects.exclude(visitor_id=visitor_id)
            return list(visitor_reviews) + list(other_reviews)
        return Review.objects.all()


# Owner Views

class OwnerAppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointment_list_owner')

    def form_valid(self, form):
        owner_profile = self.request.user.owner_user_profile
        if owner_profile:
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