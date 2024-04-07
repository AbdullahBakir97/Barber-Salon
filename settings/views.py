from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404 , HttpResponseRedirect, JsonResponse, HttpResponseServerError, HttpResponse
from django.db import IntegrityError
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
from contact.forms import AppointmentForm
from contact.models import Owner, GalleryItem, Barber, Review, Appointment, Service, Category

class HomeView(FormView):
    template_name = 'settings/home.html'
    form_class = AppointmentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_items'] = GalleryItem.objects.all()
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
            return JsonResponse({'result': 'success', 'message': 'Ihre Termin wurde erfolgreich gesendet!'})
        except IntegrityError as e:
            messages.error(self.request, 'Fehler beim Senden des Formulars. Bitte versuchen Sie es erneut.')
            return JsonResponse({'result': 'error', 'message': 'Fehler beim Senden des Formulars. Bitte versuchen Sie es erneut.'}, status=400)

    def form_invalid(self, form):
        errors = "\n".join([f" {errors[0]}" for field, errors in form.errors.items()])  
        # Construct error messages as plain text
        error_message = f"Bitte überprüfen Sie Ihre Eingaben.\n{errors}"
        return HttpResponse(error_message, status=400, content_type="text/plain")
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

home_view = HomeView.as_view()


def handl404(request, exception):
    return render(request, 'settings/404.html', status=404)

def handl500(request):
    return render(request, 'settings/500.html', status=500)


