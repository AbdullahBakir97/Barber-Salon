from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView,  View , TemplateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import CustomUserCreationForm, UserProfileForm, OwnerProfileForm, CustomUserChangeForm
from .models import UserProfile, OwnerProfile
from django.contrib.auth.models import User


class CustomUserLoginView(LoginView):
    model = User
    template_name = 'accounts/registration/login.html'
    next_page = reverse_lazy('contact:management')
    
class CustomUserLogoutView(LogoutView):
    model = User
    template_name = 'accounts/registration/logout.html'
    next_page = reverse_lazy('project:home')
    
    
def user_logout(request):
    logout(request)
    return redirect('project:home')


class CustomUserSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/registration/signup.html'
    success_message = 'Account created successfully.'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.UserProfile)
        return response

    def get_success_url(self):
        return reverse_lazy('home')
    
    
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    success_message = 'Account updated successfully.'
    template_name = 'accounts/registration/users_update.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    
class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    model = User
    template_name = 'accounts/registration/users_delete.html'
    success_message = 'Account deleted successfully.'
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(reverse('accounts:management'))
    
    
def create_profile(request):
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:management')
    else:
        form = UserProfileForm()
    return render(request, 'accounts/accounts_create.html', {'form': form})

def edit_profile(request, pk):
    try:
        user_profile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return HttpResponseNotFound("UserProfile not found")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:management')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'accounts/accounts_update.html', {'form': form, 'user_profile': user_profile})


def delete_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:management')
    return render(request, 'accounts/accounts_delete.html', {'user': user})
    
class UserCretateView(SuccessMessageMixin, View):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/accounts_management.html'


def accounts_management(request):
    user_list = User.objects.all()
    accounts_list = UserProfile.objects.all()
     
    

    
    context = {
        'accounts_list': accounts_list,
        'user_list': user_list,
    }
    
    return render(request, 'accounts/accounts_management.html', context)


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/user_profile_update.html'
    success_message = 'User profile updated successfully.'

    def get_object(self, queryset=None):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return user_profile

    def get_success_url(self):
        return reverse_lazy('home')

class OwnerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = OwnerProfile
    form_class = OwnerProfileForm
    template_name = 'accounts/owner_profile_update.html'
    success_message = 'Owner profile updated successfully.'

    def get_object(self, queryset=None):
        return self.request.user.owner.owner_profile

    def test_func(self):
        return self.request.user.is_owner

    def get_success_url(self):
        return reverse_lazy('home')

class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        owner_profile, _ = OwnerProfile.objects.get_or_create(owner=self.request.user.owner)
        context['user_profile'] = user_profile
        context['owner_profile'] = owner_profile
        return context


@login_required
def profile_update(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    owner_profile, _ = OwnerProfile.objects.get_or_create(owner=request.user.owner)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        owner_form = OwnerProfileForm(request.POST, request.FILES, instance=owner_profile)

        if user_form.is_valid() and owner_form.is_valid():
            user_form.save()
            owner_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_dashboard')

    else:
        user_form = UserProfileForm(instance=user_profile)
        owner_form = OwnerProfileForm(instance=owner_profile)

    return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'owner_form': owner_form})
