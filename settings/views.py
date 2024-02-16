from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import FormView
from contact.forms import AppointmentForm
from contact.models import GalleryItem, Barber, Review, Appointment, Service, Category



class HomeView(FormView):
    template_name = 'settings/home.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('home') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_items'] = GalleryItem.objects.all()[:10]
        context['barbers'] = Barber.objects.all()[:10]
        context['categories'] = Category.objects.prefetch_related('service_category').all()
        context['services'] = Service.objects.all()

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

