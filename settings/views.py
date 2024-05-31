from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404 , HttpResponseRedirect, JsonResponse, HttpResponseServerError, HttpResponse
from django.db import IntegrityError
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
from contact.forms import AppointmentForm
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from contact.models import Owner, GalleryItem, Barber, Review, Appointment, Service, Category
import logging


logger = logging.getLogger(__name__)


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

home_view = HomeView.as_view()



def visitor_appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            return handle_form_valid(request, form)
        else:
            return handle_form_invalid(request, form)
    else:
        form = AppointmentForm()
        return render(request, 'settings/home.html', {'form': form})

def handle_form_valid(request, form):
    try:
        appointment = form.save()

        send_appointment_email(
            name=appointment.name,
            barber=appointment.barber,
            email=appointment.email,
            date=appointment.date,
            time=appointment.time,
            service_type=appointment.service_type,
            phone=appointment.phone,
            message=appointment.message
        )

        # Set a success message
        messages.success(request, 'Ihre Termin wurde erfolgreich gesendet!')
        return JsonResponse({'result': 'success', 'message': 'Ihre Termin wurde erfolgreich gesendet!'})
    except IntegrityError as e:
        logger.error(f'Error saving appointment: {e}')
        messages.error(request, 'Fehler beim Speichern des Termins. Bitte versuchen Sie es erneut.')
        return JsonResponse({'result': 'error', 'message': 'Fehler beim Speichern des Termins. Bitte versuchen Sie es erneut.'}, status=400)
    except Exception as e:
        logger.error(f'Error sending appointment email: {e}')
        messages.error(request, 'Fehler beim Senden der Termin-E-Mail. Bitte versuchen Sie es später erneut.')
        return JsonResponse({'result': 'error', 'message': 'Fehler beim Senden der Termin-E-Mail. Bitte versuchen Sie es später erneut.'})

def handle_form_invalid(request, form):
    errors = "\n".join([f" {errors[0]}" for field, errors in form.errors.items()])  
    error_message = f"Bitte überprüfen Sie Ihre Eingaben.\n{errors}"
    return HttpResponse(error_message, status=400, content_type="text/plain")

def send_appointment_email(name, barber, email, date, time, service_type, phone, message):
    try:
        formatted_time = time.strftime('%I:%M %p')
        send_mail(
            f'Ihr wunsch Termin wurde bestätigt',
            f'Name: {name}\nE-Mail: {email}\nTelefonnummer: {phone}\nNachricht: {message if message else "Keine zusätzliche Nachricht"}\nDatum: {date}\nUhrzeit: {formatted_time}\nDienstleistungsart: {service_type}\nFriseur: {barber}',
            email,
            [settings.EMAIL_HOST_USER, email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        raise e  # Reraise the exception to handle it in the caller function

def handl404(request, exception):
    return render(request, 'settings/404.html', status=404)

def handl500(request):
    return render(request, 'settings/500.html', status=500)


