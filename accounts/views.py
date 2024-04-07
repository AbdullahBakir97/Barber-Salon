from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from .forms import CustomUserCreationForm, UserProfileForm, OwnerProfileForm
from .models import UserProfile, OwnerProfile
from django.contrib.auth.models import User

class CustomUserLoginView(LoginView):
    template_name = 'accounts/registration/login.html'
    next_page = reverse_lazy('contact:management')
    
class CustomUserLogoutView(LogoutView):
    template_name = 'accounts/registration/logout.html'
    next_page = reverse_lazy('home')

class CustomUserSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_message = 'Account created successfully.'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.User)
        return response


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
