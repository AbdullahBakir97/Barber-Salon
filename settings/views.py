from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
from contact.forms import AppointmentForm
from contact.models import Owner, GalleryItem, Barber, Review, Appointment, Service, Category, Product

class HomeView(FormView):
    template_name = 'settings/home.html'
    form_class = AppointmentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_items'] = GalleryItem.objects.all()[:10]
        context['product'] = Product.objects.all()[:10]
        context['barbers'] = Barber.objects.all()[:10]
        context['categories'] = Category.objects.prefetch_related('service_category').all()
        context['services'] = Service.objects.all()
        owner = Owner.objects.first()
        if owner:
            context['owner'] = owner
            
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.save()
            messages.success(self.request, _("Termin erfolgreich erstellt."))
            return redirect('home')
        else:
            raise Http404(_("Sie müssen angemeldet sein, um einen Termin zu erstellen."))

    def form_invalid(self, form):
        messages.error(self.request, _("Termin konnte nicht erstellt werden. Bitte überprüfen Sie das Formular."))
        return super().form_invalid(form)

home_view = HomeView.as_view()

