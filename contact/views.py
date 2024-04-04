from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView , DetailView, TemplateView
from .models import Owner, Barber, Review, GalleryItem, Appointment, Message, Service, Category, Product
from .forms import OwnerForm, BarberForm, GalleryItemForm, ReviewCreateForm, AppointmentForm, MessageForm, ServiceForm, ProductForm, CategoryForm
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponseServerError
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from accounts.models import OwnerProfile
import logging
from project import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger(__name__)


def my_view(request):
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
    logger = logging.getLogger(__name__)  # Get logger instance for the current module

    logger.debug('Processing my_view function...')

    try:
        # Code that may raise an exception
        result = perform_some_task()
        logger.debug(f'Result: {result}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')

    logger.debug('Exiting my_view function...')

# Define the function that performs some task (placeholder)
def perform_some_task():
    # Placeholder code
    return "Task result"

# Owner

class OwnerProfileRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        raise Http404(_("Sie sind nicht berechtigt, diese Seite zu sehen, melden sie sich erstmal an."))
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # owner_profile = request.user.owner_user_profile
        # if not owner_profile:
            # raise Http404(_("Sie dürfen diese Seite nicht anzeigen."))

        return super().dispatch(request, *args, **kwargs)

    
class OwnerCreateView(LoginRequiredMixin, CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'contact/owner/owner_create.html'
    success_url = reverse_lazy('contact:owner_detail') 

    def form_valid(self, form):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if an owner already exists
        if Owner.objects.exists():
            messages.error(self.request, _('Es kann nur einen Eigentümer geben.'))
            return self.handle_no_permission()

        form.instance.user = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, _('Ein Fehler ist aufgetreten.'))
            return self.handle_no_permission()

    def handle_no_permission(self):
        raise Http404(_("Sie sind nicht berechtigt, diese Seite zu sehen."))


class OwnerUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'contact/owner/owner_update.html'
    success_url = reverse_lazy('contact:owner_detail')

    def dispatch(self, request, *args, **kwargs):
        owner = self.get_object()
        owner_profile = owner.owner_profile
        if owner_profile and request.user != owner_profile.user:
            raise Http404(_("Sie dürfen dieses Eigentümerprofil nicht bearbeiten."))
        
        return super().dispatch(request, *args, **kwargs)
        
        
class OwnerDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Owner
    template_name = 'contact/owner/owner_delete.html'
    success_url = reverse_lazy('contact:management')

    def dispatch(self, request, *args, **kwargs):
        owner = self.get_object()
        owner_profile = owner.owner_profile
        if owner_profile and request.user != owner_profile.user:
            raise Http404(_("Sie dürfen dieses Eigentümerprofil nicht löschen."))
        return super().dispatch(request, *args, **kwargs)

class OwnerDetailView(OwnerProfileRequiredMixin, DetailView):
    model = Owner
    template_name = 'contact/owner/owner_detail.html'
    
    def get_queryset(self):
        return Owner.objects.all()
    
    
def contact_view(request):
    template_name = 'contact/contact.html'
    owner = Owner.objects.first()
    message_form = MessageForm()

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            name = message_form.cleaned_data['name']
            email = message_form.cleaned_data['email']
            phone = message_form.cleaned_data['phone']
            message = message_form.cleaned_data['message']

            Message.objects.create(name=name, email=email, phone=phone, message=message)

            try:
                send_mail(
                    f'Nachricht von {name}',
                    f'Name: {name}\nE-Mail: {email}\nTelefon: {phone}\nNachricht: {message}',
                    email,
                    [settings.EMAIL_HOST_USER,email],
                    fail_silently=False,
                )
                # Set a success message
                messages.success(request, 'Ihre Nachricht wurde erfolgreich gesendet!')
                return redirect('contact:contact')
            except Exception as e:
                # Log the error for troubleshooting
                logger.error(f'Error sending email: {e}')
                # Return a server error response
                return HttpResponseServerError("Fehler beim Senden der E-Mail. Bitte versuchen Sie es später erneut.")

    context = {
        'owner': owner,
        'message_form': message_form,
    }
    return render(request, 'contact/contact.html', context)



