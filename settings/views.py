from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import FormView
from contact.forms import AppointmentForm
from contact.models import GalleryItem, Barber, Review, Appointment
from contact.views import OwnerProfileRequiredMixin


class HomeView(FormView):
    template_name = 'settings/home.html'
    form_class = AppointmentForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_items'] = GalleryItem.objects.all()[:10]
        context['barbers'] = Barber.objects.all()[:10]
        context['reviews'] = Review.objects.all()[:10]
        
        # Debugging output
        print("Gallery Items:", context['gallery_items'])
        print("Barbers:", context['barbers'])
        print("Reviews:", context['reviews'])
        
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.save()
            messages.success(self.request, "Appointment created successfully.")
            return redirect('home')
        else:
            raise Http404("Sie müssen angemeldet sein, um einen Termin zu erstellen.")

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create appointment. Please check the form.")
        return super().form_invalid(form)


home_view = HomeView.as_view()

