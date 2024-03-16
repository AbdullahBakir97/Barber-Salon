from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404 , HttpResponseRedirect, JsonResponse, HttpResponseServerError
from django.db import IntegrityError
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
from contact.forms import AppointmentForm
from contact.models import Owner, GalleryItem, Barber, Review, Appointment, Service, Category, Product

class HomeView(FormView):
    template_name = 'settings/home.html'
    form_class = AppointmentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_items'] = GalleryItem.objects.all()
        context['products'] = Product.objects.all()
        context['barbers'] = Barber.objects.all()
        context['categories'] = Category.objects.prefetch_related('service_category').all()
        context['services'] = Service.objects.all()
        owner = Owner.objects.first()
        if owner:
            context['owner'] = owner
        return context

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Ihre Termin wurde erfolgreich gesendet!')
        except IntegrityError as e:
            messages.error(self.request, 'Fehler beim Senden des Formulars. Bitte versuchen Sie es erneut.')
        return HttpResponseRedirect(reverse('home') + '#appointments')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        # Set a flag to scroll to appointments section
        self.request.session['scroll_to_appointments'] = True
        return super().form_invalid(form)

home_view = HomeView.as_view()