# Barber
class BarberCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Barber
    form_class = BarberForm
    template_name = 'contact/barber/barber_create.html'
    success_url = reverse_lazy('contact:management')

    def form_valid(self, form):
            form.instance.user = self.request.user
            name = form.cleaned_data.get('name')
            existing_barber = Barber.objects.filter(name=name).first()

            if existing_barber:
                messages.error(self.request, _('A barber with this name already exists.'))
                return self.form_invalid(form)
            else:
                return super().form_valid(form)

        
        
class BarberUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Barber
    form_class = BarberForm
    template_name = 'contact/barber/barber_update.html'
    success_url = reverse_lazy('contact:management')
    

class BarberDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Barber
    template_name = 'contact/barber/barber_delete.html'
    success_url = reverse_lazy('contact:management')
    

    def get_object(self, queryset=None):
        return get_object_or_404(Barber, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        barber = self.get_object()
        barber.delete()
        return HttpResponseRedirect(self.get_success_url())



class BarberListView(OwnerProfileRequiredMixin, ListView):
    model = Barber
    template_name = 'contact/barber/barber_list.html'
    
    def get_queryset(self):
        return Barber.objects.all()
    
class BarberManagementView(OwnerProfileRequiredMixin, ListView):
    model = Barber
    template_name = 'contact/barber/barber_management.html'
    
    def get_queryset(self):
        return Barber.objects.all()
    
    


# GalleryItem
class GalleryItemCreateView(OwnerProfileRequiredMixin, CreateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'contact/gallery/item_create.html'
    success_url = reverse_lazy('contact:management')

    def form_valid(self, form):
            form.instance.user = self.request.user
            try:
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Ein Element mit diesem Titel existiert bereits.'))
                return self.form_invalid(form)


class GalleryItemUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'contact/gallery/item_update.html'
    success_url = reverse_lazy('contact:management')


class GalleryItemDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = GalleryItem
    template_name = 'contact/gallery/item_delete.html'
    success_url = reverse_lazy('contact:management')

    def get_object(self, queryset=None):
        return get_object_or_404(GalleryItem, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return HttpResponseRedirect(self.get_success_url())


class GalleryItemListView(OwnerProfileRequiredMixin, ListView):
    model = GalleryItem
    template_name = 'contact/gallery/item_list.html'
    
    def get_queryset(self):
        return GalleryItem.objects.all()
    
    
class GalleryItemManagementView(OwnerProfileRequiredMixin, ListView):
    model = GalleryItem
    template_name = 'contact/gallery/item_management.html'
    
    def get_queryset(self):
        return GalleryItem.objects.all()



# Product
class ProductCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'contact/product/product_create.html'
    success_url = reverse_lazy('contact:management')

    @transaction.atomic
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            with transaction.atomic():
                category = Category.objects.get(name='Products')  # Get the Products category
                form.instance.category = category  # Set the category for the product
                response = super().form_valid(form)
                # Create a corresponding service instance
                service = Service.objects.create(
                    name=form.instance.name,
                    price=form.instance.price,
                    category=category  # Set the category for the service to Products
                )
                form.instance.service = service
                form.instance.save()
                return response
        except IntegrityError:
            form.add_error(None, 'Ein Element mit diesem Titel existiert bereits.')
            return self.form_invalid(form)

class ProductUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'contact/product/product_update.html'
    success_url = reverse_lazy('contact:management')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Update associated service instance
        service = self.object.service
        if service:
            service.name = form.instance.name
            service.price = form.instance.price
            service.save()
        return response

class ProductDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Product
    template_name = 'contact/product/product_delete.html'
    success_url = reverse_lazy('contact:management')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        service = product.service
        if service:
            # Delete the service, which will automatically clear any foreign key references to it
            service.delete()
        messages.success(self.request, _('Produkt wurde erfolgreich gelöscht.'))
        return super().delete(request, *args, **kwargs)

class ProductListView(OwnerProfileRequiredMixin, ListView):
    model = Product
    template_name = 'contact/product/product_list.html'
    context_object_name = 'product_list'
    
    def get_queryset(self):
        return Product.objects.all()
    
class ProductManagementView(OwnerProfileRequiredMixin, ListView):
    model = Product
    template_name = 'contact/product/product_management.html'
    context_object_name = 'product_list'
    
    def get_queryset(self):
        return Product.objects.all()
    
    
class CategoryCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'contact/prices/category_create.html'
    success_url = reverse_lazy('contact:management')

class CategoryUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'contact/prices/category_update.html'
    success_url = reverse_lazy('contact:management')

class CategoryDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Category
    template_name = 'contact/prices/category_delete.html'
    success_url = reverse_lazy('contact:management')



class ServiceCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'contact/prices/service_create.html'
    success_url = reverse_lazy('contact:management')

class ServiceUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'contact/prices/service_update.html'
    success_url = reverse_lazy('contact:management')

class ServiceDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Service
    template_name = 'contact/prices/service_delete.html'
    success_url = reverse_lazy('contact:management')
    
    
def pricing_view(request):
    if request.method == 'POST':
        # If a product is edited or deleted, redirect to the pricing view
        return redirect('pricing_view')
    categories = Category.objects.prefetch_related('service_category').all()
    services = Service.objects.exclude(product_service__isnull=True)
    return render(request, 'contact/prices/pricing.html', {'categories': categories, 'services': services})
    
      
class ServiceManagementView(OwnerProfileRequiredMixin, ListView):
    model = Service
    template_name = 'contact/prices/service_management.html'
    
    def get_queryset(self):
        return Service.objects.all()


# Review
class ReviewCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'contact/review/review_create.html'
    success_url = reverse_lazy('contact:management')

    def form_valid(self, form):
            form.instance.user = self.request.user
            form.instance.rating = form.cleaned_data['rating']
            try:
                return super().form_valid(form)
            except IntegrityError:
                messages.error(self.request, _('Eine Bewertung von diesem Benutzer für denselben Friseur existiert bereits.'))
                return self.form_invalid(form)

class ReviewUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'contact/review/review_update.html'
    success_url = reverse_lazy('contact:management')



class ReviewDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Review
    template_name = 'contact/review/review_delete.html'
    success_url = reverse_lazy('contact:management')


    def get_object(self, queryset=None):
        return get_object_or_404(Review, pk=self.kwargs['pk'])

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        review.delete()
        return HttpResponseRedirect(self.get_success_url())


class ReviewListView(ListView):
    model = Review
    template_name = 'contact/review/review_list.html'
    context_object_name = 'review_data'
    paginate_by = 2
    
    def get_queryset(self):
        return Review.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.get_queryset()
        paginator = Paginator(reviews, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        context['review_data'] = object_list
        return context
    
    
def review_list(request):
    review_data = Review.objects.all()
    paginator = Paginator(review_data, 5)

    page = request.GET.get('page')
    try:
        review_data = paginator.page(page)
    except PageNotAnInteger:
        review_data = paginator.page(1)
    except EmptyPage:
        review_data = paginator.page(paginator.num_pages)

    return render(request, 'contact/review/review_list.html', {'review_data': review_data})
    
class ReviewManagementView(OwnerProfileRequiredMixin, ListView):
    model = Review
    template_name = 'contact/review/review_management.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        return Review.objects.all()

# Appointment
class AppointmentCreateView(OwnerProfileRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'contact/appointment/appointment_create.html'
    success_url = reverse_lazy('contact:management')

    def form_valid(self, form):
            form.instance.user = self.request.user
            self.submitted = True
            return super().form_valid(form)

    
    def form_invalid(self, form):
        self.submitted = False
        return self.render_to_response(self.get_context_data(form=form))
    
    # def get_success_url(self):
    #     return reverse('contact:appointment_list')

class AppointmentUpdateView(OwnerProfileRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'contact/appointment/appointment_update.html'
    success_url = reverse_lazy('contact:management')

    # def get_success_url(self):
    #     return reverse('contact:appointment_list')
    


class AppointmentDeleteView(OwnerProfileRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'contact/appointment/appointment_delete.html'
    success_url = reverse_lazy('contact:management')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return self.success_url



class AppointmentListView(OwnerProfileRequiredMixin, ListView):
    model = Appointment
    template_name = 'contact/appointment/appointment_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title()
        return context
    
    
class AppointmentManagementView(OwnerProfileRequiredMixin, ListView):
    model = Appointment
    template_name = 'contact/appointment/appointment_management.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title()
        return context


# Visitor Views

class VisitorAppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'contact/appointment/visitor_appointment_create.html'

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({'success': True})  # Return JSON response for AJAX request
        except IntegrityError as e:
            error_message = str(e)
            return JsonResponse({'success': False, 'message': error_message}, status=400)
        

# def visitor_appointment_create(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, 'Ihre Termin wurde erfolgreich gesendet!')
#                 return HttpResponseRedirect(reverse('settings:home') + '#appointments')
#             except IntegrityError as e:
#                 error_message = str(e)
#                 messages.error(request, 'Fehler beim Senden des Formulars. Bitte versuchen Sie es erneut.')
#         else:
#             # Collect all form errors into a list
#             form_errors = []
#             for field, errors in form.errors.items():
#                 form_errors.extend(errors)

#             # Display all collected error messages
#             for error_message in form_errors:
#                 messages.error(request, error_message)

#     else:
#         form = AppointmentForm()

#     return render(request, 'settings/home.html', {'form': form})

def visitor_appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'result': 'success', 'message': 'Ihre Termin wurde erfolgreich gesendet!'})
            except IntegrityError as e:
                return JsonResponse({'result': 'error', 'message': 'Fehler beim Senden des Formulars. Bitte versuchen Sie es erneut.'})
        else:
            form_errors = form.errors.as_json()
            return JsonResponse({'result': 'error', 'errors': form_errors})
    else:
        form = AppointmentForm()

    return render(request, 'settings/home.html', {'form': form})

class VisitorReviewCreateView(CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'contact/review/visitor_review_create.html'

    def form_valid(self, form):
        try:
            self.object = form.save()
            messages.success(self.request, _('Bewertung erfolgreich hinzugefügt.'))
            
            new_review_html = render_to_string('include/reviews.html', {'review': self.object}, request=self.request)
            return JsonResponse({'html': new_review_html})
        except IntegrityError:
            messages.error(self.request, _('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.'))
            return self.form_invalid(form)

def create_visitor_review(request):
    if request.method == 'POST':
        form = ReviewCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the review form data and save to the database
            review = form.save()
            reviews_html = render_to_string('include/reviews.html', {'review_data': Review.objects.all()})
            return JsonResponse({'success': True, 'message': 'Review submitted successfully.', 'reviews_html': reviews_html})
            # Here, you can customize the success response as needed
        else:
            # Return form errors in case of validation failure
            errors = ''.join([f'<p>{error}</p>' for field, error in form.errors.items()])
            return JsonResponse({'success': False, 'errors': errors})
    else:
        # Handle GET request or other HTTP methods
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@require_POST
def submit_review(request):
    form = ReviewCreateForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            review = form.save()
            reviews_html = render_to_string('include/reviews.html', {'review_data': Review.objects.all()})
            return JsonResponse({'success': True, 'reviews_html': reviews_html})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'An error occurred while saving the review.'})
    else:
        return JsonResponse({'success': False, 'message': 'Form data is not valid.'})
        

class VisitorAppointmentListView(ListView):
    model = Appointment
    template_name = 'contact/appointment/visitor_appointment_list.html'

    def get_queryset(self):
        email = self.request.POST.get('email', 'name')
        if email:
            return Appointment.objects.filter(email=email, name=self.request.POST.get('name', ''))
        else:
            return Appointment.objects.none()

class VisitorReviewListView(ListView):
    model = Review
    template_name = 'contact/review/visitor_review_list.html'

    def get_queryset(self):
        email = self.request.POST.get('email', 'name')
        if email:
            return Review.objects.filter(email=email, name=self.request.POST.get('name', ''))
        else:
            return Review.objects.none()




def management_view(request):
    appointment_list = Appointment.objects.all()
    barber_list = Barber.objects.all()
    review_list = Review.objects.all()
    gallery_item_list = GalleryItem.objects.all()
    product_list = Product.objects.all()
    category_list = Category.objects.all()
    service_list = Service.objects.all()
    service_form = ServiceForm()
    
    context = {
        'appointment_list': appointment_list,
        'barber_list': barber_list,
        'review_list': review_list,
        'gallery_item_list': gallery_item_list,
        'category_list': category_list,
        'product_list': product_list,
        'service_list': service_list,
        'service_form': service_form,
    }
    
    return render(request, 'contact/management.html', context)
