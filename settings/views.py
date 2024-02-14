from django.shortcuts import render, redirect 
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.http import Http404
from contact.models import GalleryItem, Barber, Review, Appointment
from contact.forms import AppointmentForm
from django.contrib import messages

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'contact/appointment/appointment_create.html'
    success_url = reverse_lazy('contact:appointment_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            self.submitted = True
            return super().form_valid(form)
        else:
            raise Http404("Sie müssen angemeldet sein, um einen Termin zu erstellen.")

    def form_invalid(self, form):
        self.submitted = False
        return self.render_to_response(self.get_context_data(form=form))

def home(request):
    try:
        gallery_items = GalleryItem.objects.all()[:10]
        barbers = Barber.objects.all()[:10]
        reviews = Review.objects.all()[:10]
    except Exception as e:
        
        raise Http404("Failed to fetch data for the home page: {}".format(str(e)))

    if request.method == 'POST':
        
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            if request.user.is_authenticated:
                appointment_form.instance.user = request.user
                appointment_form.save()
                messages.success(request, "Appointment created successfully.")
                return redirect('home')  
            else:
                raise Http404("Sie müssen angemeldet sein, um einen Termin zu erstellen.")
    else:
        
        appointment_form = AppointmentForm()

    return render(request, 'settings/home.html', {
        'gallery_items': gallery_items,
        'barbers': barbers,
        'reviews': reviews,
        'appointment_form': appointment_form,
    })
